from django.db import models
from projects.models import Project

class AnalysisResult(models.Model):
    project = models.OneToOneField(Project, related_name='analysis_result', on_delete=models.CASCADE)
    anomalies_detected = models.IntegerField()
    average_latency = models.FloatField()
    average_packet_loss = models.FloatField(default=0.0)
    average_jitter = models.FloatField(default=0.0)
    optimizations = models.JSONField(default=list)
    timestamp = models.DateTimeField(null=True, blank=True)
    anomaly_timestamp = models.DateTimeField(null=True, blank=True)
    protocol = models.CharField(max_length=50, default='Unknown')
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.project.name}"


