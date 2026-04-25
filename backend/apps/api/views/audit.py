from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.api.selectors import workspace_audit_events
from apps.api.serializers import AuditEventSerializer


class AuditEventListAPIView(generics.ListAPIView):
    serializer_class = AuditEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return workspace_audit_events(
            user=self.request.user,
            workspace_id=self.kwargs["workspace_id"],
        )
