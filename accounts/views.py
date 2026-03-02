from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from .models import UserLogin
from quiz.models import QuizAttempt

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('quiz:select_semester')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Track initial login time
            UserLogin.objects.create(
                user=user,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, 'Account created successfully!')
            return redirect('quiz:select_semester')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('quiz:select_semester')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Track login time
                UserLogin.objects.create(
                    user=user,
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                messages.success(request, f'Welcome back, {username}!')
                return redirect('quiz:select_semester')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    from quiz.models import QuizAttempt
    quiz_history = QuizAttempt.objects.filter(user=request.user).select_related('subject')
    
    # Calculate average score percentage
    average_percentage = 0
    if quiz_history.exists():
        total_percentage = 0
        for attempt in quiz_history:
            percentage = (attempt.score / attempt.total_questions) * 100 if attempt.total_questions > 0 else 0
            total_percentage += percentage
        average_percentage = round(total_percentage / quiz_history.count())
    
    # Get best score
    best_score = quiz_history.order_by('-score').first() if quiz_history.exists() else None
    
    context = {
        'quiz_history': quiz_history,
        'average_percentage': average_percentage,
        'best_score': best_score,
    }
    return render(request, 'accounts/profile.html', context)

@staff_member_required
def admin_user_management(request):
    """Admin dashboard for user management and tracking"""
    from semesters.models import Subject
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(
            username__icontains=search_query
        ) | User.objects.filter(
            email__icontains=search_query
        )
    else:
        users = User.objects.all()
    
    # Get all users with statistics
    users = users.annotate(
        login_count=Count('login_history'),
        quiz_attempts_count=Count('quiz_attempts'),
        total_score=Sum('quiz_attempts__score'),
        total_questions=Sum('quiz_attempts__total_questions')
    ).order_by('-date_joined')
    
    # Overall statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_logins = UserLogin.objects.count()
    total_quiz_attempts = QuizAttempt.objects.count()
    
    # Calculate average score across all users
    all_attempts = QuizAttempt.objects.all()
    total_all_score = sum(a.score for a in all_attempts)
    total_all_questions = sum(a.total_questions for a in all_attempts)
    overall_avg_score = (total_all_score / total_all_questions * 100) if total_all_questions > 0 else 0
    
    # Recent logins (last 10)
    recent_logins = UserLogin.objects.select_related('user').order_by('-login_time')[:10]
    
    # Top performers
    top_performers = []
    for user in users:
        if user.quiz_attempts_count > 0 and user.total_questions and user.total_questions > 0:
            avg_score = (user.total_score / user.total_questions) * 100
            top_performers.append({
                'user': user,
                'avg_score': round(avg_score, 1),
                'attempts': user.quiz_attempts_count,
                'total_score': user.total_score or 0,
                'total_questions': user.total_questions or 0
            })
    
    top_performers = sorted(top_performers, key=lambda x: x['avg_score'], reverse=True)[:10]
    
    # Unit-wise statistics
    unit_stats = {}
    for attempt in QuizAttempt.objects.select_related('subject').all():
        key = f"{attempt.subject.name} - Unit {attempt.unit}"
        if key not in unit_stats:
            unit_stats[key] = {
                'subject': attempt.subject.name,
                'unit': attempt.unit,
                'total_attempts': 0,
                'total_score': 0,
                'total_questions': 0,
                'users_count': set()
            }
        unit_stats[key]['total_attempts'] += 1
        unit_stats[key]['total_score'] += attempt.score
        unit_stats[key]['total_questions'] += attempt.total_questions
        unit_stats[key]['users_count'].add(attempt.user_id)
    
    # Calculate averages and convert sets to counts
    for key in unit_stats:
        stats = unit_stats[key]
        stats['users_count'] = len(stats['users_count'])
        if stats['total_questions'] > 0:
            stats['avg_percentage'] = round((stats['total_score'] / stats['total_questions']) * 100, 1)
        else:
            stats['avg_percentage'] = 0
    
    # Sort unit stats by total attempts
    unit_stats_list = sorted(unit_stats.items(), key=lambda x: x[1]['total_attempts'], reverse=True)[:10]
    
    # Subject-wise statistics
    subject_stats = {}
    for attempt in QuizAttempt.objects.select_related('subject').all():
        subject_name = attempt.subject.name
        if subject_name not in subject_stats:
            subject_stats[subject_name] = {
                'total_attempts': 0,
                'total_score': 0,
                'total_questions': 0,
                'users_count': set()
            }
        subject_stats[subject_name]['total_attempts'] += 1
        subject_stats[subject_name]['total_score'] += attempt.score
        subject_stats[subject_name]['total_questions'] += attempt.total_questions
        subject_stats[subject_name]['users_count'].add(attempt.user_id)
    
    for subject_name in subject_stats:
        stats = subject_stats[subject_name]
        stats['users_count'] = len(stats['users_count'])
        if stats['total_questions'] > 0:
            stats['avg_percentage'] = round((stats['total_score'] / stats['total_questions']) * 100, 1)
        else:
            stats['avg_percentage'] = 0
    
    subject_stats_list = sorted(subject_stats.items(), key=lambda x: x[1]['total_attempts'], reverse=True)
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'total_logins': total_logins,
        'total_quiz_attempts': total_quiz_attempts,
        'overall_avg_score': round(overall_avg_score, 1),
        'recent_logins': recent_logins,
        'top_performers': top_performers,
        'unit_stats': unit_stats_list,
        'subject_stats': subject_stats_list,
        'search_query': search_query,
    }
    return render(request, 'accounts/admin_user_management.html', context)

@staff_member_required
def admin_user_detail(request, user_id):
    """Detailed view of a specific user"""
    user = get_object_or_404(User, id=user_id)
    
    # Login history
    login_history = UserLogin.objects.filter(user=user).order_by('-login_time')
    total_logins = login_history.count()
    last_login_obj = login_history.first()
    
    # Quiz attempts
    quiz_attempts = QuizAttempt.objects.filter(user=user).select_related('subject').order_by('-attempted_at')
    total_attempts = quiz_attempts.count()
    
    # Add percentage and time info to each attempt for template display
    for attempt in quiz_attempts:
        if attempt.total_questions > 0:
            attempt.percentage = round((attempt.score / attempt.total_questions) * 100, 1)
        else:
            attempt.percentage = 0
        
        # Format time taken
        if attempt.time_taken:
            minutes = attempt.time_taken // 60
            seconds = attempt.time_taken % 60
            attempt.time_display = f"{minutes}:{seconds:02d}"
        else:
            attempt.time_display = "N/A"
    
    # Calculate statistics
    total_score = sum(attempt.score for attempt in quiz_attempts)
    total_questions = sum(attempt.total_questions for attempt in quiz_attempts)
    avg_percentage = (total_score / total_questions * 100) if total_questions > 0 else 0
    
    # Time statistics (only for random mode attempts)
    random_attempts = [a for a in quiz_attempts if a.quiz_mode == 'random' and a.time_taken]
    if random_attempts:
        total_time = sum(a.time_taken for a in random_attempts)
        avg_time = total_time / len(random_attempts)
        fastest_attempt = min(random_attempts, key=lambda x: x.time_taken)
        slowest_attempt = max(random_attempts, key=lambda x: x.time_taken)
        
        def format_time(seconds):
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}:{secs:02d}"
        
        time_stats = {
            'total_time': format_time(total_time),
            'avg_time': format_time(int(avg_time)),
            'fastest': fastest_attempt,
            'slowest': slowest_attempt,
            'fastest_time': format_time(fastest_attempt.time_taken),
            'slowest_time': format_time(slowest_attempt.time_taken),
            'random_attempts_count': len(random_attempts)
        }
    else:
        time_stats = None
    
    best_attempt = quiz_attempts.order_by('-score').first() if quiz_attempts.exists() else None
    worst_attempt = quiz_attempts.order_by('score').first() if quiz_attempts.exists() else None
    
    # Subject-wise performance
    subject_stats = {}
    for attempt in quiz_attempts:
        key = f"{attempt.subject.name} - Unit {attempt.unit}"
        if key not in subject_stats:
            subject_stats[key] = {
                'subject': attempt.subject.name,
                'unit': attempt.unit,
                'attempts': 0,
                'total_score': 0,
                'total_questions': 0,
                'best_score': 0,
                'worst_score': float('inf'),
            }
        subject_stats[key]['attempts'] += 1
        subject_stats[key]['total_score'] += attempt.score
        subject_stats[key]['total_questions'] += attempt.total_questions
        if attempt.score > subject_stats[key]['best_score']:
            subject_stats[key]['best_score'] = attempt.score
        if attempt.score < subject_stats[key]['worst_score']:
            subject_stats[key]['worst_score'] = attempt.score
    
    for key in subject_stats:
        stats = subject_stats[key]
        if stats['total_questions'] > 0:
            stats['avg_percentage'] = round((stats['total_score'] / stats['total_questions']) * 100, 1)
        else:
            stats['avg_percentage'] = 0
        if stats['worst_score'] == float('inf'):
            stats['worst_score'] = 0
    
    # Quiz mode statistics
    random_mode_count = quiz_attempts.filter(quiz_mode='random').count()
    practice_mode_count = quiz_attempts.filter(quiz_mode='practice_all').count()
    
    # Recent activity (last 7 days)
    from datetime import datetime, timedelta
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_attempts = quiz_attempts.filter(attempted_at__gte=seven_days_ago).count()
    recent_logins_count = login_history.filter(login_time__gte=seven_days_ago).count()
    
    context = {
        'user': user,
        'login_history': login_history[:50],  # Show last 50 logins
        'total_logins': total_logins,
        'last_login_obj': last_login_obj,
        'quiz_attempts': quiz_attempts[:100],  # Show last 100 attempts
        'total_attempts': total_attempts,
        'total_score': total_score,
        'total_questions': total_questions,
        'avg_percentage': round(avg_percentage, 1),
        'best_attempt': best_attempt,
        'worst_attempt': worst_attempt,
        'subject_stats': subject_stats,
        'time_stats': time_stats,
        'random_mode_count': random_mode_count,
        'practice_mode_count': practice_mode_count,
        'recent_attempts': recent_attempts,
        'recent_logins_count': recent_logins_count,
    }
    return render(request, 'accounts/admin_user_detail.html', context)
