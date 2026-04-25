from django.conf import settings
from django.db import models


class Workspace(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workspaces",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    description = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("title",)
        constraints = [
            models.UniqueConstraint(
                fields=("owner", "slug"),
                name="unique_workspace_slug_per_owner",
            )
        ]
        indexes = [
            models.Index(fields=("owner", "status")),
            models.Index(fields=("owner", "updated_at")),
        ]

    def __str__(self) -> str:
        return self.title
