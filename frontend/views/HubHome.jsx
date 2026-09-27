import { useEffect, useMemo, useState } from "react";
import AgentCard from "../components/AgentCard.jsx";

export default function HubHome() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("all");
  const [query, setQuery] = useState("");

  useEffect(() => {
    fetch("/api/agents")
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load agents (${res.status})`);
        return res.json();
      })
      .then((data) => {
        setAgents(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Unable to load agents.");
        setLoading(false);
      });
  }, []);

  const filtered = useMemo(() => agents.filter((agent) => {
    const text = [agent.name, agent.category, agent.tagline, agent.description].join(" ").toLowerCase();
    return (filter === "all" || agent.status === filter) && text.includes(query.trim().toLowerCase());
  }), [filter, query, agents]);

  const readyCount = agents.filter((agent) => agent.status === "ready").length;
  const categoryCount = new Set(agents.map((agent) => agent.category)).size;

  return <div className="shell">
    <aside className="sidebar"><a className="brand" href="/"><span className="brand-mark">✦</span><span>AGENT HUB</span></a><p className="nav-label">Workspace</p><nav className="nav"><a className="active" href="#top">⌂ Overview</a><a href="#catalog">▦ All agents</a><a href="#activity">↺ Run history</a></nav><div className="sidebar-foot"><strong>Independent by design</strong>Every agent has its own module, manifest, and operating boundary.</div></aside>
    <main className="main" id="top"><div className="topbar"><span>Personal workspace / overview</span><span className="profile"><span className="avatar">P</span> Pengjuan</span></div><div className="content">
      <section className="hero"><p className="eyebrow">Your independent AI team</p><h1>A home for the agents you make.</h1><p className="hero-copy">Build small, capable agents for the work you care about. Keep them independent. Bring them together here when you need to find, run, or share one.</p></section>
      <section className="stats"><div><strong>{String(agents.length).padStart(2, "0")}</strong><span>total modules</span></div><div><strong>{String(readyCount).padStart(2, "0")}</strong><span>ready to use</span></div><div><strong>{String(categoryCount).padStart(2, "0")}</strong><span>active disciplines</span></div></section>
      {loading ? <div className="empty">Loading agents…</div> : error ? <div className="empty">Could not load the agent catalog. {error}</div> : <>
        <section><div className="section-head"><div><h2>Featured in your toolbox</h2><p>The agents closest to your everyday work.</p></div><a className="view-all" href="#catalog">View all →</a></div><div className="featured">{agents.filter((agent) => agent.featured).map((agent) => <AgentCard key={agent.id} agent={agent} featured />)}</div></section>
        <section id="catalog"><div className="section-head"><div><h2>Agent catalog</h2><p>Independent modules, organized in one place.</p></div></div><div className="catalog-toolbar"><div className="filters">{["all", "ready", "building"].map((value) => <button className={filter === value ? "filter active" : "filter"} key={value} onClick={() => setFilter(value)}>{value === "all" ? "All agents" : value[0].toUpperCase() + value.slice(1)}</button>)}</div><label className="search"><span className="sr-only">Search agents</span><input value={query} onChange={(event) => setQuery(event.target.value)} type="search" placeholder="Search your agents" /></label></div><div className="catalog">{filtered.length ? filtered.map((agent) => <AgentCard key={agent.id} agent={agent} />) : <div className="empty">No agents match that search yet.</div>}</div></section>
      </>}
      <p className="footer-note" id="activity">The catalog is designed around the project registry. Agent implementations remain inside their own folders; the Hub coordinates discovery and access.</p>
    </div></main>
  </div>;
}
