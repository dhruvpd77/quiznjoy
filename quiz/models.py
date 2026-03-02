from django.db import models
from django.contrib.auth.models import User
from semesters.models import Subject, Question, ProgrammingQuestion

class QuizAttempt(models.Model):
    QUIZ_MODE_CHOICES = [
        ('random', 'Random Mode'),
        ('practice_all', 'Practice All Mode'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unit = models.IntegerField()
    score = models.IntegerField()
    total_questions = models.IntegerField(default=10)
    quiz_mode = models.CharField(max_length=20, choices=QUIZ_MODE_CHOICES, default='random')
    attempted_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.IntegerField(null=True, blank=True, help_text='Time taken in seconds (only for random mode)')
    
    def __str__(self):
        return f"{self.user.username} - {self.subject.name} - Unit {self.unit} - {self.score}/{self.total_questions}"
    
    def get_time_taken_display(self):
        """Format time_taken in MM:SS format"""
        if self.time_taken is None:
            return None
        minutes = self.time_taken // 60
        seconds = self.time_taken % 60
        return f"{minutes}:{seconds:02d}"
    
    class Meta:
        ordering = ['-attempted_at']

class QuizAnswer(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    is_correct = models.BooleanField()
    
    def __str__(self):
        return f"{self.quiz_attempt.user.username} - Question {self.question.id}"
    
    class Meta:
        ordering = ['id']


class QuestionBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mcq_bookmarks')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'question']
        ordering = ['-created_at']


class ProgrammingBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='programming_bookmarks')
    programming_question = models.ForeignKey(ProgrammingQuestion, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'programming_question']
        ordering = ['-created_at']
