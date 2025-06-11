import React, { useEffect, useState } from 'react'
import { fetchPapers } from '../hooks/useApi'

export default function PaperList() {
  const [papers, setPapers] = useState<any[]>([])

  useEffect(() => {
    fetchPapers().then(setPapers)
  }, [])

  return (
    <ul>
      {papers.map(p => (
        <li key={p.id}>{p.title || p.filename}</li>
      ))}
    </ul>
  )
}
