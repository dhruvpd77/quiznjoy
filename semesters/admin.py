from django.contrib import admin
from .models import Semester, Subject, Question, Unit, ProgrammingQuestion, ProgrammingQuestionAccess, QuestionReport, AdminAuditLog

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'semester', 'created_at']
    list_filter = ['semester']
    search_fields = ['name', 'code']

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['subject', 'unit_number', 'title', 'created_at']
    list_filter = ['subject', 'unit_number']
    search_fields = ['title', 'description', 'topics']
    ordering = ['subject', 'unit_number']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'subject', 'unit', 'correct_answer', 'added_by', 'verified_by']
    list_filter = ['subject', 'unit', 'correct_answer']
    search_fields = ['question_text', 'added_by', 'verified_by']

@admin.register(ProgrammingQuestion)
class ProgrammingQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'subject', 'unit', 'added_by', 'verified_by', 'created_at']
    list_filter = ['subject', 'unit']
    search_fields = ['question_text', 'added_by', 'verified_by']
    fieldsets = (
        ('Question Details', {
            'fields': ('subject', 'unit', 'question_text', 'question_image', 'csv_file')
        }),
        ('Solution', {
            'fields': ('solution',),
            'description': 'Enter solution(s). For multiple solutions, separate them with |||OPTION||| (max 3 options).'
        }),
        ('Metadata', {
            'fields': ('added_by', 'verified_by')
        }),
    )


@admin.register(ProgrammingQuestionAccess)
class ProgrammingQuestionAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'unit', 'accessed_at', 'ip_address']
    list_filter = ['subject', 'unit', 'accessed_at']
    search_fields = ['user__username', 'user__email', 'subject__name', 'ip_address']
    readonly_fields = ['user', 'subject', 'unit', 'accessed_at', 'ip_address', 'user_agent']
    date_hierarchy = 'accessed_at'
    ordering = ['-accessed_at']
    
    def has_add_permission(self, request):
        # Prevent manual creation - only track via views
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(QuestionReport)
class QuestionReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'programming_question', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['reason', 'user__username']
    readonly_fields = ['user', 'question', 'programming_question', 'reason', 'created_at']
    ordering = ['-created_at']


@admin.register(AdminAuditLog)
class AdminAuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_id', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['action', 'details']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'details', 'created_at']
    ordering = ['-created_at']
    def has_add_permission(self, request):
        return False
