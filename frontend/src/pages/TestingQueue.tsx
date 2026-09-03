import { Check, CircleSlash2, ListChecks, Play, RotateCcw } from "lucide-react";
import { useEffect, useState } from "react";
import type { QueueItem } from "../types";
import { PageHeader } from "../components/ui/PageHeader";
import { PriorityBadge } from "../components/ui/PriorityBadge";
import { StatusBadge } from "../components/ui/StatusBadge";
import { getQueueItems } from "../services/queueService";

export function TestingQueue() {
  const [items, setItems] = useState<QueueItem[]>([]);

  useEffect(() => {
    void getQueueItems().then(setItems).catch(() => setItems([]));
  }, []);

  function updateStatus(id: string, status: QueueItem["status"]) {
    setItems((current) => current.map((item) => item.id === id ? { ...item, status } : item));
  }

  return (
    <>
      <PageHeader
        title="Manual Testing Queue"
        description="AI-prioritized candidates. Validate everything manually."
      />

      <div className="queue-banner">
        <ListChecks size={20} />
        <div>
          <strong>Researcher-controlled workflow</strong>
          <p>ReconPilot prioritizes candidates; it does not automatically exploit them.</p>
        </div>
      </div>

      <div className="testing-queue">
        {items.map((item) => (
          <div className={`testing-item ${item.status}`} key={item.id}>
            <div className="testing-priority"><PriorityBadge priority={item.priority} /><strong>{item.aiScore}</strong></div>
            <div className="testing-main">
              <div className="queue-item-top">
                <span className={`method ${item.endpoint.method.toLowerCase()}`}>{item.endpoint.method}</span>
                <span className="endpoint-path">{item.endpoint.path}</span>
              </div>
              <div className="table-secondary">{item.endpoint.host}</div>
              <p>{item.reason}</p>
              {item.endpoint.notes && <div className="testing-note">{item.endpoint.notes}</div>}
            </div>
            <div className="testing-actions">
              <StatusBadge status={item.status} variant={item.status === "done" ? "success" : item.status === "testing" ? "info" : "default"} />
              {item.status === "new" && <button className="button small primary" onClick={() => updateStatus(item.id, "testing")}><Play size={14} /> Start</button>}
              {item.status === "testing" && <button className="button small secondary" onClick={() => updateStatus(item.id, "done")}><Check size={14} /> Done</button>}
              {item.status === "done" && <button className="button small secondary" onClick={() => updateStatus(item.id, "new")}><RotateCcw size={14} /> Reopen</button>}
              <button className="icon-button danger-icon" onClick={() => updateStatus(item.id, "dismissed")} title="Dismiss"><CircleSlash2 size={16} /></button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}