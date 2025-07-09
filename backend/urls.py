from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
import users

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

]