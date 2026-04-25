from django.conf import settings
from django.db import models

from apps.sources.models import SourceExcerpt
from apps.workspaces.models import Workspace


class BriefingRequest(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PROCESSING = "processing", "Processing"
        READY = "ready", "Ready"
        NEEDS_REVIEW = "needs_review", "Needs Review"

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="briefing_requests",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="briefing_requests",
    )
    title = models.CharField(max_length=200)
    question = models.TextField()
    audience = models.CharField(max_length=120, blank=True, default="")
    goal = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        indexes = [
            models.Index(fields=("workspace", "status")),
            models.Index(fields=("workspace", "updated_at")),
        ]

    def __str__(self) -> str:
        return self.title


class BriefingAnswer(models.Model):
    class Status(models.TextChoices):
        GENERATED = "generated", "Generated"
        REVIEWED = "reviewed", "Reviewed"
        SUPERSEDED = "superseded", "Superseded"

    class ConfidenceBand(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    request = models.ForeignKey(
        BriefingRequest,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_briefing_answers",
    )
    provider = models.CharField(max_length=50, default="stub")
    model_name = models.CharField(max_length=100, blank=True, default="")
    answer_text = models.TextField()
    confidence_band = models.CharField(
        max_length=20,
        choices=ConfidenceBand.choices,
        default=ConfidenceBand.MEDIUM,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.GENERATED,
    )
    generation_notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("request", "status")),
            models.Index(fields=("request", "created_at")),
        ]

    def __str__(self) -> str:
        return f"Answer for {self.request.title}"


class AnswerCitation(models.Model):
    answer = models.ForeignKey(
        BriefingAnswer,
        on_delete=models.CASCADE,
        related_name="citations",
    )
    excerpt = models.ForeignKey(
        SourceExcerpt,
        on_delete=models.CASCADE,
        related_name="answer_citations",
    )
    relevance_rank = models.PositiveIntegerField(default=1)
    rationale = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        ordering = ("relevance_rank", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("answer", "excerpt"),
                name="unique_citation_per_answer_excerpt",
            )
        ]

    def __str__(self) -> str:
        return f"{self.answer_id} -> {self.excerpt_id}"
