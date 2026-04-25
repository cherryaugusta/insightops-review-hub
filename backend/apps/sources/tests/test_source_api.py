from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.sources.models import SourceDocument
from apps.workspaces.models import Workspace

User = get_user_model()


class SourceApiTests(APITestCase):
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
            title="Source One",
            source_type="note",
            raw_text="This is some source text that is long enough to pass validation.",
        )
        self.other_source = SourceDocument.objects.create(
            workspace=self.other_workspace,
            title="Other Source",
            source_type="note",
            raw_text="This is some other source text that is long enough to pass validation.",
        )

    def test_create_source_inside_owned_workspace_works(self):
        response = self.client.post(
            f"/api/workspaces/{self.workspace.id}/sources/",
            {
                "title": "New Source",
                "source_type": "report",
                "filename": "demo.txt",
                "source_url": "",
                "raw_text": "This raw text is definitely long enough for the serializer validation.",
                "status": "ready",
                "metadata": {},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_source_list_shows_only_owned_workspace_sources(self):
        response = self.client.get(f"/api/workspaces/{self.workspace.id}/sources/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.source.id)

    def test_source_detail_rejects_cross_user_access(self):
        response = self.client.get(
            f"/api/workspaces/{self.workspace.id}/sources/{self.other_source.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_excerpt_generation_creates_excerpts_and_updates_count(self):
        response = self.client.post(f"/api/sources/{self.source.id}/generate-excerpts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.source.refresh_from_db()
        self.assertGreater(self.source.excerpt_count, 0)
