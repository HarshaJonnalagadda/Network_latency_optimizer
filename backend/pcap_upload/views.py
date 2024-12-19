from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import PcapFile
from .serializers import PcapFileSerializer
from projects.models import Project

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser])
def pcap_file_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'GET':
        pcap_files = project.pcap_files.all()
        serializer = PcapFileSerializer(pcap_files, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        files = request.FILES.getlist('files')
        print(request.FILES)  # To check if files are being sent in the request
        files = request.FILES.getlist('files')
        print(files)  # To see the list of files received

        if not files:
            return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_files = []
        for file in files:
            serializer = PcapFileSerializer(data={'file': file, 'project': project.id})
            if serializer.is_valid():
                serializer.save(project=project)
                uploaded_files.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(uploaded_files, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_pcap_file(request, pk):
    pcap_file = get_object_or_404(PcapFile, pk=pk)
    pcap_file.delete()
    return Response({'message': 'File deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
