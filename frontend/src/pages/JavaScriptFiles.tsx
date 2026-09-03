import { Code2, ExternalLink } from "lucide-react";
import { useEffect, useState } from "react";
import { PageHeader } from "../components/ui/PageHeader";
import { SearchInput } from "../components/ui/SearchInput";
import { getJavaScriptFiles } from "../services/javascriptService";
import type { JavaScriptFile } from "../types";

export function JavaScriptFiles() {
  const [search, setSearch] = useState("");
  const [javascriptFiles, setJavaScriptFiles] = useState<JavaScriptFile[]>([]);

  useEffect(() => {
    void getJavaScriptFiles().then(setJavaScriptFiles).catch(() => setJavaScriptFiles([]));
  }, []);

  const filtered = javascriptFiles.filter((file) =>
    `${file.filename} ${file.host}`.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <>
      <PageHeader title="JavaScript Files" description="Discovered client-side bundles and extracted intelligence." />
      <div className="toolbar"><SearchInput value={search} onChange={setSearch} placeholder="Search JS files..." /></div>
      <div className="panel">
        <div className="table-wrap">
          <table>
            <thead><tr><th>File</th><th>Host</th><th>Size</th><th>Endpoints</th><th>Secrets</th><th>Status</th><th>Source</th></tr></thead>
            <tbody>
              {filtered.map((file) => (
                <tr key={file.id}>
                  <td><a className="table-primary inline-link" href={file.url} target="_blank" rel="noreferrer">{file.filename} <ExternalLink size={12} /></a></td>
                  <td>{file.host}</td>
                  <td>{(file.size / 1024).toFixed(0)} KB</td>
                  <td>{file.endpointsFound}</td>
                  <td><span className={file.secretsFound ? "danger-text" : "success-text"}>{file.secretsFound}</span></td>
                  <td>{file.statusCode}</td>
                  <td>{file.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {!filtered.length && <div className="empty-state"><Code2 size={24} /><h3>No JavaScript files</h3><p>No files match your search.</p></div>}
      </div>
    </>
  );
}