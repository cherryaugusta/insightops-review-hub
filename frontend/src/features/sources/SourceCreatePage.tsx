import type { FormEvent } from "react";
import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { createSource } from "./api";

export function SourceCreatePage() {
  const { workspaceId = "" } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    title: "",
    source_type: "note",
    filename: "",
    source_url: "",
    raw_text: "",
  });

  const mutation = useMutation({
    mutationFn: () => createSource(workspaceId, form),
    onSuccess: (data) => navigate(`/workspaces/${workspaceId}/sources/${data.id}`),
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    mutation.mutate();
  }

  return (
    <section className="page-section">
      <h1>Create source document</h1>

      <form className="form-grid panel" onSubmit={handleSubmit}>
        <label>
          Title
          <input
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
          />
        </label>

        <label>
          Source type
          <select
            value={form.source_type}
            onChange={(e) => setForm({ ...form, source_type: e.target.value })}
          >
            <option value="note">note</option>
            <option value="report">report</option>
            <option value="url">url</option>
            <option value="transcript">transcript</option>
            <option value="research">research</option>
            <option value="manual">manual</option>
          </select>
        </label>

        <label>
          Filename
          <input
            value={form.filename}
            onChange={(e) => setForm({ ...form, filename: e.target.value })}
          />
        </label>

        <label>
          Source URL
          <input
            value={form.source_url}
            onChange={(e) => setForm({ ...form, source_url: e.target.value })}
          />
        </label>

        <label>
          Raw text
          <textarea
            rows={12}
            value={form.raw_text}
            onChange={(e) => setForm({ ...form, raw_text: e.target.value })}
          />
        </label>

        <button className="button" type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Creating..." : "Create source"}
        </button>
      </form>
    </section>
  );
}
