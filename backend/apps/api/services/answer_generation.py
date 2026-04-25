from collections import Counter
import re

from apps.briefings.models import AnswerCitation, BriefingAnswer, BriefingRequest
from apps.sources.models import SourceExcerpt


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def keyword_overlap_score(question: str, excerpt_text: str) -> int:
    question_terms = Counter(tokenize(question))
    excerpt_terms = Counter(tokenize(excerpt_text))
    return sum((question_terms & excerpt_terms).values())


def select_candidate_excerpts(request_obj: BriefingRequest, limit: int = 3):
    excerpts = SourceExcerpt.objects.filter(workspace=request_obj.workspace).select_related("document")
    ranked = sorted(
        excerpts,
        key=lambda excerpt: keyword_overlap_score(request_obj.question, excerpt.text),
        reverse=True,
    )
    return [excerpt for excerpt in ranked[:limit] if keyword_overlap_score(request_obj.question, excerpt.text) > 0]


def compose_stub_answer(request_obj: BriefingRequest, excerpts):
    if not excerpts:
        return (
            f"Briefing: {request_obj.title}\n\n"
            f"Question: {request_obj.question}\n\n"
            "No sufficiently relevant excerpts were found for this request. "
            "Add more source material or refine the question before generating another answer."
        )

    bullets = []
    for excerpt in excerpts:
        bullets.append(
            f"- Evidence from {excerpt.document.title}: {excerpt.text[:240].strip()}"
        )

    return (
        f"Briefing: {request_obj.title}\n\n"
        f"Audience: {request_obj.audience or 'Internal reviewer'}\n"
        f"Goal: {request_obj.goal or 'Provide a source-backed summary'}\n\n"
        f"Question: {request_obj.question}\n\n"
        "Source-backed summary:\n"
        + "\n".join(bullets)
        + "\n\n"
        "This answer was generated deterministically from the most relevant stored excerpts in the workspace."
    )


def generate_answer_for_briefing(*, request_obj: BriefingRequest, user):
    excerpts = select_candidate_excerpts(request_obj=request_obj)
    answer_text = compose_stub_answer(request_obj, excerpts)

    answer = BriefingAnswer.objects.create(
        request=request_obj,
        generated_by=user,
        provider="stub",
        model_name="keyword-overlap-v1",
        answer_text=answer_text,
        confidence_band=BriefingAnswer.ConfidenceBand.MEDIUM if excerpts else BriefingAnswer.ConfidenceBand.LOW,
        generation_notes="Deterministic stub generation using keyword overlap across source excerpts.",
    )

    for rank, excerpt in enumerate(excerpts, start=1):
        AnswerCitation.objects.create(
            answer=answer,
            excerpt=excerpt,
            relevance_rank=rank,
            rationale="Top overlap against briefing question.",
        )

    return answer
