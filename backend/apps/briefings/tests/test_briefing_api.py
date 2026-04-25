from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.services.excerpts import generate_excerpts_for_document
from apps.briefings.models import BriefingAnswer, BriefingRequest
from apps.evaluations.models import EvaluationRun
from apps.sources.models import SourceDocument
from apps.workspaces.models import Workspace

User = get_user_model()


class BriefingApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="StrongPassword123!",
        )
        self.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="StrongPassword123!",
        )
        token = self.client.post(
            "/api/token/",
            {"username": "owner", "password": "StrongPassword123!"},
            format="json",
        ).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        self.workspace = Workspace.objects.create(
            owner=self.user,
            title="Workspace",
            slug="workspace",
        )
        self.other_workspace = Workspace.objects.create(
            owner=self.other_user,
            title="Other Workspace",
            slug="other-workspace",
        )

        self.source = SourceDocument.objects.create(
            workspace=self.workspace,
            title="Source",
            source_type="note",
            raw_text=(
                "Customer risk remains elevated because service delays and complaint volume are rising. "
                "Operational teams report review bottlenecks and missing evidence."
            ),
        )
        generate_excerpts_for_document(self.source)

        self.briefing = BriefingRequest.objects.create(
            workspace=self.workspace,
            created_by=self.user,
            title="Risk summary",
            question="What are the main customer risks?",
            audience="Ops lead",
            goal="Summarise risks",
        )

    def test_create_briefing_in_owned_workspace_works(self):
        response = self.client.post(
            f"/api/workspaces/{self.workspace.id}/briefings/",
            {
                "title": "New briefing",
                "question": "What bottlenecks are visible?",
                "audience": "Manager",
                "goal": "Summarise operational constraints",
                "status": "draft",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_briefing_list_is_owner_scoped(self):
        BriefingRequest.objects.create(
            workspace=self.other_workspace,
            created_by=self.other_user,
            title="Other briefing",
            question="Should not be visible?",
        )
        response = self.client.get(f"/api/workspaces/{self.workspace.id}/briefings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_generate_answer_creates_answer_citations_and_evaluation(self):
        response = self.client.post(f"/api/briefings/{self.briefing.id}/generate-answer/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answer = BriefingAnswer.objects.get(id=response.data["answer_id"])
        self.assertGreater(answer.citations.count(), 0)
        self.assertTrue(EvaluationRun.objects.filter(answer=answer).exists())
        self.briefing.refresh_from_db()
        self.assertIn(
            self.briefing.status,
            [BriefingRequest.Status.READY, BriefingRequest.Status.NEEDS_REVIEW],
        )
