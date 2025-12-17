from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Resume
from .serializers import ResumeSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Resume uploads.
    
    Provides:
    - POST /api/resumes/ - Upload a new resume
    - GET /api/resumes/ - List all resumes for the authenticated user
    - GET /api/resumes/{id}/ - Retrieve a specific resume
    - DELETE /api/resumes/{id}/ - Delete a resume
    """
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     """Return only resumes belonging to the authenticated user"""
    #     return Resume.objects.filter(user=self.request.user)
    
    # def perform_create(self, serializer):
    #     """Create a resume and automatically associate it with the current user"""
    #     serializer.save(user=self.request.user)
    
    # @action(detail=True, methods=['get'])
    # def download(self, request, pk=None):
    #     """
    #     Download endpoint for a resume file.
    #     GET /api/resumes/{id}/download/
    #     """
    #     resume = self.get_object()
    #     if not resume.file:
    #         return Response(
    #             {'error': 'No file associated with this resume'},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
        
    #     # Return the file URL
    #     file_url = request.build_absolute_uri(resume.file.url)
    #     return Response({
    #         'file_url': file_url,
    #         'filename': resume.file.name.split('/')[-1] if resume.file.name else None
    #     })
