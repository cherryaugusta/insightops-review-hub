from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.api.services.excerpts import generate_excerpts_for_document, split_text_into_excerpts
from apps.sources.models import SourceDocument
from apps.workspaces.models import Workspace

User = get_user_model()


class ExcerptServiceTests(TestCase):
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
        self.document = SourceDocument.objects.create(
            workspace=self.workspace,
            title="Document",
            source_type="note",
            raw_text=" ".join(["evidence"] * 300),
        )

    def test_split_text_into_excerpts_returns_chunks(self):
        chunks = split_text_into_excerpts(self.document.raw_text, chunk_size=120)
        self.assertGreater(len(chunks), 1)
        self.assertEqual(chunks[0]["order_index"], 1)

    def test_generate_excerpts_for_document_replaces_existing_rows(self):
        first_count = generate_excerpts_for_document(self.document)
        second_count = generate_excerpts_for_document(self.document)
        self.document.refresh_from_db()
        self.assertEqual(self.document.excerpt_count, second_count)
        self.assertEqual(self.document.excerpts.count(), second_count)
        self.assertGreaterEqual(first_count, 1)
