import type { Priority } from "../../types";

export function PriorityBadge({ priority }: { priority: Priority }) {
  return (
    <span className={`priority-badge ${priority}`}>
      <span className="priority-dot" />
      {priority}
    </span>
  );
}