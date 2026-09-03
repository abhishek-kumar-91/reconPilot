import { Boxes, ExternalLink } from "lucide-react";
import { useEffect, useState } from "react";
import { PageHeader } from "../components/ui/PageHeader";
import { getApiSpecs } from "../services/apiService";
import type { ApiSpec } from "../types";

export function APIs() {
  const [apiSpecs, setApiSpecs] = useState<ApiSpec[]>([]);

  useEffect(() => {
    void getApiSpecs().then(setApiSpecs).catch(() => setApiSpecs([]));
  }, []);

  return (
    <>
      <PageHeader title="API Discovery" description="OpenAPI, Swagger, GraphQL and REST intelligence." />
      <div className="cards-grid">
        {apiSpecs.map((api) => (
          <div className="panel api-card" key={api.id}>
            <div className="api-card-icon"><Boxes size={20} /></div>
            <div className="api-type">{api.type}</div>
            <h3>{api.host}</h3>
            <a className="inline-link" href={api.url} target="_blank" rel="noreferrer">{api.url} <ExternalLink size={12} /></a>
            <div className="api-meta">
              <span>Endpoints <strong>{api.endpointCount}</strong></span>
              <span>Status <strong>{api.statusCode}</strong></span>
              {api.version && <span>Version <strong>{api.version}</strong></span>}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}