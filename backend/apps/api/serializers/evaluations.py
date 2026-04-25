from rest_framework import serializers

from apps.evaluations.models import EvaluationRun, ReviewDecision


class EvaluationRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationRun
        fields = (
            "id",
            "answer_id",
            "evaluator_type",
            "groundedness_score",
            "citation_coverage_score",
            "completeness_score",
            "overall_score",
            "verdict",
            "notes",
            "created_at",
        )


class ReviewDecisionSerializer(serializers.ModelSerializer):
    reviewer_id = serializers.IntegerField(source="reviewer.id", read_only=True)

    class Meta:
        model = ReviewDecision
        fields = (
            "id",
            "answer_id",
            "reviewer_id",
            "decision",
            "comment",
            "created_at",
        )


class ReviewDecisionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewDecision
        fields = (
            "decision",
            "comment",
        )

    def validate_comment(self, value: str) -> str:
        return value.strip()
