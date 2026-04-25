from django.contrib import admin

from apps.sources.models import SourceDocument, SourceExcerpt


class SourceExcerptInline(admin.TabularInline):
    model = SourceExcerpt
    extra = 0
    readonly_fields = ("order_index", "token_count", "char_start", "char_end")


@admin.register(SourceDocument)
class SourceDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "workspace", "source_type", "status", "excerpt_count", "updated_at")
    search_fields = ("title", "filename", "source_url", "workspace__title", "workspace__owner__username")
    list_filter = ("source_type", "status", "created_at", "updated_at")
    autocomplete_fields = ("workspace",)
    inlines = [SourceExcerptInline]
    ordering = ("-updated_at",)


@admin.register(SourceExcerpt)
class SourceExcerptAdmin(admin.ModelAdmin):
    list_display = ("document", "order_index", "token_count")
    search_fields = ("document__title", "text")
    autocomplete_fields = ("workspace", "document")
    ordering = ("document", "order_index")
