import React, { useState } from 'react'

type Props = {
  onCreate: (name: string, hue: number) => void
}

export default function TagDialog({ onCreate }: Props) {
  const [name, setName] = useState('')
  const [hue, setHue] = useState(200)

  return (
    <div>
      <input value={name} onChange={e => setName(e.target.value)} placeholder="Tag name" />
      <input type="number" value={hue} onChange={e => setHue(Number(e.target.value))} />
      <button onClick={() => onCreate(name, hue)}>Add</button>
    </div>
  )
}
