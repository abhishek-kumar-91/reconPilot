import { Link } from "react-router-dom";
import type { Endpoint } from "../../types";
import { PriorityBadge } from "../ui/PriorityBadge";

export function EndpointRow({ endpoint }: { endpoint: Endpoint }) {
  return (
    <tr>
      <td><span className={`method ${endpoint.method.toLowerCase()}`}>{endpoint.method}</span></td>
      <td>
        <div className="endpoint-cell">
          <span className="table-primary">{endpoint.path}</span>
          <span className="table-secondary">{endpoint.host}</span>
        </div>
      </td>
      <td>{endpoint.category}</td>
      <td>{endpoint.authRequired ? <span className="auth-yes">Required</span> : <span className="auth-no">Public</span>}</td>
      <td>{endpoint.parameterCount}</td>
      <td><PriorityBadge priority={endpoint.priority} /></td>
      <td>
        <Link className="small-action" to={`/endpoints?selected=${endpoint.id}`}>Inspect</Link>
      </td>
    </tr>
  );
}