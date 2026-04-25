import type { FormEvent } from "react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { fetchWorkspaceDetail, updateWorkspace } from "./api";
import { LoadingState } from "../../components/ui/LoadingState";

export function WorkspaceEditPage() {
  const { workspaceId = "" } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    title: "",
    slug: "",
    description: "",
    status: "active" as "active" | "archived",
  });

  const query = useQuery({
    queryKey: ["workspace", workspaceId, "edit"],
    queryFn: () => fetchWorkspaceDetail(workspaceId),
  });

  useEffect(() => {
    if (query.data) {
      setForm({
        title: query.data.title,
        slug: query.data.slug,
        description: query.data.description,
        status: query.data.status,
      });
    }
  }, [query.data]);

  const mutation = useMutation({
    mutationFn: () => updateWorkspace(workspaceId, form),
    onSuccess: () => navigate(`/workspaces/${workspaceId}`),
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    mutation.mutate();
  }

  if (query.isLoading) {
    return <LoadingState label="Loading workspace form..." />;
  }

  return (
    <section className="page-section">
      <h1>Edit workspace</h1>

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

        <label>
          Status
          <select
            value={form.status}
            onChange={(e) =>
              setForm({ ...form, status: e.target.value as "active" | "archived" })
            }
          >
            <option value="active">active</option>
            <option value="archived">archived</option>
          </select>
        </label>

        <button className="button" type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Saving..." : "Save workspace"}
        </button>
      </form>
    </section>
  );
}
