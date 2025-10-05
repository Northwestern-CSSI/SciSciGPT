'use client'
import { useEffect } from 'react'

export function DoneMarker() {
    // Refresh the whole page after every stream is finished
    useEffect(() => {
    window.location.reload()
    }, [])
    return null
}