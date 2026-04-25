from apps.audit.models import AuditEvent
from apps.briefings.models import BriefingRequest
from apps.evaluations.models import EvaluationRun
from apps.sources.models import SourceDocument, SourceExcerpt
from apps.workspaces.models import Workspace


def user_workspaces(user):
    return Workspace.objects.filter(owner=user).order_by("title")


def workspace_sources(user, workspace_id):
    return (
        SourceDocument.objects.filter(workspace_id=workspace_id, workspace__owner=user)
        .order_by("-updated_at")
    )


def source_excerpts(user, source_id):
    return (
        SourceExcerpt.objects.filter(document_id=source_id, workspace__owner=user)
        .select_related("document", "workspace")
        .order_by("order_index")
    )


def workspace_briefings(user, workspace_id):
    return (
        BriefingRequest.objects.filter(workspace_id=workspace_id, workspace__owner=user)
        .prefetch_related("answers__evaluation_runs", "answers__review_decisions")
        .order_by("-updated_at")
    )


def briefing_detail(user, briefing_id):
    return (
        BriefingRequest.objects.filter(workspace__owner=user, id=briefing_id)
        .prefetch_related(
            "answers__citations__excerpt__document",
            "answers__evaluation_runs",
            "answers__review_decisions",
        )
        .first()
    )


def evaluation_detail(user, evaluation_id):
    return (
        EvaluationRun.objects.filter(answer__request__workspace__owner=user, id=evaluation_id)
        .select_related("answer", "answer__request", "answer__request__workspace")
        .first()
    )


def workspace_audit_events(user, workspace_id):
    return (
        AuditEvent.objects.filter(workspace_id=workspace_id, workspace__owner=user)
        .select_related("actor")
        .order_by("-created_at")
    )
