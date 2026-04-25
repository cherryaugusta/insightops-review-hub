from decimal import Decimal

from apps.briefings.models import BriefingAnswer
from apps.evaluations.models import EvaluationRun


def clamp_score(value: float) -> Decimal:
    value = max(0.0, min(1.0, value))
    return Decimal(f"{value:.2f}")


def evaluate_answer(answer: BriefingAnswer):
    citation_count = answer.citations.count()
    answer_length = len(answer.answer_text.split())

    groundedness = 0.90 if citation_count >= 3 else 0.75 if citation_count >= 1 else 0.40
    citation_coverage = 0.95 if citation_count >= 3 else 0.70 if citation_count >= 1 else 0.20
    completeness = 0.85 if answer_length >= 80 else 0.65 if answer_length >= 40 else 0.35

    overall = (groundedness + citation_coverage + completeness) / 3

    if overall >= 0.80:
        verdict = EvaluationRun.Verdict.PASS
    elif overall >= 0.55:
        verdict = EvaluationRun.Verdict.REVIEW
    else:
        verdict = EvaluationRun.Verdict.FAIL

    evaluation = EvaluationRun.objects.create(
        answer=answer,
        evaluator_type="heuristic",
        groundedness_score=clamp_score(groundedness),
        citation_coverage_score=clamp_score(citation_coverage),
        completeness_score=clamp_score(completeness),
        overall_score=clamp_score(overall),
        verdict=verdict,
        notes="Heuristic evaluation based on citation density and answer length.",
    )
    return evaluation
