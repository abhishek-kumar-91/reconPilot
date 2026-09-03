import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string | number;
  change?: string;
  icon: LucideIcon;
  tone?: "default" | "success" | "warning" | "danger";
}

export function StatCard({
  label,
  value,
  change,
  icon: Icon,
  tone = "default",
}: StatCardProps) {
  return (
    <div className="stat-card">
      <div className={`stat-icon ${tone}`}>
        <Icon size={19} />
      </div>
      <div className="stat-content">
        <div className="stat-label">{label}</div>
        <div className="stat-value">{value}</div>
        {change && <div className="stat-change">{change}</div>}
      </div>
    </div>
  );
}