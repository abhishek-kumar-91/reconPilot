import { Filter, Network, SlidersHorizontal } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import type { Endpoint, EndpointCategory, Priority } from "../types";
import { PageHeader } from "../components/ui/PageHeader";
import { SearchInput } from "../components/ui/SearchInput";
import { EndpointRow } from "../components/endpoints/EndpointRow";
import { PriorityBadge } from "../components/ui/PriorityBadge";
import { getEndpoints } from "../services/endpointService";

export function Endpoints() {
  const [params] = useSearchParams();
  const initialSearch = params.get("search") ?? "";
  const [search, setSearch] = useState(initialSearch);
  const [category, setCategory] = useState<EndpointCategory | "all">("all");
  const [priority, setPriority] = useState<Priority | "all">("all");
  const [endpoints, setEndpoints] = useState<Endpoint[]>([]);

  useEffect(() => {
    void getEndpoints().then(setEndpoints).catch(() => setEndpoints([]));
  }, []);

  const filtered = useMemo(() => endpoints.filter((endpoint) => {
    const matchesSearch = `${endpoint.host} ${endpoint.path} ${endpoint.method}`
      .toLowerCase().includes(search.toLowerCase());
    const matchesCategory = category === "all" || endpoint.category === category;
    const matchesPriority = priority === "all" || endpoint.priority === priority;
    return matchesSearch && matchesCategory && matchesPriority;
  }), [endpoints, search, category, priority]);

  return (
    <>
      <PageHeader title="Endpoints" description="Normalized application endpoints discovered across recon sources." />
      <div className="toolbar endpoints-toolbar">
        <SearchInput value={search} onChange={setSearch} placeholder="Search path, host, method..." />
        <select value={category} onChange={(e) => setCategory(e.target.value as EndpointCategory | "all")}>
          <option value="all">All categories</option>
          <option value="authentication">Authentication</option>
          <option value="authorization">Authorization</option>
          <option value="business-logic">Business Logic</option>
          <option value="file-upload">File Upload</option>
          <option value="admin">Admin</option>
          <option value="graphql">GraphQL</option>
        </select>
        <select value={priority} onChange={(e) => setPriority(e.target.value as Priority | "all")}>
          <option value="all">All priorities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
        <button className="button secondary"><SlidersHorizontal size={15} /> Filters</button>
      </div>

      <div className="result-summary">
        <span><Network size={15} /> {filtered.length} endpoints</span>
        <span><Filter size={14} /> Sorted by relevance</span>
        <span><PriorityBadge priority="high" /> Priority available</span>
      </div>

      <div className="panel">
        <div className="table-wrap">
          <table>
            <thead><tr><th>Method</th><th>Endpoint</th><th>Category</th><th>Auth</th><th>Params</th><th>Priority</th><th></th></tr></thead>
            <tbody>{filtered.map((endpoint) => <EndpointRow key={endpoint.id} endpoint={endpoint} />)}</tbody>
          </table>
        </div>
      </div>
    </>
  );
}