
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

export async function getProjects() {
  const res = await fetch(`${API_URL}/api/projects`);
  if (!res.ok) throw new Error('Failed to fetch projects');
  return res.json();
}
