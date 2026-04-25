from rest_framework import generics, response, status, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.api.serializers import (
    BriefingRequestDetailSerializer,
    BriefingRequestListSerializer,
    BriefingRequestWriteSerializer,
    ReviewDecisionSerializer,
    ReviewDecisionWriteSerializer,
)
from apps.api.services.answer_generation import generate_answer_for_briefing
from apps.api.services.audit import create_audit_event
from apps.api.services.evaluations import evaluate_answer
from apps.briefings.models import BriefingAnswer, BriefingRequest
from apps.evaluations.models import ReviewDecision
from apps.workspaces.models import Workspace


class BriefingRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        queryset = BriefingRequest.objects.filter(
            workspace_id=workspace_id,
            workspace__owner=self.request.user,
        ).order_by("-updated_at")
        status_value = self.request.query_params.get("status", "").strip()
        if status_value:
            queryset = queryset.filter(status=status_value)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BriefingRequestListSerializer
        if self.action == "retrieve":
            return BriefingRequestDetailSerializer
        return BriefingRequestWriteSerializer

    def perform_create(self, serializer):
        workspace = Workspace.objects.get(
            id=self.kwargs["workspace_id"],
            owner=self.request.user,
        )
        instance = serializer.save(
            workspace=workspace,
            created_by=self.request.user,
        )
        create_audit_event(
            actor=self.request.user,
            workspace=workspace,
            entity_type="briefing_request",
            entity_id=instance.id,
            action="briefing_request.created",
            metadata={"title": instance.title},
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        create_audit_event(
            actor=self.request.user,
            workspace=instance.workspace,
            entity_type="briefing_request",
            entity_id=instance.id,
            action="briefing_request.updated",
            metadata={"title": instance.title, "status": instance.status},
        )

    def perform_destroy(self, instance):
        create_audit_event(
            actor=self.request.user,
            workspace=instance.workspace,
            entity_type="briefing_request",
            entity_id=instance.id,
            action="briefing_request.deleted",
            metadata={"title": instance.title},
        )
        instance.delete()


class GenerateAnswerAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, briefing_id):
        briefing = BriefingRequest.objects.get(
            id=briefing_id,
            workspace__owner=request.user,
        )

        briefing.status = BriefingRequest.Status.PROCESSING
        briefing.save(update_fields=["status", "updated_at"])

        answer = generate_answer_for_briefing(
            request_obj=briefing,
            user=request.user,
        )
        evaluation = evaluate_answer(answer)

        briefing.status = (
            BriefingRequest.Status.READY
            if evaluation.verdict == "pass"
            else BriefingRequest.Status.NEEDS_REVIEW
        )
        briefing.save(update_fields=["status", "updated_at"])

        create_audit_event(
            actor=request.user,
            workspace=briefing.workspace,
            entity_type="briefing_answer",
            entity_id=answer.id,
            action="briefing_answer.generated",
            metadata={"provider": answer.provider, "model_name": answer.model_name},
        )
        create_audit_event(
            actor=request.user,
            workspace=briefing.workspace,
            entity_type="evaluation_run",
            entity_id=evaluation.id,
            action="evaluation_run.created",
            metadata={"verdict": evaluation.verdict, "overall_score": str(evaluation.overall_score)},
        )

        return response.Response(
            {
                "briefing_request_id": briefing.id,
                "answer_id": answer.id,
                "evaluation_run_id": evaluation.id,
                "status": briefing.status,
            },
            status=status.HTTP_200_OK,
        )


class AnswerReviewDecisionCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewDecisionWriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        answer = BriefingAnswer.objects.get(
            id=self.kwargs["answer_id"],
            request__workspace__owner=request.user,
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        decision = ReviewDecision.objects.create(
            answer=answer,
            reviewer=request.user,
            **serializer.validated_data,
        )

        if decision.decision == ReviewDecision.Decision.APPROVED:
            answer.status = BriefingAnswer.Status.REVIEWED
            answer.save(update_fields=["status"])

        create_audit_event(
            actor=request.user,
            workspace=answer.request.workspace,
            entity_type="review_decision",
            entity_id=decision.id,
            action="review_decision.created",
            metadata={"decision": decision.decision},
        )

        output = ReviewDecisionSerializer(decision)
        return response.Response(output.data, status=status.HTTP_201_CREATED)
