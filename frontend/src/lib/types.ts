export type WorkspaceStatus = "active" | "archived";

export type SourceType =
  | "note"
  | "report"
  | "url"
  | "transcript"
  | "research"
  | "manual";

export type SourceStatus = "draft" | "ready" | "archived";

export type BriefingStatus = "draft" | "processing" | "ready" | "needs_review";

export type AnswerStatus = "generated" | "reviewed" | "superseded";

export type ConfidenceBand = "low" | "medium" | "high";

export type EvaluationVerdict = "pass" | "review" | "fail";

export type ReviewDecisionType = "approved" | "changes_requested" | "rejected";

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface AuthUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  display_name: string;
}

export interface WorkspaceSummary {
  id: number;
  title: string;
  slug: string;
  description: string;
  status: WorkspaceStatus;
  source_document_count: number;
  briefing_request_count: number;
  last_activity_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface WorkspaceDetail extends WorkspaceSummary {
  evaluation_run_count: number;
  latest_review_decision: ReviewDecisionType | null;
}

export interface SourceDocumentSummary {
  id: number;
  title: string;
  source_type: SourceType;
  filename: string;
  source_url: string;
  status: SourceStatus;
  excerpt_count: number;
  created_at: string;
  updated_at: string;
}

export interface SourceExcerpt {
  id: number;
  document_id: number;
  order_index: number;
  text: string;
  token_count: number;
  char_start: number;
  char_end: number;
}

export interface SourceDocumentDetail extends SourceDocumentSummary {
  raw_text: string;
  metadata: Record<string, unknown>;
  excerpts: SourceExcerpt[];
}

export interface BriefingSummary {
  id: number;
  title: string;
  question: string;
  audience: string;
  goal: string;
  status: BriefingStatus;
  latest_answer_id: number | null;
  latest_evaluation_verdict: EvaluationVerdict | null;
  created_at: string;
  updated_at: string;
}

export interface AnswerCitation {
  id: number;
  excerpt_id: number;
  relevance_rank: number;
  rationale: string;
  excerpt_text: string;
  document_title: string;
}

export interface EvaluationSummary {
  id: number;
  groundedness_score: string;
  citation_coverage_score: string;
  completeness_score: string;
  overall_score: string;
  verdict: EvaluationVerdict;
  notes: string;
}

export interface ReviewDecision {
  id: number;
  decision: ReviewDecisionType;
  comment: string;
}

export interface BriefingAnswer {
  id: number;
  provider: string;
  model_name: string;
  answer_text: string;
  confidence_band: ConfidenceBand;
  status: AnswerStatus;
  generation_notes: string;
  created_at: string;
  citations: AnswerCitation[];
  latest_evaluation: EvaluationSummary | null;
  latest_review_decision: ReviewDecision | null;
}

export interface BriefingDetail {
  id: number;
  title: string;
  question: string;
  audience: string;
  goal: string;
  status: BriefingStatus;
  answers: BriefingAnswer[];
  created_at: string;
  updated_at: string;
}

export interface EvaluationDetail {
  id: number;
  answer_id: number;
  evaluator_type: string;
  groundedness_score: string;
  citation_coverage_score: string;
  completeness_score: string;
  overall_score: string;
  verdict: EvaluationVerdict;
  notes: string;
  created_at: string;
}

export interface AuditEvent {
  id: number;
  actor_display_name: string | null;
  entity_type: string;
  entity_id: number;
  action: string;
  metadata: Record<string, unknown>;
  created_at: string;
}
