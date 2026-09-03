import { ArrowLeft, Play, Globe2, Network, Code2 } from "lucide-react";
import { Link } from "react-router-dom";
import { useState } from "react";
import { useProject } from "../hooks/useProject";
import { useAsync } from "../hooks/useAsync";
import { createScan, getScans } from "../services/scanService";
import { PageHeader } from "../components/ui/PageHeader";
import { StatCard } from "../components/ui/StatCard";
import { ScanProgress } from "../components/scans/ScanProgress";
import { LoadingState } from "../components/ui/LoadingState";

export function ProjectOverview() {
  const { project, loading, error, projectId } = (() => {
    const result = useProject();
    return { project: result.data, loading: result.loading, error: result.error, projectId: result.projectId };
  })();

  const scansResult = useAsync(
    () => (projectId ? getScans(projectId) : Promise.resolve([])),
    [projectId],
  );
  const [startingScan, setStartingScan] = useState(false);
  const [startError, setStartError] = useState<string | null>(null);

  async function handleStartScan() {
    if (!projectId || startingScan) return;
    setStartingScan(true);
    setStartError(null);
    try {
      await createScan(projectId);
      await scansResult.refetch();
    } catch (err) {
      setStartError(err instanceof Error ? err.message : "Unable to start scan");
    } finally {
      setStartingScan(false);
    }
  }

  if (loading) return <LoadingState />;
  if (error || !project) return <div className="error-state">{error ?? "Project not found"}</div>;

  return (
    <>
      <div className="breadcrumb"><Link to="/projects"><ArrowLeft size={14} /> Projects</Link><span>/</span><span>{project.name}</span></div>
      <PageHeader
        title={project.name}
        description={`${project.rootDomain} · ${project.description ?? "Reconnaissance project"}`}
        actions={<button className="button primary" onClick={() => void handleStartScan()} disabled={startingScan}>
          <Play size={16} /> {startingScan ? "Starting..." : "Start scan"}
        </button>}
      />
      {startError ? <div className="error-state">{startError}</div> : null}

      <div className="stats-grid compact">
        <StatCard label="Assets" value={project.assetCount} icon={Globe2} />
        <StatCard label="Endpoints" value={project.endpointCount} icon={Network} />
        <StatCard label="JavaScript" value={scansResult.data?.[0]?.jsFiles ?? 0} icon={Code2} />
      </div>

      <div className="section-title">Scan history</div>
      {scansResult.error ? <div className="error-state">{scansResult.error}</div> : null}
      {scansResult.loading ? <LoadingState /> : (
        <div className="stack">
          {(scansResult.data ?? []).map((scan) => <ScanProgress key={scan.id} scan={scan} />)}
        </div>
      )}
    </>
  );
}