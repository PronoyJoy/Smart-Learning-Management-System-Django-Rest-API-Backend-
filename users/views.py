from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers.auth import RegisterSerializer

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RegisterAPIView(generics.CreateAPIView):
#     """
#     API view to register a new user.
#     """
#     serializer_class = RegisterSerializer
#     permission_classes = [permissions.AllowAny]
#     queryset = User.objects.all()


# from django.shortcuts import render
# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework import status
# from users.serializers.auth import RegisterSerializer
# from django.contrib.auth import get_user_model

# User = get_user_model()

# # Create your views here.


