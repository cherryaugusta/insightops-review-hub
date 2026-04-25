import { createBrowserRouter, Navigate } from "react-router-dom";
import { AppShell } from "../components/layout/AppShell";
import { ProtectedRoute } from "../components/layout/ProtectedRoute";
import { LoginPage } from "../features/auth/LoginPage";
import { RegisterPage } from "../features/auth/RegisterPage";
import { ProfilePage } from "../features/auth/ProfilePage";
import { DashboardPage } from "../features/dashboard/DashboardPage";
import { WorkspaceListPage } from "../features/workspaces/WorkspaceListPage";
import { WorkspaceCreatePage } from "../features/workspaces/WorkspaceCreatePage";
import { WorkspaceDetailPage } from "../features/workspaces/WorkspaceDetailPage";
import { WorkspaceEditPage } from "../features/workspaces/WorkspaceEditPage";
import { SourceListPage } from "../features/sources/SourceListPage";
import { SourceCreatePage } from "../features/sources/SourceCreatePage";
import { SourceDetailPage } from "../features/sources/SourceDetailPage";
import { BriefingListPage } from "../features/briefings/BriefingListPage";
import { BriefingCreatePage } from "../features/briefings/BriefingCreatePage";
import { BriefingDetailPage } from "../features/briefings/BriefingDetailPage";
import { AnswerDetailPage } from "../features/briefings/AnswerDetailPage";
import { EvaluationDetailPage } from "../features/evaluations/EvaluationDetailPage";
import { AuditTimelinePage } from "../features/audit/AuditTimelinePage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/dashboard" replace />,
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/register",
    element: <RegisterPage />,
  },
  {
    element: (
      <ProtectedRoute>
        <AppShell />
      </ProtectedRoute>
    ),
    children: [
      { path: "/dashboard", element: <DashboardPage /> },
      { path: "/profile", element: <ProfilePage /> },

      { path: "/workspaces", element: <WorkspaceListPage /> },
      { path: "/workspaces/new", element: <WorkspaceCreatePage /> },
      { path: "/workspaces/:workspaceId", element: <WorkspaceDetailPage /> },
      { path: "/workspaces/:workspaceId/edit", element: <WorkspaceEditPage /> },

      { path: "/workspaces/:workspaceId/sources", element: <SourceListPage /> },
      { path: "/workspaces/:workspaceId/sources/new", element: <SourceCreatePage /> },
      { path: "/workspaces/:workspaceId/sources/:sourceId", element: <SourceDetailPage /> },

      { path: "/workspaces/:workspaceId/briefings", element: <BriefingListPage /> },
      { path: "/workspaces/:workspaceId/briefings/new", element: <BriefingCreatePage /> },
      { path: "/workspaces/:workspaceId/briefings/:briefingId", element: <BriefingDetailPage /> },

      { path: "/answers/:answerId", element: <AnswerDetailPage /> },
      { path: "/evaluations/:evaluationId", element: <EvaluationDetailPage /> },
      { path: "/workspaces/:workspaceId/audit", element: <AuditTimelinePage /> },
    ],
  },
]);
