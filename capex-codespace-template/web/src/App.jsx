
import React, { useEffect, useState } from 'react'
import { getProjects } from './api'

export default function App() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    (async () => {
      try {
        const data = await getProjects()
        setProjects(data)
      } catch (e) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  return (
    <div style={{ fontFamily: 'system-ui', margin: '2rem' }}>
      <h1>CapEx Projects</h1>
      {loading && <p>Loading…</p>}
      {error && <p style={{color:'crimson'}}>Error: {error}</p>}
      {!loading && !error && (
        <table border="1" cellPadding="8" cellSpacing="0">
          <thead>
            <tr>
              <th>Name</th>
              <th>Stage</th>
              <th>Status</th>
              <th>Approved Budget</th>
              <th>Actuals</th>
              <th>Variance</th>
            </tr>
          </thead>
          <tbody>
            {projects.map(p => (
              <tr key={p.id}>
                <td>{p.name}</td>
                <td>{p.stage}</td>
                <td>{p.status}</td>
                <td>${'{'}Number(p.approved_budget).toLocaleString(){'}'}</td>
                <td>${'{'}Number(p.actuals_to_date).toLocaleString(){'}'}</td>
                <td>${'{'}Number(p.variance).toLocaleString(){'}'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
