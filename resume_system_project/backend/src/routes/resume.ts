
import { Router } from "express";
import { v4 as uuidv4 } from "uuid";
import type Database from "better-sqlite3";

export default function(db: Database) {
  const router = Router();

  // Create or update resume
  router.post("/", (req, res) => {
    const { userId, title, summary } = req.body;
    if (!userId) return res.status(400).json({ error: "userId required" });
    // upsert user (simple)
    db.prepare("INSERT OR IGNORE INTO users (id, name, email) VALUES (?, ?, ?)").run(userId, "Unnamed", "");
    const resumeId = uuidv4();
    const updated_at = new Date().toISOString();
    db.prepare("INSERT INTO resumes (id, user_id, title, summary, updated_at) VALUES (?, ?, ?, ?, ?)")
      .run(resumeId, userId, title||"Untitled Resume", summary||"", updated_at);
    return res.json({ resumeId, updated_at });
  });

  // Get resume with projects/skills/achievements
  router.get("/:resumeId", (req, res) => {
    const { resumeId } = req.params;
    const r = db.prepare("SELECT * FROM resumes WHERE id = ?").get(resumeId);
    if (!r) return res.status(404).json({ error: "resume not found" });
    const projects = db.prepare("SELECT * FROM projects WHERE resume_id = ?").all(resumeId);
    const skills = db.prepare("SELECT * FROM skills WHERE resume_id = ?").all(resumeId);
    const achievements = db.prepare("SELECT * FROM achievements WHERE resume_id = ?").all(resumeId);
    return res.json({ ...r, projects, skills, achievements });
  });

  // Simple add project
  router.post("/:resumeId/project", (req, res) => {
    const { resumeId } = req.params;
    const { title, description, start_date, end_date, technologies } = req.body;
    const id = uuidv4();
    db.prepare("INSERT INTO projects (id, resume_id, title, description, start_date, end_date, technologies) VALUES (?, ?, ?, ?, ?, ?, ?)")
      .run(id, resumeId, title, description, start_date, end_date, technologies);
    return res.json({ id });
  });

  // add skill
  router.post("/:resumeId/skill", (req, res) => {
    const { resumeId } = req.params;
    const { name, level } = req.body;
    const id = uuidv4();
    db.prepare("INSERT INTO skills (id, resume_id, name, level) VALUES (?, ?, ?, ?)")
      .run(id, resumeId, name, level);
    return res.json({ id });
  });

  // add achievement
  router.post("/:resumeId/achievement", (req, res) => {
    const { resumeId } = req.params;
    const { title, description, date } = req.body;
    const id = uuidv4();
    db.prepare("INSERT INTO achievements (id, resume_id, title, description, date) VALUES (?, ?, ?, ?, ?)")
      .run(id, resumeId, title, description, date);
    return res.json({ id });
  });

  return router;
}
