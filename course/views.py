from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import Course
from course.serializers.course_serializers import CourseSerializer
from .permissions import IsCourseTeacherOrAdmin

from rest_framework.viewsets import ReadOnlyModelViewSet
from course.models import Category
from course.serializers.category_serializers import CategorySerializer

class CourseViewSet(ModelViewSet):
    """
    Standard CRUD + an extra 'publish' action teachers/admins can call.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsCourseTeacherOrAdmin]

    # Example custom endpoint: PATCH /courses/{id}/publish/
    #publish action to set the course as active
    #users visibility is controlled by the is_active field
    @action(detail=True, methods=["patch"], permission_classes=[IsCourseTeacherOrAdmin])
    def publish(self, request, pk=None):
        course = self.get_object()
        course.is_active = True
        course.save(update_fields=["is_active"])
        return Response({"status": "published"}, status=status.HTTP_200_OK)



#catergory viewset for read-only access to categories
class CategoryViewSet(ReadOnlyModelViewSet):
    """
    Read-only viewset for categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser] # No special permissions needed for read-only access

