from rest_framework import serializers
from .models import PcapFile

class PcapFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PcapFile
        fields = ['id', 'project', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
