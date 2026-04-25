from django.contrib import admin

from apps.evaluations.models import EvaluationRun, ReviewDecision


@admin.register(EvaluationRun)
class EvaluationRunAdmin(admin.ModelAdmin):
    list_display = ("answer", "verdict", "overall_score", "created_at")
    search_fields = ("answer__request__title", "notes")
    list_filter = ("verdict", "evaluator_type", "created_at")
    autocomplete_fields = ("answer",)
    ordering = ("-created_at",)


@admin.register(ReviewDecision)
class ReviewDecisionAdmin(admin.ModelAdmin):
    list_display = ("answer", "reviewer", "decision", "created_at")
    search_fields = ("answer__request__title", "reviewer__username", "comment")
    list_filter = ("decision", "created_at")
    autocomplete_fields = ("answer", "reviewer")
    ordering = ("-created_at",)
