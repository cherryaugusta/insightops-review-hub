import type { FormEvent } from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { createWorkspace } from "./api";

export function WorkspaceCreatePage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    title: "",
    slug: "",
    description: "",
  });

  const mutation = useMutation({
    mutationFn: () => createWorkspace(form),
    onSuccess: (data) => navigate(`/workspaces/${data.id}`),
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    mutation.mutate();
  }

  return (
    <section className="page-section">
      <h1>Create workspace</h1>

      <form className="form-grid panel" onSubmit={handleSubmit}>
        <label>
          Title
          <input
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
          />
        </label>

        <label>
          Slug
          <input
            value={form.slug}
            onChange={(e) => setForm({ ...form, slug: e.target.value })}
          />
        </label>

        <label>
          Description
          <textarea
            rows={5}
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
        </label>

        <button className="button" type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Creating..." : "Create workspace"}
        </button>
      </form>
    </section>
  );
}
