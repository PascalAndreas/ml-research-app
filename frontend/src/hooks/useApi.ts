const API_BASE = 'http://localhost:14285'

export async function fetchPapers(sort?: string) {
  const url = new URL(API_BASE + '/papers')
  if (sort) {
    url.searchParams.set('sort', sort)
  }
  const res = await fetch(url.toString())
  return res.json()
}

export function pdfUrl(id: string) {
  return `${API_BASE}/papers/${id}/pdf`
}
