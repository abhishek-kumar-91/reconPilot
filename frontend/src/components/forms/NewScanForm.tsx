import { useState } from "react";
import { Play, ShieldCheck } from "lucide-react";

interface NewScanFormProps {
  onSubmit: (target: string) => void;
}

export function NewScanForm({ onSubmit }: NewScanFormProps) {
  const [target, setTarget] = useState("");

  function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!target.trim()) return;
    onSubmit(target.trim());
  }

  return (
    <form className="scan-form" onSubmit={submit}>
      <div className="form-field">
        <label htmlFor="target">Authorized target</label>
        <input
          id="target"
          value={target}
          onChange={(event) => setTarget(event.target.value)}
          placeholder="https://example.com"
        />
      </div>
      <div className="scope-note">
        <ShieldCheck size={16} />
        Only scan assets you are explicitly authorized to test.
      </div>
      <button className="button primary" type="submit">
        <Play size={16} />
        Start recon
      </button>
    </form>
  );
}