import { ArrowRight, Target } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getQueueItems } from "../../services/queueService";
import type { QueueItem } from "../../types";
import { PriorityBadge } from "../ui/PriorityBadge";

export function PriorityQueue() {
  const [queueItems, setQueueItems] = useState<QueueItem[]>([]);

  useEffect(() => {
    void getQueueItems().then(setQueueItems).catch(() => setQueueItems([]));
  }, []);

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h2>Manual testing queue</h2>
          <p>AI-prioritized endpoints for researcher review</p>
        </div>
        <Link className="text-link" to="/testing-queue">Open queue <ArrowRight size={14} /></Link>
      </div>
      <div className="queue-list">
        {queueItems.slice(0, 4).map((item) => (
          <div className="queue-item" key={item.id}>
            <div className="queue-item-icon"><Target size={17} /></div>
            <div className="queue-item-main">
              <div className="queue-item-top">
                <span className="method">{item.endpoint.method}</span>
                <span className="endpoint-path">{item.endpoint.path}</span>
              </div>
              <p>{item.reason}</p>
            </div>
            <div className="queue-item-score">
              <PriorityBadge priority={item.priority} />
              <span>{item.aiScore}/100</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}