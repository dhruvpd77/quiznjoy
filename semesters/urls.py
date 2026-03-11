from django.urls import path
from . import views

app_name = 'semesters'

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create-semester/', views.create_semester, name='create_semester'),
    path('admin/edit-semester/<int:semester_id>/', views.edit_semester, name='edit_semester'),
    path('admin/delete-semester/<int:semester_id>/', views.delete_semester, name='delete_semester'),
    path('admin/create-subject/', views.create_subject, name='create_subject'),
    path('admin/edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('admin/delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('admin/upload-questions/', views.upload_questions, name='upload_questions'),
    path('admin/download-upload-template/', views.download_upload_template, name='download_upload_template'),
    path('admin/manage-semesters/', views.manage_semesters, name='manage_semesters'),
    path('admin/manage-subjects/<int:semester_id>/', views.manage_subjects, name='manage_subjects'),
    path('admin/manage-questions/<int:subject_id>/', views.manage_questions, name='manage_questions'),
    path('admin/export-questions/<int:subject_id>/', views.export_questions, name='export_questions'),
    path('admin/add-question/<int:subject_id>/', views.add_question, name='add_question'),
    path('admin/edit-question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('admin/delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('admin/delete-unit-questions/<int:subject_id>/<int:unit>/', views.delete_unit_questions, name='delete_unit_questions'),
    path('admin/delete-all-questions/<int:subject_id>/', views.delete_all_questions, name='delete_all_questions'),
    path('admin/manage-units/<int:subject_id>/', views.manage_units, name='manage_units'),
    path('admin/edit-unit/<int:unit_id>/', views.edit_unit, name='edit_unit'),
    path('admin/create-unit/<int:subject_id>/<int:unit_number>/', views.create_unit, name='create_unit'),
    # Programming Question Management URLs
    path('admin/manage-programming-questions/<int:subject_id>/', views.manage_programming_questions, name='manage_programming_questions'),
    path('admin/add-programming-question/<int:subject_id>/', views.add_programming_question, name='add_programming_question'),
    path('admin/add-multiple-programming-questions/<int:subject_id>/', views.add_multiple_programming_questions, name='add_multiple_programming_questions'),
    path('admin/edit-programming-question/<int:programming_question_id>/', views.edit_programming_question, name='edit_programming_question'),
    path('admin/delete-programming-question/<int:programming_question_id>/', views.delete_programming_question, name='delete_programming_question'),
    path('admin/delete-unit-programming-questions/<int:subject_id>/<int:unit>/', views.delete_unit_programming_questions, name='delete_unit_programming_questions'),
    path('admin/delete-all-programming-questions/<int:subject_id>/', views.delete_all_programming_questions, name='delete_all_programming_questions'),
    path('admin/programming-question-analytics/', views.programming_question_analytics, name='programming_question_analytics'),
    # Paper Generation
    path('admin/paper-generation/', views.paper_generation, name='paper_generation'),
    path('admin/paper-generation-units/<int:subject_id>/', views.paper_generation_units, name='paper_generation_units'),
    path('admin/paper-preview/', views.paper_preview, name='paper_preview'),
    path('admin/paper-shuffle/', views.paper_shuffle, name='paper_shuffle'),
    path('admin/paper-shuffle-question/<int:position>/', views.paper_shuffle_question, name='paper_shuffle_question'),
    path('admin/paper-download/', views.paper_download, name='paper_download'),
]

