from django.urls import path
from . import views

urlpatterns = [
    path('projects/<int:project_id>/pcap_files/', views.pcap_file_list, name='pcap_file_list'),
    path('pcap_files/<int:pk>/delete/', views.delete_pcap_file, name='delete_pcap_file'),
]
