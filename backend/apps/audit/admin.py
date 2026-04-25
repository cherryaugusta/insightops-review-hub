from django.contrib import admin

from apps.audit.models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("action", "entity_type", "entity_id", "workspace", "actor", "created_at")
    search_fields = ("action", "entity_type", "workspace__title", "actor__username")
    list_filter = ("entity_type", "action", "created_at")
    autocomplete_fields = ("actor", "workspace")
    ordering = ("-created_at",)
