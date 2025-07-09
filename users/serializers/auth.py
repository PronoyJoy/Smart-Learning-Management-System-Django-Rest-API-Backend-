
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'role', 'phone_number')
        extra_kwargs = {
            'role': {'required': False},
            'phone_number': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        # create_user will hash the password 
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            role=validated_data.get('role', User.Role.STUDENT), #default to STUDENT if not provided
            phone_number=validated_data.get('phone_number')
        )
        return user



# # RegisterSerializer
# # LoginSerializer
# # JWT refresh / response serializers (optional)

# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError as DjangoValidationError

# User = get_user_model()

# class RegisterSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True,required=True, min_length=8, style={'input_type': 'password'})
#     password2 = serializers.CharField(write_only=True,required= True, min_length=8, style={'input_type': 'password'})

#     class Meta:
#         fields = ['id', 'username', 'email', 'role', 'password', 'password2']
#         model = User
#         extra_kwargs = {
#             'role': {'required': True, 'default': User.Role.STUDENT},
#         }
    
#     def validate(self, attrs):
#          # attrs = {'email': ..., 'password': ..., 'role': ...}
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError("Passwords do not match.")
#         return attrs
    
#     def email_exists(self, email):
#         """Check if the email already exists in the database."""
#         return User.objects.filter(email=email).exists()

#     def validate_email(self, value):
#         """Validate that the email is not already registered."""
#         if self.email_exists(value):
#             raise serializers.ValidationError("Email is already registered.")
#         return value
    
#     def create(self, validated_data):
#         """Create user with hashed password, remove extra field."""
#         validated_data.pop('password2') #remove extra field
#         # Ensure the password is hashed before saving
#         try:
#             user = User.objects.create_user(**validated_data) #.create user will hash the password,** for unpacking the dict

#         except DjangoValidationError as e:
#             raise serializers.ValidationError(e.message_dict)
#         return user

#   When you call:
# serializer.is_valid()
# DRF does this:
# Converts the input data (request.data) into Python-native types.

# Runs field validation (required, max_length, etc.) — based on:

# the serializer fields

# model constraints (if using ModelSerializer)

# any validate_<field>() you wrote

# Then calls your custom validate(self, data) method — exactly as you wrote it.