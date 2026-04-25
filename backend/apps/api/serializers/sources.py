from rest_framework import serializers

from apps.sources.models import SourceDocument, SourceExcerpt


class SourceExcerptSerializer(serializers.ModelSerializer):
    document_id = serializers.IntegerField(source="document.id", read_only=True)

    class Meta:
        model = SourceExcerpt
        fields = (
            "id",
            "document_id",
            "order_index",
            "text",
            "token_count",
            "char_start",
            "char_end",
        )


class SourceDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceDocument
        fields = (
            "id",
            "title",
            "source_type",
            "filename",
            "source_url",
            "status",
            "excerpt_count",
            "created_at",
            "updated_at",
        )


class SourceDocumentDetailSerializer(SourceDocumentListSerializer):
    excerpts = SourceExcerptSerializer(many=True, read_only=True)

    class Meta(SourceDocumentListSerializer.Meta):
        fields = SourceDocumentListSerializer.Meta.fields + (
            "raw_text",
            "metadata",
            "excerpts",
        )


class SourceDocumentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceDocument
        fields = (
            "id",
            "title",
            "source_type",
            "filename",
            "source_url",
            "raw_text",
            "status",
            "metadata",
        )
        read_only_fields = ("id",)

    def validate_title(self, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Title must contain at least 3 characters.")
        return value

    def validate_raw_text(self, value: str) -> str:
        value = value.strip()
        if len(value) < 20:
            raise serializers.ValidationError("Raw text must contain at least 20 characters.")
        return value
