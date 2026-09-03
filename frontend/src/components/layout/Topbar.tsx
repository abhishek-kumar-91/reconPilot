import { Bell, Search } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export function Topbar() {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  function submit(event: React.FormEvent) {
    event.preventDefault();
    if (query.trim()) navigate(`/endpoints?search=${encodeURIComponent(query)}`);
  }

  return (
    <header className="topbar">
      <form className="global-search" onSubmit={submit}>
        <Search size={17} />
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search endpoints, assets, hosts..."
        />
        <kbd>⌘ K</kbd>
      </form>
      <div className="topbar-actions">
        <button className="icon-button" title="Notifications">
          <Bell size={18} />
        </button>
        <div className="avatar">AK</div>
      </div>
    </header>
  );
}