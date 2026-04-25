from rest_framework import generics, response, status, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.api.serializers import (
    SourceDocumentDetailSerializer,
    SourceDocumentListSerializer,
    SourceDocumentWriteSerializer,
    SourceExcerptSerializer,
)
from apps.api.services.audit import create_audit_event
from apps.api.services.excerpts import generate_excerpts_for_document
from apps.api.selectors import source_excerpts
from apps.sources.models import SourceDocument
from apps.workspaces.models import Workspace


class SourceDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        return SourceDocument.objects.filter(
            workspace_id=workspace_id,
            workspace__owner=self.request.user,
        ).order_by("-updated_at")

    def get_serializer_class(self):
        if self.action == "list":
            return SourceDocumentListSerializer
        if self.action == "retrieve":
            return SourceDocumentDetailSerializer
        return SourceDocumentWriteSerializer

    def perform_create(self, serializer):
        workspace = Workspace.objects.get(
            id=self.kwargs["workspace_id"],
            owner=self.request.user,
        )
        instance = serializer.save(workspace=workspace)
        create_audit_event(
            actor=self.request.user,
            workspace=workspace,
            entity_type="source_document",
            entity_id=instance.id,
            action="source_document.created",
            metadata={"title": instance.title, "source_type": instance.source_type},
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        create_audit_event(
            actor=self.request.user,
            workspace=instance.workspace,
            entity_type="source_document",
            entity_id=instance.id,
            action="source_document.updated",
            metadata={"title": instance.title, "source_type": instance.source_type},
        )

    def perform_destroy(self, instance):
        create_audit_event(
            actor=self.request.user,
            workspace=instance.workspace,
            entity_type="source_document",
            entity_id=instance.id,
            action="source_document.deleted",
            metadata={"title": instance.title},
        )
        instance.delete()


class SourceExcerptListAPIView(generics.ListAPIView):
    serializer_class = SourceExcerptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return source_excerpts(
            user=self.request.user,
            source_id=self.kwargs["source_id"],
        )


class GenerateExcerptsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, source_id):
        document = SourceDocument.objects.get(
            id=source_id,
            workspace__owner=request.user,
        )
        created_count = generate_excerpts_for_document(document)
        create_audit_event(
            actor=request.user,
            workspace=document.workspace,
            entity_type="source_document",
            entity_id=document.id,
            action="source_document.excerpts_generated",
            metadata={"created_excerpt_count": created_count},
        )
        return response.Response(
            {
                "source_document_id": document.id,
                "created_excerpt_count": created_count,
                "status": document.status,
            },
            status=status.HTTP_200_OK,
        )
