import React, { useState } from 'react'
import PaperList, { Paper } from './PaperList'

interface Props {
  onSelect: (paper: Paper) => void
}

export default function PaperSidebar({ onSelect }: Props) {
  const [open, setOpen] = useState(true)
  const [sort, setSort] = useState<string>('added')

  return (
    <div className={`bg-white border-r h-full ${open ? 'w-64' : 'w-0'} transition-width duration-300 overflow-hidden`}>
      <div className="p-2 flex items-center justify-between border-b">
        <span className="font-semibold">Papers</span>
        <button onClick={() => setOpen(o => !o)} className="text-sm">
          {open ? 'Hide' : 'Show'}
        </button>
      </div>
      {open && (
        <div className="p-2 space-y-2">
          <select value={sort} onChange={e => setSort(e.target.value)} className="w-full border rounded p-1 text-sm">
            <option value="added">Sort by added</option>
            <option value="access">Sort by last access</option>
          </select>
          <PaperList onSelect={onSelect} sort={sort} />
        </div>
      )}
    </div>
  )
}
