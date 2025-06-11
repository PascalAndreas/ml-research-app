import React from 'react'

type Props = {
  name: string
  hue: number
}

export default function TagChip({ name, hue }: Props) {
  const color = `hsl(${hue}, 70%, 50%)`
  return <span style={{ backgroundColor: color }} className="px-2 py-1 text-white rounded">{name}</span>
}
