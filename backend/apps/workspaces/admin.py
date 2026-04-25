from django.contrib import admin

from apps.workspaces.models import Workspace


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "updated_at")
    search_fields = ("title", "slug", "description", "owner__username", "owner__email")
    list_filter = ("status", "created_at", "updated_at")
    autocomplete_fields = ("owner",)
    ordering = ("title",)
