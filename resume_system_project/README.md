
# Resume System - Trial Task (Full Project)

This repository contains a minimal, working **full-stack** implementation of the Resume System trial task:
- Frontend: Next.js + React + TypeScript (simple resume editor + preview)
- Backend: Node.js + Express + TypeScript (APIs for resume data, auth (mock), and summary generation)
- Database: SQLite schema + initial seed (using better-sqlite3 is recommended)
- AI/Automation: simple local summarizer module + example integration points for OpenAI (commented)
- Scripts: start instructions and how to run locally

> **Note:** This project is a self-contained prototype to satisfy the Trial Task brief. It intentionally avoids assumptions about 3rd-party accounts; integration points are documented and left ready for your credentials.

## Structure

- backend/        -> Express TypeScript backend
- frontend/       -> Next.js TypeScript frontend
- db/             -> SQL schema and seed
- docs/           -> design notes & API contract
- README.md       -> this file

## Quickstart (local)

### Requirements
- Node.js 18+ and npm or pnpm
- (Optional) `sqlite3` available on your system if you want to inspect DB

### Backend setup
```bash
cd /path/to/resume_system_project/backend
npm install
npm run build
npm run start
# dev
npm run dev
```

Backend default: http://localhost:4000

### Frontend setup
```bash
cd /path/to/resume_system_project/frontend
npm install
npm run dev
```

Frontend default: http://localhost:3000

### Notes
- The backend uses an SQLite database file at `db/resume_system.db`.
- The AI summarizer is a simple local implementation in `backend/src/ai/summarizer.ts`. There is an example commented-out integration for OpenAI's API client.
- Replace configuration or environment variables in `backend/.env.example` as needed.

## What to submit
- A link to your GitHub or zip file of this directory.
- A short note describing approach (see docs/APPROACH.md).

