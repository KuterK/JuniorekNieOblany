# Generated manually for the initial MVP schema.

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Analysis",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("code", models.TextField()),
                ("title", models.CharField(blank=True, max_length=200)),
                ("language", models.CharField(blank=True, db_index=True, max_length=50)),
                ("short_description", models.TextField(blank=True)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("summary", models.TextField(blank=True)),
                ("explanation", models.TextField(blank=True)),
                ("concepts", models.TextField(blank=True)),
                ("pitfalls", models.TextField(blank=True)),
                ("junior_explanation", models.TextField(blank=True)),
                ("schema_version", models.PositiveSmallIntegerField(default=1)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Oczekuje"),
                            ("processing", "Analizowanie"),
                            ("completed", "Gotowa"),
                            ("failed", "Błąd"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "rating",
                    models.CharField(
                        blank=True,
                        choices=[("helpful", "Pomocna"), ("unhelpful", "Niepomocna")],
                        max_length=20,
                    ),
                ),
                ("error_message", models.CharField(blank=True, max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analyses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(
                        fields=["owner", "-created_at"],
                        name="analyses_an_owner_i_f26a89_idx",
                    ),
                    models.Index(
                        fields=["owner", "language"],
                        name="analyses_an_owner_i_f881f3_idx",
                    ),
                ],
            },
        )
    ]
