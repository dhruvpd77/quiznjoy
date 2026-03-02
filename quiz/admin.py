from django.contrib import admin
from django.utils.html import format_html
from .models import QuizAttempt, QuizAnswer

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'unit', 'score_display', 'quiz_mode', 'attempted_at', 'time_taken_display']
    list_filter = ['subject', 'unit', 'quiz_mode', 'attempted_at']
    search_fields = ['user__username', 'subject__name']
    readonly_fields = ['user', 'subject', 'unit', 'score', 'total_questions', 'quiz_mode', 'attempted_at', 'time_taken', 'score_percentage']
    date_hierarchy = 'attempted_at'
    
    fieldsets = (
        ('Quiz Information', {
            'fields': ('user', 'subject', 'unit', 'quiz_mode')
        }),
        ('Results', {
            'fields': ('score', 'total_questions', 'score_percentage', 'time_taken', 'attempted_at')
        }),
    )
    
    def score_display(self, obj):
        """Display score with percentage"""
        percentage = (obj.score / obj.total_questions * 100) if obj.total_questions > 0 else 0
        color = 'green' if percentage >= 70 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} / {} ({:.1f}%)</span>',
            color,
            obj.score,
            obj.total_questions,
            percentage
        )
    score_display.short_description = 'Score'
    score_display.admin_order_field = 'score'
    
    def time_taken_display(self, obj):
        """Display time taken in MM:SS format"""
        if obj.time_taken is None:
            return "N/A"
        minutes = obj.time_taken // 60
        seconds = obj.time_taken % 60
        return f"{minutes}:{seconds:02d}"
    time_taken_display.short_description = 'Time Taken'
    
    def score_percentage(self, obj):
        """Calculate score percentage"""
        if obj.total_questions == 0:
            return "0%"
        percentage = (obj.score / obj.total_questions) * 100
        return f"{percentage:.1f}%"
    score_percentage.short_description = 'Score %'

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz_attempt', 'question_preview', 'selected_answer', 'correct_answer_display', 'is_correct_display']
    list_filter = ['is_correct', 'quiz_attempt__subject', 'quiz_attempt__unit']
    search_fields = ['quiz_attempt__user__username', 'question__question_text']
    readonly_fields = ['quiz_attempt', 'question', 'selected_answer', 'correct_answer_display', 'is_correct']
    
    def question_preview(self, obj):
        """Show question text preview"""
        text = obj.question.question_text[:50]
        return f"{text}..." if len(obj.question.question_text) > 50 else text
    question_preview.short_description = 'Question'
    
    def correct_answer_display(self, obj):
        """Show correct answer"""
        return obj.question.correct_answer
    correct_answer_display.short_description = 'Correct Answer'
    
    def is_correct_display(self, obj):
        """Display is_correct with color"""
        if obj.is_correct:
            return format_html('<span style="color: green; font-weight: bold;">✓ Correct</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">✗ Wrong</span>')
    is_correct_display.short_description = 'Result'
