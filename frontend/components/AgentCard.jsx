import { Link } from "react-router-dom";

export default function AgentCard({ agent, featured = false }) {
  const hasRoute = Boolean(agent.route);
  return <article className={featured ? "feature-card" : "agent-card"}><div className="agent-meta"><div className="agent-id"><span className="agent-icon">{agent.icon || "•"}</span><div><div className="agent-name">{agent.name}</div><div className="agent-category">{agent.category}</div></div></div><span className="status">{agent.status === "ready" ? "Ready" : "Building"}</span></div><div className="card-copy"><h3>{agent.tagline}</h3><p>{agent.description}</p>{hasRoute ? <Link className="card-action" to={agent.route}>{agent.status === "ready" ? "Open workspace" : "Open"} ↗</Link> : <span className="card-action muted">In development</span>}</div></article>;
}
