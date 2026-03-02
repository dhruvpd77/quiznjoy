from django.db import models
from django.contrib.auth.models import User

class UserLogin(models.Model):
    """Track all user login times"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-login_time']
        verbose_name = 'User Login'
        verbose_name_plural = 'User Logins'
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time.strftime('%Y-%m-%d %H:%M:%S')}"
