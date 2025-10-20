
# Approach Note (short)

This submission implements one core module of the Resume System that is runnable end-to-end:
- A frontend UI for editing and previewing a resume (React/Next.js)
- Backend REST APIs to store resumes, list activities (projects/courses), and request an auto-generated summary
- An SQLite schema that models Users, Resumes, Projects, Courses, Achievements, and Skills
- A local AI summarizer that demonstrates how to generate a professional summary from structured user data.
- Integration readiness: APIs are documented and follow REST conventions. The summarizer includes a clear hook for plugging an external LLM.

Tools used:
- Frontend: Next.js + TypeScript (React), fetch API
- Backend: Node.js + TypeScript + Express, better-sqlite3 (synchronous SQLite client)
- Database: SQLite for portability

Evaluation criteria coverage:
- Creativity: UI/resume preview with live edits + export
- Code quality: TypeScript and clear separation of layers
- Integration readiness: REST API, DB migrations, example seed
- Documentation: README + docs

