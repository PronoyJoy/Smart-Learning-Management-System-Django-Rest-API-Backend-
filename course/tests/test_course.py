from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from course.models import Course, Category
from rest_framework import status

User = get_user_model()


class CourseViewSetTests(APITestCase):
    """
    Covers:
    - create (teacher)
    - update (teacher owns / teacher foreign / admin)
    - custom publish action (owner vs. non‑owner)
    """

    # ------------------------------------------------------------------ helpers
    def _model_payload(self):
        """
        Return course_data *without* the FK IDs so we can supply model
        instances when calling Course.objects.create().
        """
        return {k: v for k, v in self.course_data.items()
                if k not in ("category", "instructor")}

    # ------------------------------------------------------------------ fixtures
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="pass123",
            role="teacher",
        )
        self.other_teacher = User.objects.create_user(
            username="other_teacher",
            email="other_teacher@example.com",
            password="pass123",
            role="teacher",
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        self.category = Category.objects.create(title="Programming")

        # API‑facing payload: use IDs for FKs
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

    # --------------------------------------------------------------- test cases
    def test_teacher_can_create_free_course(self):
        self.client.force_authenticate(user=self.teacher)
        resp = self.client.post(reverse("course-list"), self.course_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_teacher_can_update_own_course(self):
        self.client.force_authenticate(user=self.teacher)
        course = Course.objects.create(
            **self._model_payload(),
            category=self.category,
            instructor=self.teacher,
        )
        url = reverse("course-detail", args=[course.id])
        resp = self.client.patch(url, {"title": "Updated Title"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.title, "Updated Title")

    def test_teacher_cannot_update_others_course(self):
        self.client.force_authenticate(user=self.other_teacher)
        course = Course.objects.create(
            **self._model_payload(),
            category=self.category,
            instructor=self.teacher,
        )
        url = reverse("course-detail", args=[course.id])
        resp = self.client.patch(url, {"title": "Hack attempt"})
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_course(self):
        self.client.force_authenticate(user=self.admin)
        course = Course.objects.create(
            **self._model_payload(),
            category=self.category,
            instructor=self.teacher,
        )
        url = reverse("course-detail", args=[course.id])
        resp = self.client.patch(url, {"title": "Admin Edit"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_publish_sets_course_active(self):
        self.client.force_authenticate(user=self.teacher)
        course = Course.objects.create(
            **self._model_payload(),
            is_active=False,
            category=self.category,
            instructor=self.teacher,
        )
        url = reverse("course-publish", args=[course.id])
        resp = self.client.patch(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertTrue(course.is_active)

    def test_publish_denied_for_non_owner(self):
        self.client.force_authenticate(user=self.other_teacher)
        course = Course.objects.create(
            **self._model_payload(),
            is_active=False,
            category=self.category,
            instructor=self.teacher,
        )
        url = reverse("course-publish", args=[course.id])
        resp = self.client.patch(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
