from django.conf import settings
from django.db import models

from apps.workspaces.models import Workspace


class AuditEvent(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events",
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="audit_events",
    )
    entity_type = models.CharField(max_length=50)
    entity_id = models.PositiveIntegerField()
    action = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("workspace", "created_at")),
            models.Index(fields=("entity_type", "entity_id")),
            models.Index(fields=("action", "created_at")),
        ]

    def __str__(self) -> str:
        return f"{self.action} on {self.entity_type}:{self.entity_id}"
