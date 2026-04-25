from rest_framework import serializers

from apps.audit.models import AuditEvent


class AuditEventSerializer(serializers.ModelSerializer):
    actor_display_name = serializers.SerializerMethodField()

    class Meta:
        model = AuditEvent
        fields = (
            "id",
            "actor_display_name",
            "entity_type",
            "entity_id",
            "action",
            "metadata",
            "created_at",
        )

    def get_actor_display_name(self, obj: AuditEvent):
        return obj.actor.display_name if obj.actor else None
