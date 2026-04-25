from django.db import models

from apps.workspaces.models import Workspace


class SourceDocument(models.Model):
    class SourceType(models.TextChoices):
        NOTE = "note", "Note"
        REPORT = "report", "Report"
        URL = "url", "URL"
        TRANSCRIPT = "transcript", "Transcript"
        RESEARCH = "research", "Research"
        MANUAL = "manual", "Manual"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        READY = "ready", "Ready"
        ARCHIVED = "archived", "Archived"

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="source_documents",
    )
    title = models.CharField(max_length=255)
    source_type = models.CharField(
        max_length=20,
        choices=SourceType.choices,
        default=SourceType.NOTE,
    )
    filename = models.CharField(max_length=255, blank=True, default="")
    source_url = models.URLField(blank=True, default="")
    raw_text = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.READY,
    )
    excerpt_count = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        indexes = [
            models.Index(fields=("workspace", "status")),
            models.Index(fields=("workspace", "source_type")),
            models.Index(fields=("workspace", "updated_at")),
        ]

    def __str__(self) -> str:
        return self.title


class SourceExcerpt(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="source_excerpts",
    )
    document = models.ForeignKey(
        SourceDocument,
        on_delete=models.CASCADE,
        related_name="excerpts",
    )
    order_index = models.PositiveIntegerField()
    text = models.TextField()
    token_count = models.PositiveIntegerField(default=0)
    char_start = models.PositiveIntegerField(default=0)
    char_end = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("document_id", "order_index")
        constraints = [
            models.UniqueConstraint(
                fields=("document", "order_index"),
                name="unique_excerpt_order_per_document",
            )
        ]
        indexes = [
            models.Index(fields=("workspace", "document")),
            models.Index(fields=("document", "order_index")),
        ]

    def __str__(self) -> str:
        return f"{self.document.title} #{self.order_index}"
