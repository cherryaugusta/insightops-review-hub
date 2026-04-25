from rest_framework import serializers

from apps.briefings.models import AnswerCitation, BriefingAnswer, BriefingRequest


class AnswerCitationSerializer(serializers.ModelSerializer):
    excerpt_id = serializers.IntegerField(source="excerpt.id", read_only=True)
    excerpt_text = serializers.CharField(source="excerpt.text", read_only=True)
    document_title = serializers.CharField(source="excerpt.document.title", read_only=True)

    class Meta:
        model = AnswerCitation
        fields = (
            "id",
            "excerpt_id",
            "relevance_rank",
            "rationale",
            "excerpt_text",
            "document_title",
        )


class BriefingAnswerSerializer(serializers.ModelSerializer):
    citations = AnswerCitationSerializer(many=True, read_only=True)
    latest_evaluation = serializers.SerializerMethodField()
    latest_review_decision = serializers.SerializerMethodField()

    class Meta:
        model = BriefingAnswer
        fields = (
            "id",
            "provider",
            "model_name",
            "answer_text",
            "confidence_band",
            "status",
            "generation_notes",
            "created_at",
            "citations",
            "latest_evaluation",
            "latest_review_decision",
        )

    def get_latest_evaluation(self, obj: BriefingAnswer):
        evaluation = obj.evaluation_runs.order_by("-created_at").first()
        if not evaluation:
            return None
        return {
            "id": evaluation.id,
            "groundedness_score": str(evaluation.groundedness_score),
            "citation_coverage_score": str(evaluation.citation_coverage_score),
            "completeness_score": str(evaluation.completeness_score),
            "overall_score": str(evaluation.overall_score),
            "verdict": evaluation.verdict,
            "notes": evaluation.notes,
        }

    def get_latest_review_decision(self, obj: BriefingAnswer):
        decision = obj.review_decisions.order_by("-created_at").first()
        if not decision:
            return None
        return {
            "id": decision.id,
            "decision": decision.decision,
            "comment": decision.comment,
        }


class BriefingRequestListSerializer(serializers.ModelSerializer):
    latest_answer_id = serializers.SerializerMethodField()
    latest_evaluation_verdict = serializers.SerializerMethodField()

    class Meta:
        model = BriefingRequest
        fields = (
            "id",
            "title",
            "question",
            "audience",
            "goal",
            "status",
            "latest_answer_id",
            "latest_evaluation_verdict",
            "created_at",
            "updated_at",
        )

    def get_latest_answer_id(self, obj: BriefingRequest):
        latest = obj.answers.order_by("-created_at").first()
        return latest.id if latest else None

    def get_latest_evaluation_verdict(self, obj: BriefingRequest):
        latest_answer = obj.answers.order_by("-created_at").first()
        if not latest_answer:
            return None
        evaluation = latest_answer.evaluation_runs.order_by("-created_at").first()
        return evaluation.verdict if evaluation else None


class BriefingRequestDetailSerializer(serializers.ModelSerializer):
    answers = BriefingAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = BriefingRequest
        fields = (
            "id",
            "title",
            "question",
            "audience",
            "goal",
            "status",
            "answers",
            "created_at",
            "updated_at",
        )


class BriefingRequestWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BriefingRequest
        fields = (
            "id",
            "title",
            "question",
            "audience",
            "goal",
            "status",
        )
        read_only_fields = ("id",)

    def validate_title(self, value: str) -> str:
        value = value.strip()
        if len(value) < 5:
            raise serializers.ValidationError("Title must contain at least 5 characters.")
        return value

    def validate_question(self, value: str) -> str:
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError("Question must contain at least 10 characters.")
        return value
