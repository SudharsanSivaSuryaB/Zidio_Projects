
/**
 * Simple local summarizer that composes a professional resume summary
 * from structured resume data. This is intentionally simple and deterministic
 * so it runs without external services.
 *
 * The function returns a short paragraph summarizing:
 * - user resume title
 * - top skills (by order)
 * - number of projects and notable achievements
 *
 * Integration point: To plug an external LLM, replace the commented section
 * with a call to your LLM client and pass the 'prompt'.
 */

type Project = { title?: string; description?: string; technologies?: string };
type Skill = { name?: string };
type Achievement = { title?: string };

export function generateSummary(payload: { resume: any; projects: Project[]; skills: Skill[]; achievements: Achievement[] }) {
  const { resume, projects, skills, achievements } = payload;
  const title = resume.title || "Professional";
  const topSkills = (skills || []).slice(0,5).map(s=>s.name).filter(Boolean).join(", ");
  const projCount = projects?.length || 0;
  const achCount = achievements?.length || 0;

  let parts: string[] = [];
  parts.push(`${title} with experience across ${projCount} project${projCount!==1?"s":""}.`);
  if (topSkills) parts.push(`Key skills: ${topSkills}.`);
  if (achCount) parts.push(`Notable achievements: ${achCount} listed.`);
  parts.push("Delivering reliable, well-documented results and ready to integrate into cross-platform ecosystems.");

  const summary = parts.join(" ");
  return summary;
}
