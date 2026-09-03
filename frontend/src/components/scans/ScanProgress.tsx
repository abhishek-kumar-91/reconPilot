import type { Scan } from "../../types";
import { StatusBadge } from "../ui/StatusBadge";

export function ScanProgress({ scan }: { scan: Scan }) {
  return (
    <div className="scan-progress-card">
      <div className="scan-progress-header">
        <div>
          <div className="scan-target">{scan.target}</div>
          <div className="table-secondary">{scan.id}</div>
        </div>
        <StatusBadge status={scan.status} variant={scan.status === "completed" ? "success" : "info"} />
      </div>
      <div className="progress large"><span style={{ width: `${scan.progress}%` }} /></div>
      <div className="scan-progress-stats">
        <span>{scan.progress}% complete</span>
        <span>{scan.assetsFound} assets</span>
        <span>{scan.apiEndpoints} endpoints</span>
        <span>{scan.jsFiles} JS</span>
      </div>
    </div>
  );
}