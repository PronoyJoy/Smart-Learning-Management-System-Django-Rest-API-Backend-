from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
import users

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from course.views import CourseViewSet,CategoryViewSet
from lessons.views import LessonViewSet


# ------------------------------
# 📦 Main API Router
# ------------------------------
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

# ------------------------------
# 📦 Nested Lessons under Courses
# ------------------------------
course_router = NestedDefaultRouter(router, r'courses', lookup='course')
course_router.register(r'lessons', LessonViewSet, basename='course-lessons')
router.register(r"categories", CategoryViewSet, basename="category")
#path('courses/<int:course_pk>/lessons/', ...)



urlpatterns = [
    path('admin/', admin.site.urls),

     # ✅ JWT endpoints
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login will get token here
    # path('api/logout/', TokenDestroyView.as_view(), name='token_destroy'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),    # verify

    # Optional for browsable API — safe to remove if not needed
    path('api-auth/', include('rest_framework.urls')),

    #register
    path('api/users/', include('users.urls')),


    # 📚 Course & Lesson APIs
    path('api/', include(router.urls)),         # /api/courses/
    path('api/', include(course_router.urls)),  # /api/courses/<id>/lessons/

]