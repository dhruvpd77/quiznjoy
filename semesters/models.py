from django.db import models

class Semester(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.semester.name})"
    
    class Meta:
        ordering = ['semester', 'name']
        unique_together = ['semester', 'name']

class Unit(models.Model):
    """Unit information with description and topics for each subject"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='units')
    unit_number = models.IntegerField()
    title = models.CharField(max_length=200, blank=True, help_text="Unit title (e.g., 'Introduction to Programming')")
    description = models.TextField(blank=True, help_text="Brief description of the unit")
    topics = models.TextField(blank=True, help_text="List of topics covered in this unit (one per line or comma-separated)")
    syllabus_pdf = models.FileField(upload_to='syllabus_pdfs/', blank=True, null=True, help_text="Upload syllabus PDF for this subject")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject.name} - Unit {self.unit_number}"
    
    def get_topics_list(self):
        """Return topics as a list"""
        if not self.topics:
            return []
        # Handle both comma-separated and newline-separated topics
        topics = self.topics.replace('\n', ',').split(',')
        return [topic.strip() for topic in topics if topic.strip()]
    
    class Meta:
        ordering = ['subject', 'unit_number']
        unique_together = ['subject', 'unit_number']


DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
]


class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    unit = models.IntegerField()
    question_text = models.TextField()
    question_image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    explanation = models.TextField(blank=True, help_text='Detailed explanation shown after quiz')
    hint = models.TextField(blank=True, help_text='Optional hint (e.g. step 1)')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium', blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text='Comma-separated: e.g. pandas, numpy')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    added_by = models.CharField(max_length=100, blank=True)
    verified_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject.name} - Unit {self.unit} - {self.question_text[:50]}"
    
    def get_tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]
    
    class Meta:
        ordering = ['subject', 'unit', 'created_at']


class ProgrammingQuestion(models.Model):
    """Programming questions (non-MCQ questions without all 4 options)"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='programming_questions')
    unit = models.IntegerField()
    question_text = models.TextField(help_text="Programming question with proper Python indentation")
    question_image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    solution = models.TextField(blank=True, null=True, help_text="Solution(s) for the question. Separate multiple solutions with '|||OPTION|||' (max 3 options)")
    csv_file = models.FileField(upload_to='programming_data/', blank=True, null=True, help_text="Optional CSV/data file for pandas/numpy questions (e.g. data for ML). Available as 'data.csv' when user runs code.")
    hint = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium', blank=True)
    tags = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    # JSON: list of {"input": "...", "expected_output": "...", "is_hidden": false}
    test_cases = models.JSONField(blank=True, null=True, help_text='List of {"input": "", "expected_output": "", "is_hidden": false}')
    added_by = models.CharField(max_length=100, blank=True)
    verified_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_solutions_list(self):
        """Parse solution field to return list of solutions (max 3)"""
        if not self.solution:
            return []
        solutions = [s.strip() for s in self.solution.split('|||OPTION|||') if s.strip()]
        return solutions[:3]
    
    def get_tags_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]
    
    def __str__(self):
        return f"{self.subject.name} - Unit {self.unit} - {self.question_text[:50]}"
    
    class Meta:
        ordering = ['subject', 'unit', 'created_at']


class ProgrammingQuestionAccess(models.Model):
    """Track when users access programming question modules unit-wise"""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='programming_question_accesses')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='programming_accesses')
    unit = models.IntegerField()
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.subject.name} - Unit {self.unit} - {self.accessed_at}"
    
    class Meta:
        ordering = ['-accessed_at']
        indexes = [
            models.Index(fields=['user', 'subject', 'unit']),
            models.Index(fields=['-accessed_at']),
        ]
        verbose_name = 'Programming Question Access'
        verbose_name_plural = 'Programming Question Accesses'


class QuestionReport(models.Model):
    """User reports for wrong/inappropriate questions"""
    REPORT_STATUS = [('pending', 'Pending'), ('resolved', 'Resolved'), ('dismissed', 'Dismissed')]
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    programming_question = models.ForeignKey(ProgrammingQuestion, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']


class AdminAuditLog(models.Model):
    """Log admin actions for accountability"""
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=50, blank=True)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']