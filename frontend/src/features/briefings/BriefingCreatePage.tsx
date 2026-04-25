import type { FormEvent } from "react";
import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { createBriefing } from "./api";

export function BriefingCreatePage() {
  const { workspaceId = "" } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    title: "",
    question: "",
    audience: "",
    goal: "",
  });

  const mutation = useMutation({
    mutationFn: () => createBriefing(workspaceId, form),
    onSuccess: (data) => navigate(`/workspaces/${workspaceId}/briefings/${data.id}`),
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    mutation.mutate();
  }

  return (
    <section className="page-section">
      <h1>Create briefing request</h1>

      <form className="form-grid panel" onSubmit={handleSubmit}>
        <label>
          Title
          <input
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
          />
        </label>

        <label>
          Question
          <textarea
            rows={4}
            value={form.question}
            onChange={(e) => setForm({ ...form, question: e.target.value })}
          />
        </label>

        <label>
          Audience
          <input
            value={form.audience}
            onChange={(e) => setForm({ ...form, audience: e.target.value })}
          />
        </label>

        <label>
          Goal
          <textarea
            rows={4}
            value={form.goal}
            onChange={(e) => setForm({ ...form, goal: e.target.value })}
          />
        </label>

        <button className="button" type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Creating..." : "Create briefing"}
        </button>
      </form>
    </section>
  );
}
