import { Activity, Code2, Globe2, Network } from "lucide-react";
import type { DashboardStats } from "../../types";

export function ReconOverview({ stats }: { stats: DashboardStats }) {
  const bars = [stats.liveHosts, stats.endpoints, stats.jsFiles, stats.queueItems];
  const maximum = Math.max(...bars, 1);

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h2>Recon activity</h2>
          <p>Discovery volume over the current workspace</p>
        </div>
        <div className="live-indicator"><span /> Live</div>
      </div>

      <div className="activity-chart">
        {bars.map((value, index) => (
          <div className="bar-column" key={index}>
            <div className="bar" style={{ height: `${Math.max((value / maximum) * 100, 4)}%` }} />
            <span>{index + 1}</span>
          </div>
        ))}
      </div>

      <div className="mini-metrics">
        <div><Globe2 size={16} /><span>Live hosts</span><strong>{stats.liveHosts}</strong></div>
        <div><Network size={16} /><span>Endpoints</span><strong>{stats.endpoints}</strong></div>
        <div><Code2 size={16} /><span>JS files</span><strong>{stats.jsFiles}</strong></div>
        <div><Activity size={16} /><span>Queue items</span><strong>{stats.queueItems}</strong></div>
      </div>
    </div>
  );
}