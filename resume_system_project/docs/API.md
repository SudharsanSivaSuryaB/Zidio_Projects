
# API Contract (summary)

Base: /api

## Resume
POST /api/resume
- body: { userId, title, summary }
- response: { resumeId, updated_at }

GET /api/resume/:resumeId
- response: { id, user_id, title, summary, updated_at, projects[], skills[], achievements[] }

POST /api/resume/:resumeId/project
- body: { title, description, start_date, end_date, technologies }
- response: { id }

POST /api/resume/:resumeId/skill
- body: { name, level }
- response: { id }

POST /api/resume/:resumeId/achievement
- body: { title, description, date }
- response: { id }

## AI
POST /api/ai/generate/:resumeId
- response: { summary }
