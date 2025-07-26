from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Lesson
from .lesson_serializers import LessonSerializer
from rest_framework.permissions import IsAuthenticated
from course.permissions import IsCourseTeacherOrAdmin #custom permission to check if the user is a teacher or admin of the course

class LessonViewSet(ModelViewSet):
    """
    ViewSet for managing lessons nested under a course.
    URL: /api/courses/<course_pk>/lessons/
    """
    serializer_class = LessonSerializer
    permission_classes = [IsCourseTeacherOrAdmin]

    def get_queryset(self):
        """
        Returns the queryset of lessons filtered by the course primary key.
        """
        course_pk = self.kwargs.get('course_pk')
        return Lesson.objects.filter(course_id=course_pk)
    
    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(course_id=course_id)
        """
        Automatically assign the course to the lesson during creation,
        using the course ID from the URL, not from request data.
        """
         