"use client";

import { useState, useRef, useEffect } from "react";

const COUNTRIES = [
  "",
  "Ghana",
  "Nigeria",
  "South Africa",
  "Kenya",
  "Germany",
  "United Kingdom",
  "France",
  "Netherlands",
  "United States",
  "Canada",
];

type Message = { role: "user" | "assistant"; content: string; error?: boolean };

async function callChatApi(
  query: string,
  country: string | null
): Promise<string> {
  const base =
    process.env.NEXT_PUBLIC_CHAT_API_URL || "http://localhost:8000";
  const res = await fetch(`${base}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, country: country || null }),
  });
  if (!res.ok) throw new Error(await res.text());
  const data = await res.json();
  return data.response ?? "";
}

export default function ChatPage() {
  const [country, setCountry] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async () => {
    const q = input.trim();
    if (!q || loading) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: q }]);
    setLoading(true);
    try {
      const response = await callChatApi(q, country || null);
      setMessages((m) => [...m, { role: "assistant", content: response }]);
    } catch (e) {
      const err =
        e instanceof Error ? e.message : "Error calling API. Is the backend running?";
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `Error: ${err}`, error: true },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="chatPage">
      <h1>🛒 Global Retail Intelligence Engine</h1>
      <p className="caption">
        Ask about products, pricing by region, and warranty. Choose your country
        for accurate results.
      </p>

      <select
        className="countrySelect"
        value={country}
        onChange={(e) => setCountry(e.target.value)}
        aria-label="Your country for regional pricing"
      >
        {COUNTRIES.map((c) => (
          <option key={c || "empty"} value={c}>
            {c || "Select your country (optional)"}
          </option>
        ))}
      </select>

      <div className="messages">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`message ${msg.role} ${msg.error ? "error" : ""}`}
          >
            {msg.content.split("\n").map((line, j) => (
              <span key={j}>
                {line}
                {j < msg.content.split("\n").length - 1 ? <br /> : null}
              </span>
            ))}
          </div>
        ))}
        {loading && <div className="loading">Thinking…</div>}
        <div ref={bottomRef} />
      </div>

      <form
        className="chatForm"
        onSubmit={(e) => {
          e.preventDefault();
          send();
        }}
      >
        <input
          type="text"
          placeholder="Ask about products, price, or warranty…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </main>
  );
}
