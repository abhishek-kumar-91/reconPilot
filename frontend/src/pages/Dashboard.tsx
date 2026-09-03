import { Code2, Cpu, Globe2, ListChecks, Network, Radar, ScanSearch } from "lucide-react";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { PageHeader } from "../components/ui/PageHeader";
import { StatCard } from "../components/ui/StatCard";
import { RecentScans } from "../components/dashboard/RecentScans";
import { PriorityQueue } from "../components/dashboard/PriorityQueue";
import { ReconOverview } from "../components/dashboard/ReconOverview";
import { apiRequest } from "../services/api";
import type { DashboardStats } from "../types";

export function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    projects: 0,
    assets: 0,
    liveHosts: 0,
    endpoints: 0,
    jsFiles: 0,
    apiSpecs: 0,
    technologies: 0,
    queueItems: 0,
  });

  useEffect(() => {
    void apiRequest<DashboardStats>("/dashboard").then(setStats).catch(() => undefined);
  }, []);

  return (
    <>
      <PageHeader
        title="Dashboard"
        description="Your reconnaissance workspace at a glance."
        actions={
          <Link className="button primary" to="/projects">
            <Radar size={16} />
            Start a scan
          </Link>
        }
      />

      <div className="stats-grid">
        <StatCard label="Projects" value={stats.projects} icon={Radar} />
        <StatCard label="Assets" value={stats.assets} icon={Globe2} tone="success" />
        <StatCard label="Live hosts" value={stats.liveHosts} icon={ScanSearch} tone="success" />
        <StatCard label="Endpoints" value={stats.endpoints} icon={Network} tone="default" />
        <StatCard label="JavaScript" value={stats.jsFiles} icon={Code2} />
        <StatCard label="API specs" value={stats.apiSpecs} icon={ListChecks} />
        <StatCard label="Technologies" value={stats.technologies} icon={Cpu} />
        <StatCard label="Testing queue" value={stats.queueItems} icon={Radar} tone="warning" />
      </div>

      <div className="dashboard-grid">
        <ReconOverview stats={stats} />
        <PriorityQueue />
      </div>

      <RecentScans />
    </>
  );
}