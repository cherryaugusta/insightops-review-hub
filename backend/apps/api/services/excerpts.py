from apps.sources.models import SourceDocument, SourceExcerpt


def split_text_into_excerpts(raw_text: str, chunk_size: int = 150):
    text = raw_text.strip()
    chunks = []
    start = 0
    order_index = 1

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(
                {
                    "order_index": order_index,
                    "text": chunk,
                    "token_count": len(chunk.split()),
                    "char_start": start,
                    "char_end": end,
                }
            )
            order_index += 1
        start = end

    return chunks


def generate_excerpts_for_document(document: SourceDocument):
    document.excerpts.all().delete()

    chunks = split_text_into_excerpts(document.raw_text)
    excerpt_objects = [
        SourceExcerpt(
            workspace=document.workspace,
            document=document,
            order_index=chunk["order_index"],
            text=chunk["text"],
            token_count=chunk["token_count"],
            char_start=chunk["char_start"],
            char_end=chunk["char_end"],
        )
        for chunk in chunks
    ]
    SourceExcerpt.objects.bulk_create(excerpt_objects)
    document.excerpt_count = len(excerpt_objects)
    document.save(update_fields=["excerpt_count", "updated_at"])

    return len(excerpt_objects)
