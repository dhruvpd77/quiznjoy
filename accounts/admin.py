from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models import Count, Avg, Sum, Q
from .models import UserLogin
from quiz.models import QuizAttempt

class UserLoginInline(admin.TabularInline):
    """Inline display of user login history"""
    model = UserLogin
    extra = 0
    readonly_fields = ['login_time', 'ip_address']
    can_delete = False
    max_num = 10  # Show last 10 logins
    
    def has_add_permission(self, request, obj=None):
        return False

class QuizAttemptInline(admin.TabularInline):
    """Inline display of user quiz attempts"""
    model = QuizAttempt
    extra = 0
    readonly_fields = ['subject', 'unit', 'score', 'total_questions', 'quiz_mode', 'attempted_at']
    can_delete = False
    max_num = 10  # Show last 10 attempts
    
    def has_add_permission(self, request, obj=None):
        return False

# Unregister the default User admin
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Enhanced User admin with login tracking and score statistics"""
    inlines = [UserLoginInline, QuizAttemptInline]
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'last_login', 'login_count', 'total_quiz_attempts', 'average_score', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined', 'last_login']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['date_joined', 'last_login', 'login_count_display', 'quiz_stats_display']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Statistics', {
            'fields': ('login_count_display', 'quiz_stats_display'),
        }),
    )
    
    def login_count(self, obj):
        """Total number of logins"""
        return UserLogin.objects.filter(user=obj).count()
    login_count.short_description = 'Total Logins'
    login_count.admin_order_field = 'login_count'
    
    def total_quiz_attempts(self, obj):
        """Total quiz attempts"""
        return QuizAttempt.objects.filter(user=obj).count()
    total_quiz_attempts.short_description = 'Quiz Attempts'
    total_quiz_attempts.admin_order_field = 'total_quiz_attempts'
    
    def average_score(self, obj):
        """Average quiz score percentage"""
        attempts = QuizAttempt.objects.filter(user=obj)
        if not attempts.exists():
            return "N/A"
        total_score = sum(attempt.score for attempt in attempts)
        total_questions = sum(attempt.total_questions for attempt in attempts)
        if total_questions == 0:
            return "0%"
        avg = (total_score / total_questions) * 100
        return f"{avg:.1f}%"
    average_score.short_description = 'Avg Score'
    
    def login_count_display(self, obj):
        """Display login count in detail view"""
        count = UserLogin.objects.filter(user=obj).count()
        last_login_obj = UserLogin.objects.filter(user=obj).order_by('-login_time').first()
        if last_login_obj:
            return format_html(
                '<strong>Total Logins:</strong> {}<br>'
                '<strong>Last Login:</strong> {}<br>'
                '<strong>IP Address:</strong> {}',
                count,
                last_login_obj.login_time.strftime('%Y-%m-%d %H:%M:%S'),
                last_login_obj.ip_address or 'N/A'
            )
        return f"Total Logins: {count}"
    login_count_display.short_description = 'Login Information'
    
    def quiz_stats_display(self, obj):
        """Display quiz statistics in detail view"""
        attempts = QuizAttempt.objects.filter(user=obj)
        if not attempts.exists():
            return "No quiz attempts yet."
        
        total_attempts = attempts.count()
        total_score = sum(attempt.score for attempt in attempts)
        total_questions = sum(attempt.total_questions for attempt in attempts)
        avg_percentage = (total_score / total_questions * 100) if total_questions > 0 else 0
        
        best_attempt = attempts.order_by('-score').first()
        worst_attempt = attempts.order_by('score').first()
        
        return format_html(
            '<strong>Total Attempts:</strong> {}<br>'
            '<strong>Total Questions Answered:</strong> {}<br>'
            '<strong>Total Score:</strong> {} / {}<br>'
            '<strong>Average Score:</strong> {:.1f}%<br>'
            '<strong>Best Score:</strong> {} / {} ({} - Unit {})<br>'
            '<strong>Worst Score:</strong> {} / {} ({} - Unit {})',
            total_attempts,
            total_questions,
            total_score,
            total_questions,
            avg_percentage,
            best_attempt.score if best_attempt else 0,
            best_attempt.total_questions if best_attempt else 0,
            best_attempt.subject.name if best_attempt else 'N/A',
            best_attempt.unit if best_attempt else 0,
            worst_attempt.score if worst_attempt else 0,
            worst_attempt.total_questions if worst_attempt else 0,
            worst_attempt.subject.name if worst_attempt else 'N/A',
            worst_attempt.unit if worst_attempt else 0,
        )
    quiz_stats_display.short_description = 'Quiz Statistics'
    
    def get_queryset(self, request):
        """Optimize queryset with annotations"""
        qs = super().get_queryset(request)
        return qs.annotate(
            login_count=Count('login_history'),
            total_quiz_attempts=Count('quiz_attempts')
        )

@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    """Admin interface for user login history"""
    list_display = ['user', 'login_time', 'ip_address']
    list_filter = ['login_time', 'user']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'login_time', 'ip_address']
    date_hierarchy = 'login_time'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
