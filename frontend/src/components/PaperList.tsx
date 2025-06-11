import React, { useEffect, useState } from 'react'
import { fetchPapers, pdfUrl } from '../hooks/useApi'

export type Paper = {
  id: string
  filename: string
  title?: string
}
type Props = {
  onSelect: (paper: Paper) => void
  sort?: string
  selectedId?: string
}

export default function PaperList({ onSelect, sort, selectedId }: Props) {
  const [papers, setPapers] = useState<Paper[]>([])

  useEffect(() => {
    fetchPapers(sort).then(setPapers)
  }, [sort])

  return (
    <ul className="space-y-2">
      {papers.map(p => (
        <li
          key={p.id}
          className={`cursor-pointer p-2 rounded flex items-center space-x-2 ${
            selectedId === p.id ? 'bg-gray-200' : ''
          }`}
          onClick={() => onSelect(p)}
        >
          <span className="w-4">📄</span>
          <span className="truncate">{p.title || p.filename}</span>
        </li>
      ))}
    </ul>
  )
}
