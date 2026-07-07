import { NavLink, Route, Routes } from 'react-router-dom'
import './App.css'
import Overview from './pages/Overview'
import Families from './pages/Families'
import Mutations from './pages/Mutations'
import Stats from './pages/Stats'
import Phase5 from './pages/Phase5'
import { REPO_URL } from './constants'

const NAV_ITEMS = [
  { to: '/', label: 'Overview', end: true },
  { to: '/families', label: 'Target families' },
  { to: '/mutations', label: 'Mutations' },
  { to: '/stats', label: 'Enrichment & stats' },
  { to: '/phase5', label: 'Phase 5' },
]

function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-inner">
          <div className="brand">
            <span className="brand-mark">TSR</span>
            <span className="brand-text">
              Cross-Site-of-Action Structural Bioinformatics
            </span>
          </div>
          <nav className="app-nav">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
              >
                {item.label}
              </NavLink>
            ))}
            <a className="nav-link nav-link-external" href={REPO_URL} target="_blank" rel="noreferrer">
              GitHub ↗
            </a>
          </nav>
        </div>
      </header>

      <main className="app-main">
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/families" element={<Families />} />
          <Route path="/mutations" element={<Mutations />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="/phase5" element={<Phase5 />} />
        </Routes>
      </main>

      <footer className="app-footer">
        <p>
          Every number on this site is generated from the project&rsquo;s own verified data
          tables (<code>output/tables/</code>, <code>data/processed/</code>) via{' '}
          <code>scripts/export_site_data.py</code> - nothing here is hand-typed or
          independent of the manuscript.
        </p>
      </footer>
    </div>
  )
}

export default App
