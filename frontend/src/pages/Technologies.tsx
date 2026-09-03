import { Cpu } from "lucide-react";
import { useEffect, useState } from "react";
import { PageHeader } from "../components/ui/PageHeader";
import { getTechnologies } from "../services/technologyService";
import type { Technology } from "../types";

export function Technologies() {
  const [technologies, setTechnologies] = useState<Technology[]>([]);

  useEffect(() => {
    void getTechnologies().then(setTechnologies).catch(() => setTechnologies([]));
  }, []);

  return (
    <>
      <PageHeader title="Technologies" description="Technology fingerprints correlated across discovered assets." />
      <div className="technology-grid">
        {technologies.map((tech) => (
          <div className="technology-card" key={tech.id}>
            <div className="technology-icon"><Cpu size={18} /></div>
            <div className="technology-main">
              <div className="technology-name">{tech.name}</div>
              <div className="table-secondary">{tech.category}{tech.version ? ` · ${tech.version}` : ""}</div>
              <div className="confidence">
                <div className="progress"><span style={{ width: `${tech.confidence}%` }} /></div>
                <span>{tech.confidence}%</span>
              </div>
            </div>
            <div className="technology-assets">{tech.assets} assets</div>
          </div>
        ))}
      </div>
    </>
  );
}