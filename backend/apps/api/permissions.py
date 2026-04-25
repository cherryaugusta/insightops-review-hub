from rest_framework.permissions import BasePermission

from apps.audit.models import AuditEvent
from apps.briefings.models import BriefingAnswer, BriefingRequest
from apps.evaluations.models import EvaluationRun
from apps.sources.models import SourceDocument, SourceExcerpt
from apps.workspaces.models import Workspace


class IsAuthenticatedAndWorkspaceOwner(BasePermission):
    message = "You do not have permission to access this resource."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        workspace = self._resolve_workspace(obj)
        if not workspace:
            return False
        return workspace.owner_id == request.user.id

    def _resolve_workspace(self, obj):
        if isinstance(obj, Workspace):
            return obj
        if isinstance(obj, SourceDocument):
            return obj.workspace
        if isinstance(obj, SourceExcerpt):
            return obj.workspace
        if isinstance(obj, BriefingRequest):
            return obj.workspace
        if isinstance(obj, BriefingAnswer):
            return obj.request.workspace
        if isinstance(obj, EvaluationRun):
            return obj.answer.request.workspace
        if isinstance(obj, AuditEvent):
            return obj.workspace
        return None


class IsWorkspaceOwnerFromURL(BasePermission):
    message = "Workspace not found or not accessible."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        workspace_id = view.kwargs.get("workspace_id")
        if not workspace_id:
            return False
        return Workspace.objects.filter(
            id=workspace_id,
            owner=request.user,
        ).exists()
