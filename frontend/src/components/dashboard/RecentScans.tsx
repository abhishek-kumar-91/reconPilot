import { ArrowRight, Clock3 } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getScans } from "../../services/scanService";
import type { Scan } from "../../types";
import { StatusBadge } from "../ui/StatusBadge";

export function RecentScans() {
  const [scans, setScans] = useState<Scan[]>([]);

  useEffect(() => {
    void getScans().then(setScans).catch(() => setScans([]));
  }, []);

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h2>Recent scans</h2>
          <p>Latest reconnaissance jobs</p>
        </div>
        <Link className="text-link" to="/projects">View all <ArrowRight size={14} /></Link>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Target</th>
              <th>Status</th>
              <th>Progress</th>
              <th>Endpoints</th>
              <th>Started</th>
            </tr>
          </thead>
          <tbody>
            {scans.map((scan) => (
              <tr key={scan.id}>
                <td>
                  <Link className="table-primary" to={`/scans/${scan.id}`}>
                    {scan.target}
                  </Link>
                  <span className="table-secondary">{scan.id}</span>
                </td>
                <td>
                  <StatusBadge
                    status={scan.status}
                    variant={scan.status === "completed" ? "success" : scan.status === "running" ? "info" : "default"}
                  />
                </td>
                <td>
                  <div className="progress-row">
                    <div className="progress"><span style={{ width: `${scan.progress}%` }} /></div>
                    <span>{scan.progress}%</span>
                  </div>
                </td>
                <td>{scan.apiEndpoints}</td>
                <td><span className="muted"><Clock3 size={13} /> {new Date(scan.startedAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}