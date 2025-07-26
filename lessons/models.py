
# Create your models here.
from django.db import models
from course.models import Course

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    video = models.FileField(upload_to="lessons/videos/", null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["order"]
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
