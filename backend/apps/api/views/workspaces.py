from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.api.permissions import IsAuthenticatedAndWorkspaceOwner
from apps.api.serializers import (
    WorkspaceDetailSerializer,
    WorkspaceListSerializer,
    WorkspaceWriteSerializer,
)
from apps.api.services.audit import create_audit_event
from apps.workspaces.models import Workspace


class WorkspaceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthenticatedAndWorkspaceOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "slug"]

    def get_queryset(self):
        queryset = Workspace.objects.filter(owner=self.request.user).order_by("title")
        status = self.request.query_params.get("status", "").strip()
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return WorkspaceListSerializer
        if self.action == "retrieve":
            return WorkspaceDetailSerializer
        return WorkspaceWriteSerializer

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        create_audit_event(
            actor=self.request.user,
            workspace=instance,
            entity_type="workspace",
            entity_id=instance.id,
            action="workspace.created",
            metadata={"title": instance.title, "status": instance.status},
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        create_audit_event(
            actor=self.request.user,
            workspace=instance,
            entity_type="workspace",
            entity_id=instance.id,
            action="workspace.updated",
            metadata={"title": instance.title, "status": instance.status},
        )

    def perform_destroy(self, instance):
        create_audit_event(
            actor=self.request.user,
            workspace=instance,
            entity_type="workspace",
            entity_id=instance.id,
            action="workspace.deleted",
            metadata={"title": instance.title},
        )
        instance.delete()
