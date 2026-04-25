from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.api.services.answer_generation import generate_answer_for_briefing
from apps.api.services.evaluations import evaluate_answer
from apps.api.services.excerpts import generate_excerpts_for_document
from apps.briefings.models import BriefingRequest
from apps.sources.models import SourceDocument
from apps.workspaces.models import Workspace

User = get_user_model()


class EvaluationServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="StrongPassword123!",
        )
        self.workspace = Workspace.objects.create(
            owner=self.user,
            title="Workspace",
            slug="workspace",
        )
        self.source = SourceDocument.objects.create(
            workspace=self.workspace,
            title="Manual",
            source_type="manual",
            raw_text=(
                "Generated briefing outputs must remain grounded in evidence. "
                "Teams should keep citations and review history visible."
            ),
        )
        generate_excerpts_for_document(self.source)
        self.briefing = BriefingRequest.objects.create(
            workspace=self.workspace,
            created_by=self.user,
            title="Governance summary",
            question="What governance requirements are described?",
            audience="Director",
            goal="Summarise control expectations",
        )

    def test_evaluate_answer_persists_scores_and_verdict(self):
        answer = generate_answer_for_briefing(request_obj=self.briefing, user=self.user)
        evaluation = evaluate_answer(answer)
        self.assertIsNotNone(evaluation.id)
        self.assertIn(evaluation.verdict, ["pass", "review", "fail"])
        self.assertIsNotNone(evaluation.overall_score)
