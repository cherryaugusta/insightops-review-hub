from apps.audit.models import AuditEvent
from apps.workspaces.models import Workspace


def create_audit_event(*, actor, workspace: Workspace, entity_type: str, entity_id: int, action: str, metadata: dict | None = None):
    return AuditEvent.objects.create(
        actor=actor,
        workspace=workspace,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        metadata=metadata or {},
    )
