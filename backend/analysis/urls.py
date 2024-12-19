from django.urls import path
from . import views

urlpatterns = [
    path('projects/<int:project_id>/analyze/', views.analyze_project, name='analyze_project'),
    path('projects/<int:project_id>/result/', views.get_analysis_result, name='get_analysis_result'),
]
