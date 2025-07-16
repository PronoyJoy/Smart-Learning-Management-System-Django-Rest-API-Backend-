from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from course.models import Course, Category
from rest_framework import status

User = get_user_model()


class CourseViewSetTests(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="pass123", role="teacher")
        self.other_teacher = User.objects.create_user(username="other_teacher", password="pass123", role="teacher")
        self.admin = User.objects.create_superuser(username="admin", password="admin123")
        self.category = Category.objects.create(title="Programming")
        self.course_data = {
            "title": "Python 101",
            "description": "Intro to Python",
            "price": 0,
            "level": "beginner",
            "type": "free",
            "tags": ["python", "beginner"],
            "category": self.category.id,
            "instructor": self.teacher.id,
        }

    def test_teacher_can_create_free_course(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(reverse("course-list"), self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_cannot_create_free_course_with_price(self):
        self.client.force_authenticate(user=self.teacher)
        self.course_data["price"] = 10.0
        response = self.client.post(reverse("course-list"), self.course_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_teacher_cannot_create_paid_course_with_zero_price(self):
        self.client.force_authenticate(user=self.teacher)
        self.course_data["type"] = "paid"
        self.course_data["price"] = 0
        response = self.client.post(reverse("course-list"), self.course_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_teacher_can_update_own_course(self):
        self.client.force_authenticate(user=self.teacher)
        course = Course.objects.create(**self.course_data)
        url = reverse("course-detail", args=[course.id])
        response = self.client.patch(url, {"title": "Updated Title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.title, "Updated Title")

    def test_teacher_cannot_update_others_course(self):
        self.client.force_authenticate(user=self.other_teacher)
        course = Course.objects.create(**self.course_data)
        url = reverse("course-detail", args=[course.id])
        response = self.client.patch(url, {"title": "Hack attempt"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_course(self):
        self.client.force_authenticate(user=self.admin)
        course = Course.objects.create(**self.course_data)
        url = reverse("course-detail", args=[course.id])
        response = self.client.patch(url, {"title": "Admin Edit"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_publish_sets_course_active(self):
        self.client.force_authenticate(user=self.teacher)
        course = Course.objects.create(**self.course_data, is_active=False)
        url = reverse("course-publish", args=[course.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertTrue(course.is_active)

    def test_publish_denied_for_non_owner(self):
        self.client.force_authenticate(user=self.other_teacher)
        course = Course.objects.create(**self.course_data, is_active=False)
        url = reverse("course-publish", args=[course.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
