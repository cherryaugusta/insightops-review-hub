from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.workspaces.models import Workspace

User = get_user_model()


class WorkspaceApiTests(APITestCase):
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
            title="Owned Workspace",
            slug="owned-workspace",
            description="Owned by current user",
        )
        self.other_workspace = Workspace.objects.create(
            owner=self.other_user,
            title="Other Workspace",
            slug="other-workspace",
            description="Owned by other user",
        )

    def test_list_shows_only_current_user_workspaces(self):
        response = self.client.get("/api/workspaces/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.workspace.id)

    def test_create_assigns_owner_automatically(self):
        response = self.client.post(
            "/api/workspaces/",
            {
                "title": "New Workspace",
                "slug": "new-workspace",
                "description": "Created via API",
                "status": "active",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Workspace.objects.get(id=response.data["id"])
        self.assertEqual(created.owner, self.user)

    def test_retrieve_rejects_other_user_workspace(self):
        response = self.client.get(f"/api/workspaces/{self.other_workspace.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_rejects_other_user_workspace(self):
        response = self.client.patch(
            f"/api/workspaces/{self.other_workspace.id}/",
            {"status": "archived"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_rejects_other_user_workspace(self):
        response = self.client.delete(f"/api/workspaces/{self.other_workspace.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
