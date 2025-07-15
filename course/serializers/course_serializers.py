from rest_framework import serializers
from course.models import Course


class CourseSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source="get_level_display", read_only=True)
    type_display  = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model  = Course
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

        
    

