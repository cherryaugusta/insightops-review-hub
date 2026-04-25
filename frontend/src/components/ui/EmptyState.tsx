type EmptyStateProps = {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
};

export function EmptyState({
  title,
  description,
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <section className="empty-state">
      <h3>{title}</h3>
      <p>{description}</p>
      {actionLabel && onAction ? (
        <button className="button" onClick={onAction}>
          {actionLabel}
        </button>
      ) : null}
    </section>
  );
}
