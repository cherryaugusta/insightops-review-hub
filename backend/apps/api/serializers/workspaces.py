from rest_framework import serializers

from apps.evaluations.models import EvaluationRun, ReviewDecision
from apps.workspaces.models import Workspace


class WorkspaceListSerializer(serializers.ModelSerializer):
    source_document_count = serializers.SerializerMethodField()
    briefing_request_count = serializers.SerializerMethodField()
    last_activity_at = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Workspace
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "status",
            "source_document_count",
            "briefing_request_count",
            "last_activity_at",
            "created_at",
            "updated_at",
        )

    def get_source_document_count(self, obj: Workspace) -> int:
        return obj.source_documents.count()

    def get_briefing_request_count(self, obj: Workspace) -> int:
        return obj.briefing_requests.count()


class WorkspaceDetailSerializer(WorkspaceListSerializer):
    evaluation_run_count = serializers.SerializerMethodField()
    latest_review_decision = serializers.SerializerMethodField()

    class Meta(WorkspaceListSerializer.Meta):
        fields = WorkspaceListSerializer.Meta.fields + (
            "evaluation_run_count",
            "latest_review_decision",
        )

    def get_evaluation_run_count(self, obj: Workspace) -> int:
        return EvaluationRun.objects.filter(answer__request__workspace=obj).count()

    def get_latest_review_decision(self, obj: Workspace):
        latest = (
            ReviewDecision.objects.filter(answer__request__workspace=obj)
            .order_by("-created_at")
            .first()
        )
        return latest.decision if latest else None


class WorkspaceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "status",
        )
        read_only_fields = ("id",)

    def validate_slug(self, value: str) -> str:
        return value.strip().lower()
