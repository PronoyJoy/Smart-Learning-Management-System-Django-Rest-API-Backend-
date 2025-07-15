from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

# Create your models here.

# ── Custom User Manager ───────────────────────────────────────
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)  # ✅ FIX HERE

        if not extra_fields.get("is_staff") or not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_staff=True and is_superuser=True")

        if extra_fields.get("role") != User.Role.ADMIN:
            raise ValueError("Superuser must have role='admin'")

        return self.create_user(email, password, **extra_fields)

    #object methods
    def get_by_natural_key(self, email):
        return self.get(email=email)
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
    def all_users(self):
        """Return all users, including inactive ones."""
        return super().get_queryset()
    
    def get_user_by_email(self, email):
        """Return a user by their email address."""
        return self.get(email=email)
    
    def get_user_by_id(self, user_id):
        """Return a user by their ID."""
        return self.get(id=user_id)
    
    def get_users_by_role(self, role):
        """Return users filtered by their role."""
        return self.filter(role=role)
    

    
# ── Custom User Model ─────────────────────────────────────────
class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", _("Student")
        TEACHER = "teacher", _("Teacher")
        ADMIN = "admin", _("Admin")

    email = models.EmailField(unique=True)  # ✅ Use EmailField for email
    username = models.CharField(max_length=150, unique=True)  # ✅ Add this
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be in the format: '+8801234567890'. Up to 15 digits allowed."
            )
        ]
    )

    USERNAME_FIELD = 'email'   # ✅ Still using email for login
    REQUIRED_FIELDS = ['username']  # ✅ This is required for `createsuperuser`

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    