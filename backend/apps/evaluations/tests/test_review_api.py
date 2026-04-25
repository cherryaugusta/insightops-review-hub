from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.api.services.answer_generation import generate_answer_for_briefing
from apps.api.services.evaluations import evaluate_answer
from apps.api.services.excerpts import generate_excerpts_for_document
from apps.briefings.models import BriefingAnswer, BriefingRequest
from apps.sources.models import SourceDocument
from apps.workspaces.models import Workspace

User = get_user_model()


class ReviewApiTests(APITestCase):
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

        source = SourceDocument.objects.create(
            workspace=self.workspace,
            title="Source",
            source_type="note",
            raw_text="Evidence backed review is required before sharing outputs externally.",
        )
        generate_excerpts_for_document(source)
        briefing = BriefingRequest.objects.create(
            workspace=self.workspace,
            created_by=self.user,
            title="Review summary",
            question="What review controls exist?",
        )
        self.answer = generate_answer_for_briefing(request_obj=briefing, user=self.user)
        evaluate_answer(self.answer)

        other_source = SourceDocument.objects.create(
            workspace=self.other_workspace,
            title="Other Source",
            source_type="note",
            raw_text="This other workspace answer must remain inaccessible.",
        )
        generate_excerpts_for_document(other_source)
        other_briefing = BriefingRequest.objects.create(
            workspace=self.other_workspace,
            created_by=self.other_user,
            title="Other",
            question="Other question?",
        )
        self.other_answer = generate_answer_for_briefing(
            request_obj=other_briefing,
            user=self.other_user,
        )

    def test_review_decision_create_works(self):
        response = self.client.post(
            f"/api/answers/{self.answer.id}/review-decisions/",
            {"decision": "approved", "comment": "Suitable for sharing."},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_approve_review_updates_answer_status_to_reviewed(self):
        response = self.client.post(
            f"/api/answers/{self.answer.id}/review-decisions/",
            {"decision": "approved", "comment": "Approved."},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.status, BriefingAnswer.Status.REVIEWED)

    def test_cross_user_answer_review_is_rejected(self):
        response = self.client.post(
            f"/api/answers/{self.other_answer.id}/review-decisions/",
            {"decision": "approved", "comment": "Should fail."},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
