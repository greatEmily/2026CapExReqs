
const API_URL = 'https://orange-carnival-xpj4gj4v7r7cpprg-3000.app.github.dev/'

export async function getProjects() {
  const res = await fetch(`${API_URL}/api/projects`);
  if (!res.ok) throw new Error('Failed to fetch projects');
  return res.json();
}
