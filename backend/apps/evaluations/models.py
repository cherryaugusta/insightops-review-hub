from django.conf import settings
from django.db import models

from apps.briefings.models import BriefingAnswer


class EvaluationRun(models.Model):
    class Verdict(models.TextChoices):
        PASS = "pass", "Pass"
        REVIEW = "review", "Review"
        FAIL = "fail", "Fail"

    answer = models.ForeignKey(
        BriefingAnswer,
        on_delete=models.CASCADE,
        related_name="evaluation_runs",
    )
    evaluator_type = models.CharField(max_length=50, default="heuristic")
    groundedness_score = models.DecimalField(max_digits=5, decimal_places=2)
    citation_coverage_score = models.DecimalField(max_digits=5, decimal_places=2)
    completeness_score = models.DecimalField(max_digits=5, decimal_places=2)
    overall_score = models.DecimalField(max_digits=5, decimal_places=2)
    verdict = models.CharField(
        max_length=20,
        choices=Verdict.choices,
        default=Verdict.REVIEW,
    )
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("answer", "created_at")),
            models.Index(fields=("verdict", "created_at")),
        ]

    def __str__(self) -> str:
        return f"Evaluation for answer {self.answer_id}"


class ReviewDecision(models.Model):
    class Decision(models.TextChoices):
        APPROVED = "approved", "Approved"
        CHANGES_REQUESTED = "changes_requested", "Changes Requested"
        REJECTED = "rejected", "Rejected"

    answer = models.ForeignKey(
        BriefingAnswer,
        on_delete=models.CASCADE,
        related_name="review_decisions",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_decisions",
    )
    decision = models.CharField(
        max_length=30,
        choices=Decision.choices,
    )
    comment = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("answer", "created_at")),
            models.Index(fields=("reviewer", "created_at")),
        ]

    def __str__(self) -> str:
        return f"{self.get_decision_display()} by {self.reviewer}"
