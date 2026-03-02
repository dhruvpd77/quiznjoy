from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('admin/users/', views.admin_user_management, name='admin_user_management'),
    path('admin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
]

