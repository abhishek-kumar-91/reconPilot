interface StatusBadgeProps {
  status: string;
  variant?: "default" | "success" | "warning" | "danger" | "info";
}

export function StatusBadge({ status, variant = "default" }: StatusBadgeProps) {
  return <span className={`badge ${variant}`}>{status}</span>;
}