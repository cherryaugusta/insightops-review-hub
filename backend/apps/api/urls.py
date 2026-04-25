from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.api.views import (
    AnswerReviewDecisionCreateAPIView,
    AuditEventListAPIView,
    EvaluationRunDetailAPIView,
    GenerateAnswerAPIView,
    GenerateExcerptsAPIView,
    MeAPIView,
    RegisterAPIView,
    SourceDocumentViewSet,
    SourceExcerptListAPIView,
    WorkspaceViewSet,
    BriefingRequestViewSet,
)

router = DefaultRouter()
router.register(r"workspaces", WorkspaceViewSet, basename="workspace")

workspace_source_list = SourceDocumentViewSet.as_view({
    "get": "list",
    "post": "create",
})
workspace_source_detail = SourceDocumentViewSet.as_view({
    "get": "retrieve",
    "patch": "partial_update",
    "delete": "destroy",
})
workspace_briefing_list = BriefingRequestViewSet.as_view({
    "get": "list",
    "post": "create",
})
workspace_briefing_detail = BriefingRequestViewSet.as_view({
    "get": "retrieve",
    "patch": "partial_update",
    "delete": "destroy",
})

urlpatterns = router.urls + [
    path("auth/register/", RegisterAPIView.as_view(), name="api-register"),
    path("auth/me/", MeAPIView.as_view(), name="api-me"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    path(
        "workspaces/<int:workspace_id>/sources/",
        workspace_source_list,
        name="workspace-source-list",
    ),
    path(
        "workspaces/<int:workspace_id>/sources/<int:pk>/",
        workspace_source_detail,
        name="workspace-source-detail",
    ),
    path(
        "sources/<int:source_id>/generate-excerpts/",
        GenerateExcerptsAPIView.as_view(),
        name="source-generate-excerpts",
    ),
    path(
        "sources/<int:source_id>/excerpts/",
        SourceExcerptListAPIView.as_view(),
        name="source-excerpt-list",
    ),

    path(
        "workspaces/<int:workspace_id>/briefings/",
        workspace_briefing_list,
        name="workspace-briefing-list",
    ),
    path(
        "workspaces/<int:workspace_id>/briefings/<int:pk>/",
        workspace_briefing_detail,
        name="workspace-briefing-detail",
    ),
    path(
        "briefings/<int:briefing_id>/generate-answer/",
        GenerateAnswerAPIView.as_view(),
        name="briefing-generate-answer",
    ),
    path(
        "answers/<int:answer_id>/review-decisions/",
        AnswerReviewDecisionCreateAPIView.as_view(),
        name="answer-review-decision-create",
    ),

    path(
        "evaluations/<int:evaluation_id>/",
        EvaluationRunDetailAPIView.as_view(),
        name="evaluation-detail",
    ),
    path(
        "workspaces/<int:workspace_id>/audit-events/",
        AuditEventListAPIView.as_view(),
        name="workspace-audit-events",
    ),
]
