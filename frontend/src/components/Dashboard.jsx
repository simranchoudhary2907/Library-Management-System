import React, {useEffect, useState} from 'react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const sample = {
  series: [
    { date: '2024-01-01', issued: 10 },
    { date: '2024-02-01', issued: 40 },
    { date: '2024-03-01', issued: 20 },
    { date: '2024-04-01', issued: 70 },
    { date: '2024-05-01', issued: 60 },
  ],
  categories: [
    { name: 'Fiction', value: 35 },
    { name: 'Science', value: 25 },
    { name: 'Technology', value: 20 },
    { name: 'History', value: 10 },
    { name: 'Other', value: 10 }
  ]
}

const COLORS = ['#7c3aed', '#06b6d4', '#f97316', '#ef4444', '#10b981']

export default function Dashboard(){
  const [data, setData] = useState(sample)

  useEffect(()=>{
    // Try fetching from backend, fallback to sample
    fetch('/api/stats').then(r=>{ if(r.ok) return r.json(); throw new Error('no api') }).then(json=> setData(json)).catch(()=>{})
  },[])

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="bg-slate-800 rounded p-4">
        <h2 className="text-lg font-semibold mb-2">Issued Books Overview</h2>
        <div style={{width: '100%', height: 250}}>
          <ResponsiveContainer>
            <AreaChart data={data.series}>
              <defs>
                <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#7c3aed" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#7c3aed" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="date" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Area type="monotone" dataKey="issued" stroke="#7c3aed" fillOpacity={1} fill="url(#colorUv)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-slate-800 rounded p-4">
        <h2 className="text-lg font-semibold mb-2">Top Categories</h2>
        <div style={{width: '100%', height: 250}}>
          <ResponsiveContainer>
            <PieChart>
              <Pie data={data.categories} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                {data.categories.map((entry, idx)=>(<Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
