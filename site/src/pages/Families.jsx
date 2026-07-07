import { useJson } from '../hooks/useJson'

const STATUS_LABEL = {
  pooled: 'Pooled, tested',
  contrast: 'Negative control',
  phase5: 'Phase 5 risk table',
}

function Families() {
  const { data: families } = useJson('families.json')
  const { data: mutations } = useJson('mutations.json')

  const countByFamily = {}
  if (mutations) {
    for (const row of mutations) {
      countByFamily[row.family] = (countByFamily[row.family] || 0) + 1
    }
  }

  if (!families) return <div className="page">Loading…</div>

  return (
    <div className="page">
      <h1>The seven target families</h1>
      <p className="lede">
        Four families form the fully-validated, pooled core of the analysis. HPPD is a
        deliberate contrast case. FAT and DHODH are emerging targets audited into a separate
        Phase 5 risk table, not the pooled enrichment test.
      </p>

      <div className="family-grid">
        {Object.entries(families).map(([code, info]) => (
          <div className={`family-card status-${info.status}`} key={code}>
            <div className="family-card-header">
              <h2>{code}</h2>
              <span className="status-pill">{STATUS_LABEL[info.status]}</span>
            </div>
            <p className="family-name">{info.name}</p>
            <p className="family-species">{info.species}</p>
            <p className="family-role">{info.role}</p>
            <div className="family-footer">
              {info.pdb ? (
                <a
                  href={`https://www.rcsb.org/structure/${info.pdb}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  PDB {info.pdb} ↗
                </a>
              ) : (
                <span className="muted">no public structure</span>
              )}
              {countByFamily[code] !== undefined && (
                <span className="mutation-count">{countByFamily[code]} accepted mutation row(s)</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Families
