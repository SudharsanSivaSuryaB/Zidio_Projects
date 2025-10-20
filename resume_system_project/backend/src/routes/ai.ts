
import { Router } from "express";
import type Database from "better-sqlite3";
import { generateSummary } from "../services/summarizer";

export default function(db: Database) {
  const router = Router();

  router.post("/generate/:resumeId", (req, res) => {
    const { resumeId } = req.params;
    const resume = db.prepare("SELECT * FROM resumes WHERE id = ?").get(resumeId);
    if (!resume) return res.status(404).json({ error: "resume not found" });
    const projects = db.prepare("SELECT * FROM projects WHERE resume_id = ?").all(resumeId);
    const skills = db.prepare("SELECT * FROM skills WHERE resume_id = ?").all(resumeId);
    const achievements = db.prepare("SELECT * FROM achievements WHERE resume_id = ?").all(resumeId);
    const summary = generateSummary({ resume, projects, skills, achievements });
    // persist
    db.prepare("UPDATE resumes SET summary = ?, updated_at = ? WHERE id = ?").run(summary, new Date().toISOString(), resumeId);
    return res.json({ summary });
  });

  return router;
}
