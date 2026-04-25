from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.audit.models import AuditEvent
from apps.api.services.excerpts import generate_excerpts_for_document
from apps.briefings.models import BriefingRequest
from apps.sources.models import SourceDocument
from apps.workspaces.models import Workspace

User = get_user_model()


class AuditApiTests(APITestCase):
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

    def test_creating_source_writes_audit_event(self):
        response = self.client.post(
            f"/api/workspaces/{self.workspace.id}/sources/",
            {
                "title": "New Source",
                "source_type": "note",
                "filename": "source.txt",
                "source_url": "",
                "raw_text": "This source contains enough text to pass validation and create an audit event.",
                "status": "ready",
                "metadata": {},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            AuditEvent.objects.filter(
                workspace=self.workspace,
                action="source_document.created",
            ).exists()
        )

    def test_audit_list_is_owner_scoped(self):
        AuditEvent.objects.create(
            workspace=self.workspace,
            actor=self.user,
            entity_type="workspace",
            entity_id=self.workspace.id,
            action="workspace.created",
            metadata={},
        )
        AuditEvent.objects.create(
            workspace=self.other_workspace,
            actor=self.other_user,
            entity_type="workspace",
            entity_id=self.other_workspace.id,
            action="workspace.created",
            metadata={},
        )

        response = self.client.get(f"/api/workspaces/{self.workspace.id}/audit-events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_generating_answer_and_review_write_audit_events(self):
        source = SourceDocument.objects.create(
            workspace=self.workspace,
            title="Risk Source",
            source_type="note",
            raw_text="The process requires citations, evaluation, and reviewer approval before sharing.",
        )
        generate_excerpts_for_document(source)

        briefing = BriefingRequest.objects.create(
            workspace=self.workspace,
            created_by=self.user,
            title="Risk briefing",
            question="What controls are required before sharing?",
        )

        answer_response = self.client.post(f"/api/briefings/{briefing.id}/generate-answer/")
        self.assertEqual(answer_response.status_code, status.HTTP_200_OK)

        review_response = self.client.post(
            f"/api/answers/{answer_response.data['answer_id']}/review-decisions/",
            {"decision": "approved", "comment": "Suitable for sharing."},
            format="json",
        )
        self.assertEqual(review_response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            AuditEvent.objects.filter(
                workspace=self.workspace,
                action="briefing_answer.generated",
            ).exists()
        )
        self.assertTrue(
            AuditEvent.objects.filter(
                workspace=self.workspace,
                action="review_decision.created",
            ).exists()
        )
