from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.api.services.answer_generation import generate_answer_for_briefing
from apps.api.services.excerpts import generate_excerpts_for_document
from apps.briefings.models import BriefingRequest
from apps.sources.models import SourceDocument
from apps.workspaces.models import Workspace

User = get_user_model()


class AnswerGenerationServiceTests(TestCase):
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
            title="Risk Report",
            source_type="report",
            raw_text=(
                "Customer retention risk is increasing where service delays continue. "
                "Complaint volume and backlog are rising in London accounts."
            ),
        )
        generate_excerpts_for_document(self.source)
        self.briefing = BriefingRequest.objects.create(
            workspace=self.workspace,
            created_by=self.user,
            title="Risk briefing",
            question="What customer risks are increasing?",
            audience="Ops lead",
            goal="Summarise evidence",
        )

    def test_generate_answer_for_briefing_creates_stub_answer_and_citations(self):
        answer = generate_answer_for_briefing(request_obj=self.briefing, user=self.user)
        self.assertEqual(answer.provider, "stub")
        self.assertEqual(answer.model_name, "keyword-overlap-v1")
        self.assertGreaterEqual(answer.citations.count(), 1)
        self.assertIn("Source-backed summary", answer.answer_text)
