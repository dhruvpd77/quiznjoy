from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from semesters.models import Semester, Subject, Question, ProgrammingQuestion
from .models import QuizAttempt, QuizAnswer, QuestionBookmark, ProgrammingBookmark
from semesters.models import QuestionReport
import random
import time
import requests
import json
import subprocess
import sys
import os
import shutil
import tempfile
from django.conf import settings
from django.core.cache import cache
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
try:
    import google.generativeai as genai
except ImportError:
    genai = None

@login_required
def select_semester(request):
    semesters = Semester.objects.all()
    return render(request, 'quiz/select_semester.html', {'semesters': semesters})

@login_required
def select_subject(request, semester_id):
    semester = get_object_or_404(Semester, id=semester_id)
    subjects = Subject.objects.filter(semester=semester)
    return render(request, 'quiz/select_subject.html', {
        'semester': semester,
        'subjects': subjects
    })

@login_required
def disclaimer(request, subject_id):
    """Show disclaimer before starting quiz"""
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'quiz/disclaimer.html', {
        'subject': subject
    })

def about_us(request):
    """About Us page with creator information"""
    return render(request, 'quiz/about_us.html')

@login_required
def select_unit(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    # Get distinct units for this subject from questions
    question_units = list(Question.objects.filter(subject=subject).values_list('unit', flat=True).distinct().order_by('unit'))
    
    # Get unit information (descriptions, topics) from Unit model
    from semesters.models import Unit
    unit_info = {}
    programming_questions_count = {}  # Count programming questions per unit
    
    for unit_num in question_units:
        try:
            unit_obj = Unit.objects.get(subject=subject, unit_number=unit_num)
            unit_info[unit_num] = {
                'title': unit_obj.title or '',
                'description': unit_obj.description or '',
                'topics': unit_obj.get_topics_list() or [],
            }
        except Unit.DoesNotExist:
            unit_info[unit_num] = {
                'title': '',
                'description': '',
                'topics': [],
            }
        
        # Count programming questions for this unit
        prog_count = ProgrammingQuestion.objects.filter(subject=subject, unit=unit_num).count()
        programming_questions_count[unit_num] = prog_count
    
    return render(request, 'quiz/select_unit.html', {
        'subject': subject,
        'units': question_units,
        'unit_info': unit_info,
        'programming_questions_count': programming_questions_count,
    })

@login_required
def view_programming_questions(request, subject_id, unit):
    """Display all programming questions for a unit"""
    subject = get_object_or_404(Subject, id=subject_id)
    programming_questions = ProgrammingQuestion.objects.filter(subject=subject, unit=unit, status='published').order_by('id')
    
    # Get unit info
    from semesters.models import Unit, ProgrammingQuestionAccess
    try:
        unit_obj = Unit.objects.get(subject=subject, unit_number=unit)
        unit_title = unit_obj.title if unit_obj.title else f'Unit {unit}'
    except Unit.DoesNotExist:
        unit_title = f'Unit {unit}'
    
    # Track access - record when user opens this programming question module
    try:
        ProgrammingQuestionAccess.objects.create(
            user=request.user,
            subject=subject,
            unit=unit,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
        )
    except Exception as e:
        # Don't break the page if tracking fails
        pass
    
    return render(request, 'quiz/programming_questions.html', {
        'subject': subject,
        'unit': unit,
        'unit_title': unit_title,
        'programming_questions': programming_questions,
    })


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
@require_http_methods(["POST"])
def get_programming_solution(request, question_id):
    """Generate AI-powered solution for a programming question"""
    question = get_object_or_404(ProgrammingQuestion, id=question_id)
    
    # Get AI provider from settings
    ai_provider = getattr(settings, 'AI_PROVIDER', 'groq').lower()
    
    # Build the prompt for the AI - Focus on simplest solution
    prompt = f"""Solve this Python programming question and provide the SIMPLEST solution with proper code.

Question: {question.question_text}

Provide:
1. The simplest and most straightforward solution
2. Complete working Python code with proper indentation
3. Brief explanation if needed (keep it minimal)
4. If multiple simple approaches exist, provide up to 3 options (Option 1, Option 2, Option 3)

Format your response as:
- For single solution: Just provide the code
- For multiple solutions: Use |||OPTION||| to separate each solution

Be concise and focus on the simplest way to solve this problem."""

    try:
        solution = None
        
        # Route to appropriate AI provider
        if ai_provider == 'groq':
            solution = get_groq_solution(prompt)
        elif ai_provider == 'huggingface':
            solution = get_huggingface_solution(prompt)
        elif ai_provider == 'gemini':
            solution = get_gemini_solution(prompt)
        elif ai_provider == 'ollama':
            solution = get_ollama_solution(prompt)
        elif ai_provider == 'openai':
            solution = get_openai_solution(prompt)
        else:
            return JsonResponse({
                'error': f'Unknown AI provider: {ai_provider}. Supported: groq, huggingface, gemini, ollama, openai'
            }, status=500)
        
        if solution:
            # Save the solution to the database
            question.solution = solution
            question.save()
            
            return JsonResponse({
                'success': True,
                'solution': solution
            })
        else:
            return JsonResponse({
                'error': 'Failed to generate solution. Please check your API configuration.'
            }, status=500)
        
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        
        return JsonResponse({
            'error': f'Error generating solution: {error_message}',
            'error_type': error_type
        }, status=500)


@login_required
def select_quiz_mode(request, subject_id, unit):
    """Select quiz mode: Random or Practice All"""
    subject = get_object_or_404(Subject, id=subject_id)
    total_questions = Question.objects.filter(subject=subject, unit=unit).count()
    
    # Check for active random mode quiz session
    continue_quiz = None
    session_key = f'random_quiz_{subject_id}_{unit}'
    if session_key in request.session:
        quiz_data = request.session[session_key]
        start_time = quiz_data.get('start_time')
        if start_time:
            elapsed_time = time.time() - start_time
            remaining_time = 600 - elapsed_time  # 10 minutes = 600 seconds
            if remaining_time > 0:
                continue_quiz = {
                    'remaining_time': int(remaining_time),
                    'remaining_minutes': int(remaining_time // 60),
                    'remaining_seconds': int(remaining_time % 60)
                }
            else:
                # Time expired, clear the session
                del request.session[session_key]
    
    return render(request, 'quiz/select_mode.html', {
        'subject': subject,
        'unit': unit,
        'total_questions': total_questions,
        'continue_quiz': continue_quiz
    })

@login_required
def take_quiz(request, subject_id, unit):
    subject = get_object_or_404(Subject, id=subject_id)
    quiz_mode = request.GET.get('mode', 'random')  # Get mode from URL parameter
    
    # Check if user is trying to continue a quiz that was already submitted
    continue_quiz = request.GET.get('continue', 'false') == 'true'
    if continue_quiz:
        # If trying to continue but session doesn't exist, quiz was already submitted
        session_key = f'random_quiz_{subject_id}_{unit}'
        if session_key not in request.session or 'quiz_questions' not in request.session:
            messages.info(request, 'This quiz has already been completed. Starting a new quiz.')
            # Remove continue parameter and start fresh
            return redirect('quiz:select_mode', subject_id=subject_id, unit=unit)
    
    # Get all questions from the unit (only published)
    all_questions = list(Question.objects.filter(subject=subject, unit=unit, status='published'))
    
    if not all_questions:
        messages.error(request, 'No questions available for this unit.')
        return redirect('quiz:select_unit', subject_id=subject_id)
    
    # Initialize session key for tracking shown questions in Practice All mode
    session_key = f'practice_all_shown_{subject_id}_{unit}'
    
    if quiz_mode == 'practice_all':
        # Practice All Mode: Show questions that haven't been shown yet
        shown_question_ids = request.session.get(session_key, [])
        available_questions = [q for q in all_questions if q.id not in shown_question_ids]
        
        if not available_questions:
            # All questions have been shown, reset and start over
            messages.info(request, 'You have completed all questions! Starting fresh...')
            request.session[session_key] = []
            available_questions = all_questions
        
        # Select up to 10 questions from available ones
        if len(available_questions) <= 10:
            quiz_questions = available_questions
        else:
            quiz_questions = random.sample(available_questions, 10)
        
        # Mark these questions as shown
        shown_question_ids.extend([q.id for q in quiz_questions])
        request.session[session_key] = shown_question_ids
        
        remaining = len(all_questions) - len(shown_question_ids)
        if remaining > 0:
            messages.info(request, f'Practice All Mode: {remaining} questions remaining in this unit.')
        else:
            messages.success(request, 'You have completed all questions in this unit!')
    else:
        # Random Mode: Check if continuing an existing quiz
        session_key = f'random_quiz_{subject_id}_{unit}'
        continue_quiz = request.GET.get('continue', 'false') == 'true'
        
        # IMPORTANT: Check if quiz session already exists (for page refresh)
        # If session exists, automatically continue the quiz to preserve timer
        has_existing_session = session_key in request.session and 'quiz_questions' in request.session
        
        if (continue_quiz or has_existing_session) and session_key in request.session:
            # Continue existing quiz - use stored questions
            stored_question_ids = request.session.get('quiz_questions', [])
            
            # Verify stored questions still exist
            if stored_question_ids:
                quiz_questions = [q for q in all_questions if q.id in stored_question_ids]
                # Preserve order
                quiz_questions = sorted(quiz_questions, key=lambda q: stored_question_ids.index(q.id))
                
                # If we lost some questions, fill with new ones (shouldn't happen, but safety check)
                if len(quiz_questions) < len(stored_question_ids):
                    missing_count = len(stored_question_ids) - len(quiz_questions)
                    available_new = [q for q in all_questions if q.id not in stored_question_ids]
                    if available_new:
                        quiz_questions.extend(random.sample(available_new, min(missing_count, len(available_new))))
            else:
                # Session exists but no questions stored, start new quiz
                has_existing_session = False
            
            # Calculate remaining time
            if has_existing_session:
                quiz_data = request.session[session_key]
                start_time = quiz_data.get('start_time')
                if start_time:
                    elapsed_time = time.time() - start_time
                    remaining_time = 600 - elapsed_time
                    if remaining_time <= 0:
                        # Time expired, start new quiz
                        messages.warning(request, 'Time expired. Starting a new quiz.')
                        has_existing_session = False
                        # Clear expired session
                        del request.session[session_key]
                        if 'quiz_questions' in request.session:
                            del request.session['quiz_questions']
        
        # Start new quiz if no existing session or session expired
        if not has_existing_session:
            if len(all_questions) < 10:
                messages.warning(request, f'Only {len(all_questions)} questions available for this unit.')
                quiz_questions = all_questions
            else:
                quiz_questions = random.sample(all_questions, 10)
            
            # Store quiz start time for random mode (10 minute timer)
            request.session[session_key] = {
                'start_time': time.time()
            }
    
    # Store question IDs in session
    request.session['quiz_questions'] = [q.id for q in quiz_questions]
    request.session['subject_id'] = subject_id
    request.session['unit'] = unit
    request.session['quiz_mode'] = quiz_mode
    
    # Shuffle option order per question (A/B/C/D) for display
    questions_with_order = []
    for q in quiz_questions:
        order = random.sample(['A', 'B', 'C', 'D'], 4)
        options = [{'letter': L, 'text': getattr(q, f'option_{L.lower()}')} for L in order]
        questions_with_order.append({'question': q, 'options': options})
    
    # Calculate remaining time for template
    remaining_time = None
    if quiz_mode == 'random':
        session_key = f'random_quiz_{subject_id}_{unit}'
        if session_key in request.session:
            quiz_data = request.session[session_key]
            start_time = quiz_data.get('start_time')
            if start_time:
                elapsed_time = time.time() - start_time
                remaining_time = max(0, int(600 - elapsed_time))
    
    return render(request, 'quiz/take_quiz.html', {
        'subject': subject,
        'unit': unit,
        'questions': quiz_questions,
        'questions_with_order': questions_with_order,
        'quiz_mode': quiz_mode,
        'remaining_time': remaining_time
    })

@login_required
def submit_quiz(request):
    if request.method != 'POST':
        return redirect('quiz:select_semester')
    
    # Try to get from session first, then from POST (for timer auto-submit)
    question_ids = request.session.get('quiz_questions', [])
    subject_id = request.session.get('subject_id') or request.POST.get('subject_id')
    unit = request.session.get('unit') or request.POST.get('unit')
    quiz_mode = request.session.get('quiz_mode') or request.POST.get('quiz_mode', 'random')
    
    # Convert to proper types
    try:
        if subject_id:
            subject_id = int(subject_id)
        if unit:
            unit = int(unit)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quiz data. Please start again.')
        return redirect('quiz:select_semester')
    
    # If session data is missing, try to reconstruct from form data
    if not question_ids or not subject_id or not unit:
        # Get subject_id and unit from POST (for timer auto-submit)
        if not subject_id or not unit:
            messages.error(request, 'Quiz session expired. Please start again.')
            return redirect('quiz:select_semester')
        
        # If we have subject_id and unit but missing question_ids, try to get from database
        # This handles cases where session expired but we still have form data
        subject = get_object_or_404(Subject, id=subject_id)
        all_questions = Question.objects.filter(subject=subject, unit=unit)
        
        if all_questions.exists():
            # Extract question IDs from form data (from radio button names)
            form_question_ids = []
            for key in request.POST.keys():
                if key.startswith('question_'):
                    try:
                        q_id = int(key.replace('question_', ''))
                        form_question_ids.append(q_id)
                    except ValueError:
                        continue
            
            if form_question_ids:
                # Use questions from form
                question_ids = form_question_ids
            else:
                # Fallback: use first 10 questions
                question_ids = list(all_questions[:10].values_list('id', flat=True))
            
            # Restore session for this submission
            request.session['quiz_questions'] = question_ids
            request.session['subject_id'] = subject_id
            request.session['unit'] = unit
            request.session['quiz_mode'] = quiz_mode
        else:
            messages.error(request, 'No questions found for this quiz. Please start again.')
            return redirect('quiz:select_semester')
    
    subject = get_object_or_404(Subject, id=subject_id)
    # Get questions and preserve order
    questions_dict = {q.id: q for q in Question.objects.filter(id__in=question_ids)}
    questions = [questions_dict[qid] for qid in question_ids if qid in questions_dict]
    
    # Calculate score
    score = 0
    quiz_mode = request.session.get('quiz_mode', 'random')
    
    # Get time taken for random mode
    time_taken = None
    if quiz_mode == 'random':
        time_taken_str = request.POST.get('time_taken', '0')
        try:
            time_taken = int(time_taken_str)
        except (ValueError, TypeError):
            time_taken = None
    
    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        subject=subject,
        unit=unit,
        score=0,
        total_questions=len(question_ids),
        quiz_mode=quiz_mode,
        time_taken=time_taken
    )
    
    # Evaluate all questions:
    # - Answered questions: Check if correct/incorrect, add to score if correct
    # - Unanswered questions: Mark as "Not Attempted", no score added
    # Example: 6 answered (4 correct, 2 wrong) + 4 unanswered = Score: 4/10
    results = []
    
    # Debug: Log all POST data to see what's being submitted
    # print("POST data:", dict(request.POST))
    
    for question in questions:
        # Get selected answer - check both POST and form data
        selected = request.POST.get(f'question_{question.id}')
        
        # If not found, try alternative format (some browsers might send differently)
        if not selected:
            # Try to get from POST list
            selected_list = request.POST.getlist(f'question_{question.id}')
            if selected_list:
                selected = selected_list[0]
        
        if selected and selected.strip():
            # Answer was selected - evaluate it (correct or incorrect)
            is_correct = (selected == question.correct_answer)
            if is_correct:
                score += 1  # Only correct answers add to score
            
            # Save the answer to database
            QuizAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                question=question,
                selected_answer=selected,
                is_correct=is_correct
            )
            
            # Add to results with evaluation (correct/incorrect)
            results.append({
                'question': question,
                'selected': selected,
                'correct': question.correct_answer,
                'is_correct': is_correct,
                'attempted': True
            })
        else:
            # Question not attempted (timer expired or user didn't answer)
            # Mark as "Not Attempted" - no score, but show in results
            # Don't create QuizAnswer record for unanswered questions
            results.append({
                'question': question,
                'selected': None,
                'correct': question.correct_answer,
                'is_correct': False,
                'attempted': False
            })
    
    # Final score = only from answered questions (correct answers)
    # Example: 6 answered (4 correct) + 4 unanswered = Score: 4/10
    quiz_attempt.score = score
    quiz_attempt.save()
    
    # Store mode and subject/unit for continue option
    quiz_mode = request.session.get('quiz_mode', 'random')
    subject_id = request.session.get('subject_id')
    unit = request.session.get('unit')
    
    # Clear quiz question session and random quiz session
    del request.session['quiz_questions']
    # Clear random quiz session if it exists
    if subject_id and unit:
        session_key = f'random_quiz_{subject_id}_{unit}'
        if session_key in request.session:
            del request.session[session_key]
    
    return render(request, 'quiz/quiz_results.html', {
        'score': score,
        'total': len(question_ids),
        'results': results,
        'quiz_attempt': quiz_attempt,
        'quiz_mode': quiz_mode,
        'subject_id': subject_id,
        'unit': unit
    })

@login_required
@require_http_methods(["POST"])
def get_question_solution(request, question_id):
    """Generate AI-powered solution explanation for a question"""
    question = get_object_or_404(Question, id=question_id)
    
    # Get AI provider from settings
    ai_provider = getattr(settings, 'AI_PROVIDER', 'groq').lower()
    
    # Build the prompt for the AI - Focus on direct solution steps
    prompt = f"""Solve this MCQ question and provide ONLY the solution steps and calculations. Be direct and concise.

Question: {question.question_text}

Options:
A. {question.option_a}
B. {question.option_b}
C. {question.option_c}
D. {question.option_d}

Correct Answer: {question.correct_answer}

Provide ONLY:
1. Direct solution steps with calculations
2. How to arrive at the answer {question.correct_answer}
3. Brief explanation of why {question.correct_answer} is correct

Do NOT give lengthy explanations. Just show the solution method, calculations, and why the answer is {question.correct_answer}. Be concise and to the point."""

    try:
        solution = None
        
        # Route to appropriate AI provider
        if ai_provider == 'groq':
            solution = get_groq_solution(prompt)
        elif ai_provider == 'huggingface':
            solution = get_huggingface_solution(prompt)
        elif ai_provider == 'gemini':
            solution = get_gemini_solution(prompt)
        elif ai_provider == 'ollama':
            solution = get_ollama_solution(prompt)
        elif ai_provider == 'openai':
            solution = get_openai_solution(prompt)
        else:
            return JsonResponse({
                'error': f'Unknown AI provider: {ai_provider}. Supported: groq, huggingface, gemini, ollama, openai'
            }, status=500)
        
        if solution:
            return JsonResponse({
                'success': True,
                'solution': solution
            })
        else:
            return JsonResponse({
                'error': 'Failed to generate solution. Please check your API configuration.'
            }, status=500)
        
    except Exception as e:
        error_message = str(e)
        error_type = 'unknown'
        user_friendly_message = None
        
        # Check for specific OpenAI API errors
        if 'insufficient_quota' in error_message or 'quota' in error_message.lower():
            error_type = 'quota_exceeded'
            user_friendly_message = (
                "⚠️ API Quota Exceeded\n\n"
                "Your OpenAI API key has exceeded its quota or doesn't have billing set up.\n\n"
                "To fix this:\n"
                "1. Go to https://platform.openai.com/account/billing\n"
                "2. Add a payment method to your account\n"
                "3. Check your usage limits at https://platform.openai.com/usage\n"
                "4. If you're on a free tier, you may need to upgrade to a paid plan\n\n"
                "Alternatively, you can use a different API key with available credits."
            )
        elif 'invalid_api_key' in error_message.lower() or 'authentication' in error_message.lower():
            error_type = 'invalid_key'
            user_friendly_message = (
                "🔑 Invalid API Key\n\n"
                "The OpenAI API key is invalid or has been revoked.\n\n"
                "To fix this:\n"
                "1. Go to https://platform.openai.com/api-keys\n"
                "2. Create a new API key\n"
                "3. Update it in your settings.py or environment variables"
            )
        elif 'rate_limit' in error_message.lower():
            error_type = 'rate_limit'
            user_friendly_message = (
                "⏱️ Rate Limit Exceeded\n\n"
                "Too many requests. Please wait a moment and try again."
            )
        
        # Use user-friendly message if available, otherwise use original error
        final_message = user_friendly_message if user_friendly_message else f'Error generating solution: {error_message}'
        
        return JsonResponse({
            'error': final_message,
            'error_type': error_type
        }, status=500)


def get_groq_solution(prompt):
    """Get solution from Groq API (FREE - No payment required!)"""
    api_key = getattr(settings, 'GROQ_API_KEY', '')
    if not api_key:
        raise Exception('Groq API key not configured. Get free key at: https://console.groq.com/keys')
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",  # Free and fast model
        "messages": [
            {"role": "system", "content": "You are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 600,
        "temperature": 0.5
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    result = response.json()
    return result['choices'][0]['message']['content']


def get_huggingface_solution(prompt):
    """Get solution from Hugging Face Inference API (FREE)"""
    api_key = getattr(settings, 'HUGGINGFACE_API_KEY', '')
    if not api_key:
        raise Exception('Hugging Face API key not configured. Get free key at: https://huggingface.co/settings/tokens')
    
    # Using Meta Llama 3 model (free)
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": f"<|system|>\nYou are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations.\n<|user|>\n{prompt}\n<|assistant|>",
        "parameters": {
            "max_new_tokens": 600,
            "temperature": 0.5,
            "return_full_text": False
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()
    
    if isinstance(result, list) and len(result) > 0:
        return result[0].get('generated_text', '')
    return result.get('generated_text', '')


def get_gemini_solution(prompt):
    """Get solution from Google Gemini API (FREE tier)"""
    if genai is None:
        raise Exception('Google Generative AI library not installed. Install with: pip install google-generativeai')
    
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        raise Exception('Gemini API key not configured. Get free key at: https://makersuite.google.com/app/apikey')
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    full_prompt = f"You are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations.\n\n{prompt}"
    response = model.generate_content(full_prompt)
    return response.text


def get_ollama_solution(prompt):
    """Get solution from Ollama (FREE - Runs locally, no API key needed)"""
    base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
    url = f"{base_url}/api/generate"
    
    data = {
        "model": "llama2",  # You can change to llama3, mistral, etc.
        "prompt": f"You are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations.\n\n{prompt}",
        "stream": False,
        "options": {
            "temperature": 0.5,
            "num_predict": 600
        }
    }
    
    response = requests.post(url, json=data, timeout=120)
    response.raise_for_status()
    result = response.json()
    return result.get('response', '')


def get_openai_solution(prompt):
    """Get solution from OpenAI API (requires payment method)"""
    if OpenAI is None:
        raise Exception('OpenAI library not installed. Install with: pip install openai')
    
    api_key = getattr(settings, 'OPENAI_API_KEY', '')
    if not api_key:
        raise Exception('OpenAI API key not configured.')
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a concise educational assistant. Provide only direct solution steps and calculations. No lengthy explanations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.5
    )
    return response.choices[0].message.content


@login_required
@require_http_methods(["POST"])
def execute_python_code(request, question_id):
    """Execute Python code safely and return output"""
    # Rate limit: 30 runs per user per minute
    rl_key = f'execute_{request.user.id}'
    count = cache.get(rl_key, 0)
    if count >= 30:
        return JsonResponse({'success': False, 'error': 'Rate limit exceeded. Please wait a minute before running more code.'}, status=429)
    cache.set(rl_key, count + 1, 60)
    
    question = get_object_or_404(ProgrammingQuestion, id=question_id)
    data_csv_path = None
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        test_inputs = data.get('inputs', [])  # Optional: list of input values
        
        if not code:
            return JsonResponse({
                'success': False,
                'error': 'No code provided'
            }, status=400)
        
        # Security: Limit code length
        if len(code) > 10000:
            return JsonResponse({
                'success': False,
                'error': 'Code is too long (max 10,000 characters)'
            }, status=400)
        
        # Verify Python is available on the server
        if not sys.executable:
            return JsonResponse({
                'success': False,
                'error': 'Python interpreter not found on server. Please contact administrator.'
            }, status=500)
        
        # Check if code uses input() and handle it
        has_input = 'input(' in code
        if has_input and not test_inputs:
            # Provide helpful error message with instructions to use input section
            return JsonResponse({
                'success': False,
                'error': '⚠️ Your code uses input() but no test values were provided.\n\n'
                         '💡 How to fix:\n'
                         '1. Click the "Add Inputs" button above\n'
                         '2. Enter test values (one per line)\n'
                         '3. Run your code again\n\n'
                         'Example: If your code has:\n'
                         '  s = input("enter string")\n'
                         '  n = int(input("enter number"))\n\n'
                         'Then in the input field, enter:\n'
                         '  hello\n'
                         '  123\n\n'
                         'Each line will be provided to input() calls in order.',
                'has_input': True,
                'needs_input': True
            }, status=400)
        
        # Create a wrapper script that handles input() if needed
        if has_input and test_inputs:
            # Create a wrapper that provides inputs
            wrapper_code = f"""
import sys
from io import StringIO

# Mock input function with provided test values
_input_values = {repr(test_inputs)}
_input_index = [0]

def mock_input(prompt=''):
    if _input_index[0] < len(_input_values):
        value = _input_values[_input_index[0]]
        _input_index[0] += 1
        if prompt:
            print(prompt, end='', flush=True)
        return str(value)
    else:
        raise EOFError("No more input values available")

# Replace built-in input with mock
__builtins__['input'] = mock_input

# User's code
{code}
"""
            code_to_execute = wrapper_code
        else:
            code_to_execute = code
        
        # Create a temporary file for the code
        # On PythonAnywhere, use user's home directory for temp files instead of /tmp
        # Check if we're on PythonAnywhere by checking HOME directory pattern
        home_dir = os.environ.get('HOME', '')
        is_pythonanywhere = '/home/' in home_dir and len(home_dir.split('/')) >= 3
        
        if is_pythonanywhere:
            # PythonAnywhere: use home directory for temp files
            temp_dir = os.path.join(home_dir, 'tmp')
            os.makedirs(temp_dir, exist_ok=True)
            temp_file = os.path.join(temp_dir, f'code_{os.getpid()}_{int(time.time())}.py')
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code_to_execute)
        else:
            # Regular server: use standard tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(code_to_execute)
                temp_file = f.name
        
        try:
            # Execute Python code on SERVER (not client) with timeout (10 seconds)
            # sys.executable uses the server's Python interpreter, so it works even if
            # users don't have Python installed on their PC
            # Use the directory containing the temp file as working directory
            temp_dir = os.path.dirname(temp_file)
            data_csv_path = None
            # If this programming question has an attached CSV, copy it as data.csv so user code can pd.read_csv('data.csv')
            if getattr(question, 'csv_file', None) and question.csv_file:
                try:
                    data_csv_path = os.path.join(temp_dir, 'data.csv')
                    with question.csv_file.open('rb') as src:
                        with open(data_csv_path, 'wb') as dest:
                            dest.write(src.read())
                except Exception:
                    data_csv_path = None
            
            # Prepare environment variables - remove any that might cause config loading issues
            env = os.environ.copy()
            # Remove PYTHONPATH and other config-related env vars that might cause issues
            env.pop('PYTHONPATH', None)
            env.pop('PYTHONSTARTUP', None)
            env.pop('PYTHONHOME', None)
            
            result = subprocess.run(
                [sys.executable, '-u', temp_file],  # -u for unbuffered output
                capture_output=True,
                text=True,
                timeout=10,
                cwd=temp_dir,
                env=env,  # Use cleaned environment
                input='\n'.join(test_inputs) if test_inputs and not has_input else None
            )
            
            output = result.stdout
            error = result.stderr
            
            # Clean up temp file and attached data.csv if any
            try:
                os.unlink(temp_file)
            except Exception:
                pass
            if data_csv_path and os.path.exists(data_csv_path):
                try:
                    os.unlink(data_csv_path)
                except Exception:
                    pass
            
            if result.returncode == 0:
                return JsonResponse({
                    'success': True,
                    'output': output if output else '(No output)',
                    'error': None
                })
            else:
                return JsonResponse({
                    'success': False,
                    'output': output if output else '',
                    'error': error if error else 'Code execution failed'
                })
                
        except subprocess.TimeoutExpired:
            # Clean up temp file and data.csv
            try:
                os.unlink(temp_file)
            except Exception:
                pass
            if data_csv_path and os.path.exists(data_csv_path):
                try:
                    os.unlink(data_csv_path)
                except Exception:
                    pass
            # Check if timeout was likely due to input()
            if has_input and not test_inputs:
                error_msg = 'Code execution timed out. This usually happens when using input() without providing test values.\n\n'
            else:
                error_msg = 'Code execution timed out (max 10 seconds).\n\n'
            error_msg += '💡 Tip: If your code uses input(), either:\n'
            error_msg += '1. Remove input() and use hardcoded values for testing\n'
            error_msg += '2. Make sure your code completes within 10 seconds'
            return JsonResponse({
                'success': False,
                'error': error_msg
            }, status=408)
            
        except Exception as e:
            # Clean up temp file and data.csv
            try:
                os.unlink(temp_file)
            except Exception:
                pass
            if data_csv_path and os.path.exists(data_csv_path):
                try:
                    os.unlink(data_csv_path)
                except Exception:
                    pass
            return JsonResponse({
                'success': False,
                'error': f'Execution error: {str(e)}'
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def run_programming_tests(request, question_id):
    """Run user code against test cases and return pass/fail for each"""
    rl_key = f'run_tests_{request.user.id}'
    count = cache.get(rl_key, 0)
    if count >= 20:
        return JsonResponse({'success': False, 'error': 'Rate limit exceeded. Try again in a minute.'}, status=429)
    cache.set(rl_key, count + 1, 60)
    
    question = get_object_or_404(ProgrammingQuestion, id=question_id)
    test_cases = question.test_cases or []
    if not isinstance(test_cases, list) or len(test_cases) == 0:
        return JsonResponse({'success': False, 'error': 'No test cases defined for this question.'}, status=400)
    
    try:
        data = json.loads(request.body)
        code = (data.get('code') or '').strip()
        if not code:
            return JsonResponse({'success': False, 'error': 'No code provided.'}, status=400)
        if len(code) > 10000:
            return JsonResponse({'success': False, 'error': 'Code too long.'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    
    has_input = 'input(' in code
    results = []
    home_dir = os.environ.get('HOME', '')
    is_pythonanywhere = '/home/' in home_dir and len(home_dir.split('/')) >= 3
    temp_dir = os.path.join(home_dir, 'tmp') if is_pythonanywhere else tempfile.gettempdir()
    if is_pythonanywhere:
        os.makedirs(temp_dir, exist_ok=True)
    
    for i, tc in enumerate(test_cases):
        if not isinstance(tc, dict):
            results.append({'index': i + 1, 'passed': False, 'error': 'Invalid test case format'})
            continue
        inp = tc.get('input', '')
        expected = (tc.get('expected_output') or '').strip()
        is_hidden = tc.get('is_hidden', True)
        inputs_list = [s.strip() for s in str(inp).replace('\\n', '\n').split('\n') if s.strip() is not None]
        if has_input and not inputs_list:
            inputs_list = ['']
        if has_input:
            wrapper = f"""
_input_values = {repr(inputs_list)}
_input_index = [0]
def mock_input(prompt=''):
    if _input_index[0] < len(_input_values):
        v = _input_values[_input_index[0]]
        _input_index[0] += 1
        if prompt: print(prompt, end='', flush=True)
        return str(v)
    raise EOFError("No more input")
__builtins__['input'] = mock_input
{code}
"""
            code_to_run = wrapper
        else:
            code_to_run = code
        temp_file = os.path.join(temp_dir, f'test_{os.getpid()}_{int(time.time())}_{i}.py')
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code_to_run)
            data_csv_path = None
            if getattr(question, 'csv_file', None) and question.csv_file:
                try:
                    data_csv_path = os.path.join(temp_dir, 'data.csv')
                    with question.csv_file.open('rb') as src:
                        with open(data_csv_path, 'wb') as dest:
                            dest.write(src.read())
                except Exception:
                    pass
            env = os.environ.copy()
            env.pop('PYTHONPATH', None)
            env.pop('PYTHONSTARTUP', None)
            env.pop('PYTHONHOME', None)
            result = subprocess.run(
                [sys.executable, '-u', temp_file],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=temp_dir,
                env=env,
            )
            out = (result.stdout or '').strip()
            err = (result.stderr or '').strip()
            passed = result.returncode == 0 and out == expected
            results.append({
                'index': i + 1,
                'passed': passed,
                'expected': expected if not is_hidden else '(hidden)',
                'actual': out if not is_hidden else ('(hidden)' if not passed else out),
                'error': err if result.returncode != 0 else None,
            })
            if data_csv_path and os.path.exists(data_csv_path):
                try:
                    os.unlink(data_csv_path)
                except Exception:
                    pass
        except subprocess.TimeoutExpired:
            results.append({'index': i + 1, 'passed': False, 'error': 'Timeout (10s)'})
        except Exception as e:
            results.append({'index': i + 1, 'passed': False, 'error': str(e)[:200]})
        finally:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception:
                pass
    
    passed_count = sum(1 for r in results if r.get('passed'))
    return JsonResponse({
        'success': True,
        'total': len(results),
        'passed': passed_count,
        'results': results,
    })


@login_required
@require_http_methods(["POST"])
def evaluate_code(request, question_id):
    """Evaluate code correctness using AI"""
    # Rate limit: 15 evaluations per user per minute
    rl_key = f'evaluate_{request.user.id}'
    count = cache.get(rl_key, 0)
    if count >= 15:
        return JsonResponse({'success': False, 'error': 'Rate limit exceeded. Please wait a minute.'}, status=429)
    cache.set(rl_key, count + 1, 60)
    
    question = get_object_or_404(ProgrammingQuestion, id=question_id)
    
    try:
        data = json.loads(request.body)
        user_code = data.get('code', '').strip()
        execution_output = data.get('output', '')
        
        if not user_code:
            return JsonResponse({
                'success': False,
                'error': 'No code provided'
            }, status=400)
        
        # Get AI provider from settings
        ai_provider = getattr(settings, 'AI_PROVIDER', 'groq').lower()
        
        # Build evaluation prompt
        prompt = f"""Evaluate this Python code solution for correctness.

Question: {question.question_text}

User's Code:
```python
{user_code}
```

Execution Output:
{execution_output if execution_output else '(No output or code not executed)'}

Please evaluate:
1. Does the code solve the problem correctly?
2. Is the logic sound?
3. Are there any errors or issues?
4. Rate the solution out of 10 points

Provide your evaluation in this format:
SCORE: X/10
FEEDBACK: [Your detailed feedback]

Be constructive and educational. If the code is correct, praise it. If incorrect, explain what's wrong and suggest improvements."""
        
        try:
            evaluation = None
            
            # Route to appropriate AI provider
            if ai_provider == 'groq':
                evaluation = get_groq_solution(prompt)
            elif ai_provider == 'huggingface':
                evaluation = get_huggingface_solution(prompt)
            elif ai_provider == 'gemini':
                evaluation = get_gemini_solution(prompt)
            elif ai_provider == 'ollama':
                evaluation = get_ollama_solution(prompt)
            elif ai_provider == 'openai':
                evaluation = get_openai_solution(prompt)
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Unknown AI provider: {ai_provider}'
                }, status=500)
            
            # Parse score and feedback
            score = None
            feedback = evaluation
            
            # Try to extract score from response
            if 'SCORE:' in evaluation:
                lines = evaluation.split('\n')
                for line in lines:
                    if 'SCORE:' in line:
                        try:
                            score_part = line.split('SCORE:')[1].strip()
                            score_num = score_part.split('/')[0].strip()
                            score = int(score_num)
                            break
                        except:
                            pass
            
            # Extract feedback
            if 'FEEDBACK:' in evaluation:
                feedback = evaluation.split('FEEDBACK:')[1].strip()
            
            return JsonResponse({
                'success': True,
                'score': score,
                'feedback': feedback,
                'full_evaluation': evaluation
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error evaluating code: {str(e)}'
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        }, status=500)


# --- User dashboard: progress, bookmarks, wrong questions, report ---

@login_required
def progress_dashboard(request):
    """User progress: attempts, scores by subject/unit, recent activity"""
    attempts = QuizAttempt.objects.filter(user=request.user).select_related('subject').order_by('-attempted_at')[:50]
    total_attempts = QuizAttempt.objects.filter(user=request.user).count()
    total_correct = sum(a.score for a in QuizAttempt.objects.filter(user=request.user))
    total_questions_attempted = sum(a.total_questions for a in QuizAttempt.objects.filter(user=request.user))
    overall_pct = (total_correct / total_questions_attempted * 100) if total_questions_attempted else 0
    by_subject = {}
    for a in QuizAttempt.objects.filter(user=request.user).select_related('subject'):
        key = (a.subject.id, a.subject.name)
        if key not in by_subject:
            by_subject[key] = {'subject': a.subject, 'attempts': 0, 'correct': 0, 'total': 0}
        by_subject[key]['attempts'] += 1
        by_subject[key]['correct'] += a.score
        by_subject[key]['total'] += a.total_questions
    return render(request, 'quiz/progress_dashboard.html', {
        'attempts': attempts,
        'total_attempts': total_attempts,
        'overall_pct': round(overall_pct, 1),
        'total_correct': total_correct,
        'total_questions_attempted': total_questions_attempted,
        'by_subject': list(by_subject.values()),
    })


@login_required
def my_bookmarks(request):
    """List bookmarked MCQs and programming questions"""
    mcq_bookmarks = QuestionBookmark.objects.filter(user=request.user).select_related('question', 'question__subject').order_by('-created_at')
    prog_bookmarks = ProgrammingBookmark.objects.filter(user=request.user).select_related('programming_question', 'programming_question__subject').order_by('-created_at')
    return render(request, 'quiz/my_bookmarks.html', {
        'mcq_bookmarks': mcq_bookmarks,
        'prog_bookmarks': prog_bookmarks,
    })


@login_required
def wrong_questions(request):
    """Questions the user got wrong (from quiz attempts)"""
    wrong_answer_ids = QuizAnswer.objects.filter(quiz_attempt__user=request.user, is_correct=False).values_list('question_id', flat=True).distinct()
    questions = Question.objects.filter(id__in=wrong_answer_ids).select_related('subject').order_by('subject', 'unit')
    return render(request, 'quiz/wrong_questions.html', {'questions': questions})


@login_required
@require_http_methods(["POST"])
def bookmark_mcq_toggle(request, question_id):
    """Toggle bookmark for an MCQ"""
    question = get_object_or_404(Question, id=question_id)
    bm, created = QuestionBookmark.objects.get_or_create(user=request.user, question=question)
    if not created:
        bm.delete()
        return JsonResponse({'success': True, 'bookmarked': False})
    return JsonResponse({'success': True, 'bookmarked': True})


@login_required
@require_http_methods(["POST"])
def bookmark_programming_toggle(request, question_id):
    """Toggle bookmark for a programming question"""
    pq = get_object_or_404(ProgrammingQuestion, id=question_id)
    bm, created = ProgrammingBookmark.objects.get_or_create(user=request.user, programming_question=pq)
    if not created:
        bm.delete()
        return JsonResponse({'success': True, 'bookmarked': False})
    return JsonResponse({'success': True, 'bookmarked': True})


@login_required
@require_http_methods(["POST"])
def report_question(request):
    """Submit a report for wrong/inappropriate question"""
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        programming_question_id = data.get('programming_question_id')
        reason = (data.get('reason') or '').strip()
        if not reason:
            return JsonResponse({'success': False, 'error': 'Reason is required.'}, status=400)
        if question_id:
            question = get_object_or_404(Question, id=question_id)
            QuestionReport.objects.create(user=request.user, question=question, reason=reason)
        elif programming_question_id:
            pq = get_object_or_404(ProgrammingQuestion, id=programming_question_id)
            QuestionReport.objects.create(user=request.user, programming_question=pq, reason=reason)
        else:
            return JsonResponse({'success': False, 'error': 'Specify question_id or programming_question_id.'}, status=400)
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
