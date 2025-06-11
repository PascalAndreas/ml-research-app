import React, { useState } from 'react'
import PaperSidebar from './components/PaperSidebar'
import PdfViewer from './components/PdfViewer'
import { Paper } from './components/PaperList'
import { pdfUrl } from './hooks/useApi'

export default function App() {
  const [current, setCurrent] = useState<Paper | null>(null)

  return (
    <div className="flex h-screen">
      <PaperSidebar onSelect={setCurrent} />
      <div className="flex-1 flex flex-col">
        <div className="p-2 border-b">
          <h1 className="text-xl font-bold">ML Paper Manager</h1>
        </div>
        <div className="flex-1">{current && <PdfViewer src={pdfUrl(current.id)} />}</div>
      </div>
    </div>
  )
}
