from django.db import models
from projects.models import Project

class PcapFile(models.Model):
    project = models.ForeignKey(Project, related_name='pcap_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='pcap_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} - {self.project.name}"

