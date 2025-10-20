import sqlite3 from "sqlite3";
import path from "path";
import fs from "fs";

const DB_PATH = path.resolve(__dirname, "../../db/resume_system.db");

export function initDb() {
  const dir = path.dirname(DB_PATH);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  const db = new sqlite3.Database(DB_PATH);
  db.serialize(() => {
    db.run(`PRAGMA foreign_keys = ON;`);
    db.run(`
      CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT
      )
    `);
    db.run(`
      CREATE TABLE IF NOT EXISTS resumes (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        title TEXT,
        summary TEXT,
        updated_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
      )
    `);
    db.run(`
      CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        resume_id TEXT,
        title TEXT,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        technologies TEXT,
        FOREIGN KEY(resume_id) REFERENCES resumes(id) ON DELETE CASCADE
      )
    `);
    db.run(`
      CREATE TABLE IF NOT EXISTS skills (
        id TEXT PRIMARY KEY,
        resume_id TEXT,
        name TEXT,
        level TEXT,
        FOREIGN KEY(resume_id) REFERENCES resumes(id) ON DELETE CASCADE
      )
    `);
    db.run(`
      CREATE TABLE IF NOT EXISTS achievements (
        id TEXT PRIMARY KEY,
        resume_id TEXT,
        title TEXT,
        description TEXT,
        date TEXT,
        FOREIGN KEY(resume_id) REFERENCES resumes(id) ON DELETE CASCADE
      )
    `);
  });
  return db;
}
