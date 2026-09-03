import { Globe2 } from "lucide-react";
import { useEffect, useState } from "react";
import { PageHeader } from "../components/ui/PageHeader";
import { SearchInput } from "../components/ui/SearchInput";
import { StatusBadge } from "../components/ui/StatusBadge";
import { getAssets } from "../services/assetService";
import type { Asset } from "../types";

export function Assets() {
  const [search, setSearch] = useState("");
  const [assets, setAssets] = useState<Asset[]>([]);

  useEffect(() => {
    void getAssets().then(setAssets).catch(() => setAssets([]));
  }, []);

  const filtered = assets.filter((asset) =>
    `${asset.hostname} ${asset.title ?? ""} ${asset.technologies.join(" ")}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  );

  return (
    <>
      <PageHeader title="Assets" description="Discovered domains, subdomains and live services." />
      <div className="toolbar"><SearchInput value={search} onChange={setSearch} placeholder="Search hosts..." /></div>
      <div className="panel">
        <div className="table-wrap">
          <table>
            <thead><tr><th>Host</th><th>Status</th><th>Title</th><th>Technologies</th><th>Ports</th><th>Sources</th></tr></thead>
            <tbody>
              {filtered.map((asset) => (
                <tr key={asset.id}>
                  <td><div className="endpoint-cell"><span className="table-primary">{asset.hostname}</span><span className="table-secondary">{asset.url}</span></div></td>
                  <td><StatusBadge status={asset.alive ? `${asset.statusCode}` : "offline"} variant={asset.statusCode === 200 ? "success" : "warning"} /></td>
                  <td>{asset.title}</td>
                  <td><div className="tag-list">{asset.technologies.map((tech) => <span className="tag" key={tech}>{tech}</span>)}</div></td>
                  <td>{asset.ports.join(", ")}</td>
                  <td>{asset.source.join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {!filtered.length && <div className="empty-state"><Globe2 size={24} /><h3>No assets found</h3><p>Try a different search.</p></div>}
      </div>
    </>
  );
}