import { useState, useCallback } from 'react'

const toastState = {
  toasts: [],
  listeners: new Set()
}

export function useToast() {
  const [, forceUpdate] = useState({})

  const addToast = useCallback((toast) => {
    const id = Math.random().toString(36).substr(2, 9)
    const newToast = { ...toast, id }
    
    toastState.toasts.push(newToast)
    toastState.listeners.forEach(listener => listener())
    
    // Auto remove after 5 seconds
    setTimeout(() => {
      toastState.toasts = toastState.toasts.filter(t => t.id !== id)
      toastState.listeners.forEach(listener => listener())
    }, 5000)
  }, [])

  const removeToast = useCallback((id) => {
    toastState.toasts = toastState.toasts.filter(t => t.id !== id)
    toastState.listeners.forEach(listener => listener())
  }, [])

  // Subscribe to toast changes
  useState(() => {
    const listener = () => forceUpdate({})
    toastState.listeners.add(listener)
    return () => toastState.listeners.delete(listener)
  })

  return {
    toast: addToast,
    toasts: toastState.toasts,
    dismiss: removeToast
  }
}

