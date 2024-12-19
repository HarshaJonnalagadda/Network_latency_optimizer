from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer

# List all projects or create a new project
@api_view(['GET', 'POST'])
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a project by its ID
@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        project.delete()
        return Response({'message': 'Project deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
