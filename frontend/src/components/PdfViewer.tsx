import React from 'react'

type Props = { src: string }

export default function PdfViewer({ src }: Props) {
  return (
    <iframe src={src} className="w-full h-full" title="pdf" />
  )
}
