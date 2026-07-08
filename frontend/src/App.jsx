import React from 'react'
import Dashboard from './components/Dashboard'

export default function App(){
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6">LibraMS — Dashboard</h1>
        <Dashboard />
      </div>
    </div>
  )
}
