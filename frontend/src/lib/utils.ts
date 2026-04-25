export function formatDateTime(value: string | null | undefined): string {
  if (!value) return "—";
  return new Date(value).toLocaleString("en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

export function truncateText(value: string, maxLength = 180): string {
  if (value.length <= maxLength) return value;
  return `${value.slice(0, maxLength)}…`;
}
