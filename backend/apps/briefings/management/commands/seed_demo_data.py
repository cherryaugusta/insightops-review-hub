from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from apps.api.services.answer_generation import generate_answer_for_briefing
from apps.api.services.audit import create_audit_event
from apps.api.services.evaluations import evaluate_answer
from apps.api.services.excerpts import generate_excerpts_for_document
from apps.briefings.models import BriefingRequest
from apps.evaluations.models import ReviewDecision
from apps.sources.models import SourceDocument
from apps.workspaces.models import Workspace

User = get_user_model()


class Command(BaseCommand):
    help = "Seed deterministic demo data for InsightOps Review Hub"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="demoanalyst",
            defaults={
                "email": "demoanalyst@example.com",
                "first_name": "Demo",
                "last_name": "Analyst",
            },
        )
        user.email = "demoanalyst@example.com"
        user.first_name = "Demo"
        user.last_name = "Analyst"
        user.set_password("StrongPassword123!")
        user.save()

        workspace_1, _ = Workspace.objects.get_or_create(
            owner=user,
            slug="market-intelligence-workspace",
            defaults={
                "title": "Market Intelligence Workspace",
                "description": "Workspace for source-backed market briefings.",
                "status": Workspace.Status.ACTIVE,
            },
        )
        workspace_2, _ = Workspace.objects.get_or_create(
            owner=user,
            slug="client-strategy-workspace",
            defaults={
                "title": "Client Strategy Workspace",
                "description": "Workspace for strategy source packs and briefings.",
                "status": Workspace.Status.ACTIVE,
            },
        )

        sources = [
            (
                workspace_1,
                "Q2 Market Themes Report",
                "report",
                "q2-market-themes.pdf",
                "",
                (
                    "Customer retention risk is increasing in segments where service delays continue to expand. "
                    "Regional feedback shows higher complaint volume in London and South East accounts. "
                    "Pricing sensitivity is more visible in SMB cohorts, especially where contract renewals align with energy cost increases. "
                    "The report identifies support backlog, renewal friction, and inconsistent account messaging as major operational risks. "
                    "Leaders are advised to prioritise communication consistency and service restoration actions."
                ),
            ),
            (
                workspace_1,
                "Operations Review Notes",
                "note",
                "operations-review.txt",
                "",
                (
                    "Operational resilience depends on case handling speed, ownership clarity, and repeatable review practices. "
                    "Teams with unresolved triage queues show elevated customer dissatisfaction. "
                    "Leadership notes point to workforce gaps, handoff delays, and incomplete evidence capture in issue resolution records. "
                    "A controlled review workflow is recommended for risk-sensitive accounts and escalations."
                ),
            ),
            (
                workspace_1,
                "Analyst Interview Transcript",
                "transcript",
                "analyst-interview.txt",
                "",
                (
                    "Interview participants described an increase in reactive work, especially when documentation is fragmented. "
                    "Teams rely heavily on local knowledge rather than structured source packs. "
                    "Analysts requested better citation visibility so recommendations can be reviewed quickly by managers and compliance stakeholders."
                ),
            ),
            (
                workspace_2,
                "Client Strategy Source Pack",
                "research",
                "client-strategy-pack.docx",
                "",
                (
                    "Client strategy themes for the upcoming quarter include channel efficiency, margin protection, and executive reporting clarity. "
                    "Source material highlights the importance of source-backed recommendations rather than intuition-led summaries. "
                    "Review gates are required before sharing externally. "
                    "Leaders requested visible rationale, supporting citations, and a clear approval record."
                ),
            ),
            (
                workspace_2,
                "Process Governance Manual",
                "manual",
                "governance-manual.pdf",
                "",
                (
                    "Governance guidance states that any generated briefing should remain traceable to source evidence. "
                    "Teams must retain evaluation results, reviewer comments, and timestamped audit history. "
                    "Approvals and change requests should be visible in the operational record."
                ),
            ),
        ]

        documents = []
        for workspace, title, source_type, filename, source_url, raw_text in sources:
            document, _ = SourceDocument.objects.get_or_create(
                workspace=workspace,
                title=title,
                defaults={
                    "source_type": source_type,
                    "filename": filename,
                    "source_url": source_url,
                    "raw_text": raw_text,
                    "status": SourceDocument.Status.READY,
                    "metadata": {},
                },
            )
            document.source_type = source_type
            document.filename = filename
            document.source_url = source_url
            document.raw_text = raw_text
            document.status = SourceDocument.Status.READY
            document.metadata = {}
            document.save()
            generate_excerpts_for_document(document)
            create_audit_event(
                actor=user,
                workspace=workspace,
                entity_type="source_document",
                entity_id=document.id,
                action="source_document.seeded",
                metadata={"title": document.title, "excerpt_count": document.excerpt_count},
            )
            documents.append(document)

        briefing_inputs = [
            (
                workspace_1,
                "Summarise the main customer risks",
                "What are the main customer risks emerging from the source pack?",
                "Operations Lead",
                "Prepare a concise executive briefing.",
            ),
            (
                workspace_1,
                "Identify the operational bottlenecks",
                "Which operational bottlenecks are most visible in the source material?",
                "Service Delivery Manager",
                "Prepare a short operational risk summary.",
            ),
            (
                workspace_2,
                "Explain the review and approval expectation",
                "What review and approval controls are expected before external sharing?",
                "Client Partner",
                "Prepare a governance-focused response.",
            ),
            (
                workspace_2,
                "Summarise evidence visibility requirements",
                "What evidence visibility requirements are described across the client materials?",
                "Programme Director",
                "Provide a source-backed summary.",
            ),
        ]

        created_briefings = []
        for workspace, title, question, audience, goal in briefing_inputs:
            briefing, _ = BriefingRequest.objects.get_or_create(
                workspace=workspace,
                title=title,
                defaults={
                    "created_by": user,
                    "question": question,
                    "audience": audience,
                    "goal": goal,
                    "status": BriefingRequest.Status.DRAFT,
                },
            )
            briefing.created_by = user
            briefing.question = question
            briefing.audience = audience
            briefing.goal = goal
            briefing.save()
            create_audit_event(
                actor=user,
                workspace=workspace,
                entity_type="briefing_request",
                entity_id=briefing.id,
                action="briefing_request.seeded",
                metadata={"title": briefing.title},
            )
            created_briefings.append(briefing)

        answers = []
        evaluations = []
        for briefing in created_briefings:
            existing_answer = briefing.answers.order_by("-created_at").first()
            if existing_answer:
                answers.append(existing_answer)
                latest_eval = existing_answer.evaluation_runs.order_by("-created_at").first()
                if latest_eval:
                    evaluations.append(latest_eval)
                continue

            briefing.status = BriefingRequest.Status.PROCESSING
            briefing.save(update_fields=["status", "updated_at"])

            answer = generate_answer_for_briefing(request_obj=briefing, user=user)
            evaluation = evaluate_answer(answer)

            briefing.status = (
                BriefingRequest.Status.READY
                if evaluation.verdict == "pass"
                else BriefingRequest.Status.NEEDS_REVIEW
            )
            briefing.save(update_fields=["status", "updated_at"])

            create_audit_event(
                actor=user,
                workspace=briefing.workspace,
                entity_type="briefing_answer",
                entity_id=answer.id,
                action="briefing_answer.generated",
                metadata={"provider": answer.provider, "model_name": answer.model_name},
            )
            create_audit_event(
                actor=user,
                workspace=briefing.workspace,
                entity_type="evaluation_run",
                entity_id=evaluation.id,
                action="evaluation_run.created",
                metadata={"verdict": evaluation.verdict, "overall_score": str(evaluation.overall_score)},
            )

            answers.append(answer)
            evaluations.append(evaluation)

        for answer in answers[:2]:
            if not answer.review_decisions.exists():
                decision = ReviewDecision.objects.create(
                    answer=answer,
                    reviewer=user,
                    decision=ReviewDecision.Decision.APPROVED,
                    comment="Suitable for sharing.",
                )
                answer.status = answer.Status.REVIEWED
                answer.save(update_fields=["status"])
                create_audit_event(
                    actor=user,
                    workspace=answer.request.workspace,
                    entity_type="review_decision",
                    entity_id=decision.id,
                    action="review_decision.created",
                    metadata={"decision": decision.decision},
                )

        self.stdout.write(self.style.SUCCESS("Seed data ready."))
        self.stdout.write("Demo account:")
        self.stdout.write("username: demoanalyst")
        self.stdout.write("email: demoanalyst@example.com")
        self.stdout.write("password: StrongPassword123!")
