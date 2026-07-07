import { Fragment, useMemo, useState } from 'react'
import { useJson } from '../hooks/useJson'
import { COLORS } from '../constants'

const COLUMNS = [
  { key: 'family', label: 'Family' },
  { key: 'mutation_id', label: 'Mutation' },
  { key: 'species', label: 'Species' },
  { key: 'native_position', label: 'Position', numeric: true },
  { key: 'in_active_site_core', label: 'Core?' },
  { key: 'percentile_rank_distance_to_core', label: 'Distance %ile', numeric: true },
  { key: 'rsa_tien2013', label: 'RSA', numeric: true },
  { key: 'bulkiness_delta', label: 'Δ Bulkiness', numeric: true },
  { key: 'hydropathy_delta', label: 'Δ Hydropathy', numeric: true },
  { key: 'charge_delta', label: 'Δ Charge', numeric: true },
  { key: 'confidence', label: 'Confidence' },
]

function Mutations() {
  const { data, error } = useJson('mutations.json')
  const [family, setFamily] = useState('all')
  const [sortKey, setSortKey] = useState('family')
  const [sortDir, setSortDir] = useState('asc')
  const [expanded, setExpanded] = useState(null)

  const families = useMemo(() => {
    if (!data) return []
    return [...new Set(data.map((r) => r.family))].sort()
  }, [data])

  const rows = useMemo(() => {
    if (!data) return []
    let filtered = family === 'all' ? data : data.filter((r) => r.family === family)
    const col = COLUMNS.find((c) => c.key === sortKey)
    filtered = [...filtered].sort((a, b) => {
      let av = a[sortKey]
      let bv = b[sortKey]
      if (col?.numeric) {
        av = av === '' ? -Infinity : parseFloat(av)
        bv = bv === '' ? -Infinity : parseFloat(bv)
      }
      if (av < bv) return sortDir === 'asc' ? -1 : 1
      if (av > bv) return sortDir === 'asc' ? 1 : -1
      return 0
    })
    return filtered
  }, [data, family, sortKey, sortDir])

  function toggleSort(key) {
    if (key === sortKey) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortKey(key)
      setSortDir('asc')
    }
  }

  if (error) return <div className="page">Could not load mutation data: {String(error)}</div>
  if (!data) return <div className="page">Loading…</div>

  return (
    <div className="page">
      <h1>Accepted mutation table</h1>
      <p className="lede">
        Every row here is source-verified against a primary paper or accession-level
        evidence - see the Notes column for the exact citation and caveats. Click a row to
        expand it. Source: <code>output/tables/phase4_master_mutation_table.csv</code>.
      </p>

      <div className="filter-bar">
        <button
          className={family === 'all' ? 'chip active' : 'chip'}
          onClick={() => setFamily('all')}
        >
          All ({data.length})
        </button>
        {families.map((f) => (
          <button
            key={f}
            className={family === f ? 'chip active' : 'chip'}
            style={family === f ? { background: COLORS[f], borderColor: COLORS[f] } : {}}
            onClick={() => setFamily(f)}
          >
            {f} ({data.filter((r) => r.family === f).length})
          </button>
        ))}
      </div>

      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              {COLUMNS.map((c) => (
                <th key={c.key} onClick={() => toggleSort(c.key)}>
                  {c.label}
                  {sortKey === c.key ? (sortDir === 'asc' ? ' ▲' : ' ▼') : ''}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <Fragment key={`${row.mutation_id}-${i}`}>
                <tr
                  className="clickable-row"
                  onClick={() => setExpanded(expanded === i ? null : i)}
                >
                  <td>
                    <span className="family-dot" style={{ background: COLORS[row.family] }} />
                    {row.family}
                  </td>
                  <td>{row.mutation_id}</td>
                  <td className="muted">{row.species}</td>
                  <td>{row.native_position}</td>
                  <td>{row.in_active_site_core?.toLowerCase() === 'true' ? 'yes' : 'no'}</td>
                  <td>{Number(row.percentile_rank_distance_to_core).toFixed(2)}</td>
                  <td>{row.rsa_tien2013 !== '' ? Number(row.rsa_tien2013).toFixed(3) : '—'}</td>
                  <td>{row.bulkiness_delta || '—'}</td>
                  <td>{row.hydropathy_delta || '—'}</td>
                  <td>{row.charge_delta || '—'}</td>
                  <td>{row.confidence}</td>
                </tr>
                {expanded === i && (
                  <tr className="detail-row">
                    <td colSpan={COLUMNS.length}>
                      <div className="detail-panel">
                        <p>
                          <strong>Mechanism:</strong> {row.mechanism_class} &middot;{' '}
                          <strong>Structure position:</strong> {row.structure_position} (
                          {row.structure_residue_name})
                        </p>
                        <p>
                          <strong>Source:</strong> {row.source_citation}
                          {row.source_doi && (
                            <span>
                              {' '}
                              (
                              <a
                                href={`https://doi.org/${row.source_doi}`}
                                target="_blank"
                                rel="noreferrer"
                              >
                                DOI {row.source_doi}
                              </a>
                              )
                            </span>
                          )}
                        </p>
                        <p className="notes">{row.notes}</p>
                      </div>
                    </td>
                  </tr>
                )}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Mutations
