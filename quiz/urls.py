from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.select_semester, name='select_semester'),
    path('semester/<int:semester_id>/', views.select_subject, name='select_subject'),
    path('subject/<int:subject_id>/disclaimer/', views.disclaimer, name='disclaimer'),
    path('subject/<int:subject_id>/units/', views.select_unit, name='select_unit'),
    path('subject/<int:subject_id>/unit/<int:unit>/mode/', views.select_quiz_mode, name='select_mode'),
    path('subject/<int:subject_id>/unit/<int:unit>/quiz/', views.take_quiz, name='take_quiz'),
    path('subject/<int:subject_id>/unit/<int:unit>/programming/', views.view_programming_questions, name='view_programming_questions'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('question/<int:question_id>/solution/', views.get_question_solution, name='get_question_solution'),
    path('programming-question/<int:question_id>/solution/', views.get_programming_solution, name='get_programming_solution'),
    path('programming-question/<int:question_id>/execute/', views.execute_python_code, name='execute_python_code'),
    path('programming-question/<int:question_id>/run-tests/', views.run_programming_tests, name='run_programming_tests'),
    path('programming-question/<int:question_id>/evaluate/', views.evaluate_code, name='evaluate_code'),
    path('about/', views.about_us, name='about_us'),
    path('dashboard/', views.progress_dashboard, name='progress_dashboard'),
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('wrong-questions/', views.wrong_questions, name='wrong_questions'),
    path('question/<int:question_id>/bookmark/', views.bookmark_mcq_toggle, name='bookmark_mcq_toggle'),
    path('programming-question/<int:question_id>/bookmark/', views.bookmark_programming_toggle, name='bookmark_programming_toggle'),
    path('report-question/', views.report_question, name='report_question'),
]

