from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
User = get_user_model()

# ---------------------------------------------------------------------------
class Category(models.Model):
    title      = models.CharField(max_length=255, unique=True)
    is_active  = models.BooleanField(default=True)
    slug       = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title

    # Auto-generate slug the first time (and if it stays blank)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------
class Course(models.Model):

    # ─── Enumerations ───────────────────────────────────────────────────────
    class CourseLevel(models.TextChoices):
        BEGINNER     = "beginner",     _("Beginner")
        INTERMEDIATE = "intermediate", _("Intermediate")
        ADVANCED     = "advanced",     _("Advanced")

    class CourseType(models.TextChoices):
        FREE = "free", _("Free")
        PAID = "paid", _("Paid")

    # ─── Core fields ────────────────────────────────────────────────────────
    title       = models.CharField(max_length=255)
    description = models.TextField()
    banner = models.ImageField(upload_to="course_banners/", null=True, blank=True)


    price       = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Price in your default currency"),
    )
    level       = models.CharField(
        max_length=20,
        choices=CourseLevel.choices,
        default=CourseLevel.BEGINNER,
        db_index=True,
    )
    type        = models.CharField(
        max_length=20,
        choices=CourseType.choices,
        default=CourseType.FREE,
        db_index=True,
    )

    tags            = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    prerequisites   = models.TextField(blank=True, null=True)
    duration        = models.PositiveSmallIntegerField(
        default=0,
        help_text=_("Approximate total duration in hours"),
    )
    syllabus        = models.TextField(blank=True, null=True, help_text=_("Course syllabus or outline"))
    feedback        = models.TextField(blank=True, null=True, help_text=_("Feedback or reviews from students"))
    is_active       = models.BooleanField(default=True)

    # ─── Relations ──────────────────────────────────────────────────────────
    category   = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="courses",
    )
    instructor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={"role": "teacher"},
        related_name="courses_taught",
    )

    # ─── Timestamps ─────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ─── Meta & indexes ─────────────────────────────────────────────────────
    class Meta:
        ordering = ("-created_at",)
        indexes  = [
            models.Index(fields=("type",)),
            models.Index(fields=("level",)),
            models.Index(fields=("category", "is_active")),
        ]
        unique_together = ("title", "instructor")      # optional: avoid dup titles per teacher

    # ─── Validation rules ───────────────────────────────────────────────────
    def clean(self):
        """
        Enforce business rules:
        - free course ⇒ price must be 0
        - paid course ⇒ price must be > 0
        """
        super().clean()

        if self.type == self.CourseType.FREE and self.price > 0:
            raise ValidationError(_("Free courses must have price = 0."))
        if self.type == self.CourseType.PAID and self.price <= 0:
            raise ValidationError(_("Paid courses must have a positive price."))

    # ─── Convenience helpers ───────────────────────────────────────────────
    @property
    def is_paid(self) -> bool:
        """Return True if the course requires payment."""
        return self.type == self.CourseType.PAID

    def __str__(self) -> str:
        return self.title