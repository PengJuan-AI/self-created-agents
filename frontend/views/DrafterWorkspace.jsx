import { useState } from "react";
import "../app/drafter.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";
const SESSION_KEY = "drafter-session-id";

export default function DrafterWorkspace() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("Your draft will appear here.");
  const [status, setStatus] = useState("");
  const [error, setError] = useState(false);
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    const prompt = message.trim();
    if (!prompt) return;

    setBusy(true);
    setError(false);
    setStatus("Writing...");
    setResponse("Drafter is working on your request.");
    try {
      const reply = await fetch(`${API_BASE}/api/agents/drafter/draft`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: prompt, session_id: localStorage.getItem(SESSION_KEY) }),
      });
      const payload = await reply.json();
      if (!reply.ok) throw new Error(payload.error || payload.detail || "Unable to reach Drafter.");
      localStorage.setItem(SESSION_KEY, payload.session_id);
      setResponse(payload.response);
      setMessage("");
      setStatus("");
    } catch (requestError) {
      setError(true);
      setResponse(requestError.message || "Unable to reach Drafter.");
      setStatus("");
    } finally {
      setBusy(false);
    }
  }

  return <main className="drafter-workspace">
    <header><h1>Drafter</h1><p>Draft and revise documents with an AI writing assistant.</p></header>
    <form onSubmit={submit}>
      <label htmlFor="message">User input</label>
      <textarea id="message" value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Describe what you want to write or revise." required />
      <div className="actions"><span aria-live="polite">{status}</span><button disabled={busy} type="submit">{busy ? "Writing..." : "Send"}</button></div>
    </form>
    <section aria-labelledby="response-label"><h2 id="response-label">Agent response</h2><div className={error ? "response error" : "response"} aria-live="polite">{response}</div></section>
  </main>;
}
