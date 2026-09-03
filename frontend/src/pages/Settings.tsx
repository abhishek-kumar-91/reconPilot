import { Database, KeyRound, Server, ShieldCheck } from "lucide-react";
import { PageHeader } from "../components/ui/PageHeader";

export function Settings() {
  return (
    <>
      <PageHeader title="Settings" description="Local ReconPilot configuration." />

      <div className="settings-grid">
        <div className="panel">
          <div className="panel-header"><div><h2>Backend</h2><p>FastAPI connection</p></div><Server size={19} /></div>
          <div className="settings-field"><label>API base URL</label><input defaultValue="http://127.0.0.1:8000/api" /></div>
          <div className="settings-field"><label>Environment</label><input defaultValue="development" /></div>
        </div>

        <div className="panel">
          <div className="panel-header"><div><h2>Database</h2><p>PostgreSQL</p></div><Database size={19} /></div>
          <div className="settings-field"><label>Host</label><input defaultValue="localhost" /></div>
          <div className="settings-field"><label>Port</label><input defaultValue="5432" /></div>
        </div>

        <div className="panel">
          <div className="panel-header"><div><h2>AI</h2><p>Local Ollama runtime</p></div><KeyRound size={19} /></div>
          <div className="settings-field"><label>Ollama URL</label><input defaultValue="http://localhost:11434" /></div>
          <div className="settings-field"><label>Model</label><input defaultValue="local-model" /></div>
        </div>

        <div className="panel">
          <div className="panel-header"><div><h2>Safety</h2><p>Scope enforcement</p></div><ShieldCheck size={19} /></div>
          <div className="toggle-row"><span>Require explicit scope</span><input type="checkbox" defaultChecked /></div>
          <div className="toggle-row"><span>Block out-of-scope hosts</span><input type="checkbox" defaultChecked /></div>
          <div className="toggle-row"><span>Respect configured rate limits</span><input type="checkbox" defaultChecked /></div>
        </div>
      </div>
    </>
  );
}