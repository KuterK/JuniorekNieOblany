import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse


class Analysis(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Oczekuje"
        PROCESSING = "processing", "Analizowanie"
        COMPLETED = "completed", "Gotowa"
        FAILED = "failed", "Błąd"

    class Rating(models.TextChoices):
        HELPFUL = "helpful", "Pomocna"
        UNHELPFUL = "unhelpful", "Niepomocna"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="analyses"
    )
    code = models.TextField()
    title = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=50, blank=True, db_index=True)
    short_description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    summary = models.TextField(blank=True)
    explanation = models.TextField(blank=True)
    concepts = models.TextField(blank=True)
    pitfalls = models.TextField(blank=True)
    junior_explanation = models.TextField(blank=True)
    schema_version = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    rating = models.CharField(max_length=20, choices=Rating.choices, blank=True)
    error_message = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "-created_at"]),
            models.Index(fields=["owner", "language"]),
        ]

    def __str__(self) -> str:
        return self.title or f"Analiza {self.id}"

    def get_absolute_url(self) -> str:
        return reverse("analysis-detail", kwargs={"pk": self.pk})
