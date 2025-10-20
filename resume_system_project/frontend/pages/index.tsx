
import { useState } from 'react';

export default function Home() {
  const [userId] = useState("user-1"); // simple fixed user
  const [resumeId, setResumeId] = useState<string|null>(null);
  const [title, setTitle] = useState("Frontend Developer");
  const [summary, setSummary] = useState("");
  const [projects, setProjects] = useState<any[]>([]);
  const [skills, setSkills] = useState<any[]>([]);
  const [achievements, setAchievements] = useState<any[]>([]);
  const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";

  async function createResume() {
    const res = await fetch(`${API}/api/resume`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ userId, title, summary })
    });
    const data = await res.json();
    setResumeId(data.resumeId);
    alert("Resume created: " + data.resumeId);
  }

  async function addProject() {
    if (!resumeId) return alert("Create resume first");
    const p = { title: "Sample Project", description: "Built a prototype", start_date:"2024-01", end_date:"2024-03", technologies:"React,Node" };
    const res = await fetch(`${API}/api/resume/${resumeId}/project`, { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(p) });
    const d = await res.json();
    setProjects(prev=>[...prev, {...p, id:d.id}]);
  }

  async function generateSummary() {
    if (!resumeId) return alert("Create resume first");
    const res = await fetch(`${API}/api/ai/generate/${resumeId}`, { method:"POST" });
    const d = await res.json();
    setSummary(d.summary);
    alert("Summary generated");
  }

  return (
    <div className="container">
      <h1>Resume System — Prototype</h1>
      <div className="card">
        <h3>Resume Editor</h3>
        <label>Title</label>
        <input value={title} onChange={e=>setTitle(e.target.value)} />
        <label>Summary</label>
        <textarea value={summary} onChange={e=>setSummary(e.target.value)} />
        <div style={{marginTop:8}} className="row">
          <button onClick={createResume}>Create Resume</button>
          <button onClick={addProject}>Add Sample Project</button>
          <button onClick={generateSummary}>Generate Summary (AI)</button>
        </div>
      </div>

      <div className="card">
        <h3>Preview</h3>
        <h2>{title}</h2>
        <p>{summary}</p>
        <h4>Projects</h4>
        <ul>{projects.map(p=> <li key={p.id}>{p.title} — {p.technologies}</li>)}</ul>
      </div>
    </div>
  )
}
