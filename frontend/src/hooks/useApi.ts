export async function fetchPapers() {
  const res = await fetch('http://localhost:14285/papers')
  return res.json()
}
