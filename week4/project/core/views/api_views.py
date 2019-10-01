from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.models import Project
from core.serializers import ProjectSerializer
from django.shortcuts import get_object_or_404
from core.permissions import IsOwner
from utils.constants import NEW, TO_DO, IN_PROGRESS, DONE


class ProjectListAPIView(APIView):

    http_method_names = ['get', 'post',]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        projects = request.user.projects
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

class ProjectDetailAPIView(APIView):
    
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        if project.creator == request.user:
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    def put(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        if project.creator == request.user:
            serializer = ProjectSerializer(instance=project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        if project.creator == request.user:
            project.delete()
            return Response("You deleted project")
        return Response(status=status.HTTP_403_FORBIDDEN)
