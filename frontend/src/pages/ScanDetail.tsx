import { ArrowLeft, CheckCircle2, Clock3, Database, Globe2, Network } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { PageHeader } from "../components/ui/PageHeader";
import { StatCard } from "../components/ui/StatCard";
import { StatusBadge } from "../components/ui/StatusBadge";
import { getScan } from "../services/scanService";
import type { Scan } from "../types";

export function ScanDetail() {
  const { scanId } = useParams();
  const [scan, setScan] = useState<Scan | null>(null);

  useEffect(() => {
    if (!scanId) return;
    void getScan(scanId).then((result) => setScan(result ?? null)).catch(() => setScan(null));
  }, [scanId]);

  if (!scan) return <div className="error-state">Scan not found.</div>;

  return (
    <>
      <div className="breadcrumb"><Link to="/projects"><ArrowLeft size={14} /> Projects</Link><span>/</span><span>Scan {scan.id}</span></div>
      <PageHeader
        title={`Scan ${scan.id}`}
        description={scan.target}
        actions={<StatusBadge status={scan.status} variant={scan.status === "completed" ? "success" : "info"} />}
      />

      <div className="stats-grid compact">
        <StatCard label="Assets" value={scan.assetsFound} icon={Globe2} />
        <StatCard label="Live hosts" value={scan.liveHosts} icon={CheckCircle2} />
        <StatCard label="URLs" value={scan.urlsFound} icon={Database} />
        <StatCard label="Endpoints" value={scan.apiEndpoints} icon={Network} />
      </div>

      <div className="panel">
        <div className="panel-header">
          <div><h2>Pipeline status</h2><p>Recon stages for this scan</p></div>
          <span className="muted"><Clock3 size={14} /> {scan.progress}%</span>
        </div>
        <div className="pipeline">
          {["Scope validation", "Subdomain discovery", "Live host detection", "Technology detection", "Crawling", "JavaScript analysis", "API discovery", "Normalization"].map((stage, index) => (
            <div className="pipeline-step" key={stage}>
              <div className={`pipeline-icon ${index < Math.ceil(scan.progress / 13) ? "done" : ""}`}>
                {index < Math.ceil(scan.progress / 13) ? <CheckCircle2 size={16} /> : index + 1}
              </div>
              <span>{stage}</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}