from django.contrib import admin

from apps.briefings.models import AnswerCitation, BriefingAnswer, BriefingRequest


class AnswerCitationInline(admin.TabularInline):
    model = AnswerCitation
    extra = 0
    autocomplete_fields = ("excerpt",)


class BriefingAnswerInline(admin.TabularInline):
    model = BriefingAnswer
    extra = 0
    readonly_fields = ("provider", "model_name", "confidence_band", "status", "created_at")


@admin.register(BriefingRequest)
class BriefingRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "workspace", "created_by", "status", "updated_at")
    search_fields = ("title", "question", "workspace__title", "created_by__username")
    list_filter = ("status", "created_at", "updated_at")
    autocomplete_fields = ("workspace", "created_by")
    inlines = [BriefingAnswerInline]
    ordering = ("-updated_at",)


@admin.register(BriefingAnswer)
class BriefingAnswerAdmin(admin.ModelAdmin):
    list_display = ("request", "provider", "model_name", "confidence_band", "status", "created_at")
    search_fields = ("request__title", "answer_text", "provider", "model_name")
    list_filter = ("confidence_band", "status", "provider", "created_at")
    autocomplete_fields = ("request", "generated_by")
    inlines = [AnswerCitationInline]
    ordering = ("-created_at",)
