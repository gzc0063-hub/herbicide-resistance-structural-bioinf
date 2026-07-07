import { useJson } from '../hooks/useJson'
import { COLORS, MECHANISM_LABELS } from '../constants'

const HEADLINE_STATS = [
  { label: 'Enzyme families pooled', value: '4' },
  { label: 'Accepted mutation rows', value: '19' },
  { label: 'Unique structural positions', value: '17' },
  { label: 'Combined non-core p-value', value: '0.0001' },
]

function Overview() {
  const { data: mechanisms } = useJson('mechanisms.json')

  const counts = {}
  if (mechanisms) {
    for (const row of mechanisms) {
      counts[row.mechanism_label] = (counts[row.mechanism_label] || 0) + 1
    }
  }

  return (
    <div className="page">
      <section className="hero">
        <h1>Do herbicide-resistance mutations share a structural address?</h1>
        <p className="lede">
          A reproducible, static structural-bioinformatics resource comparing target-site
          resistance (TSR) mutations across independently-evolved herbicide targets - PPO,
          ALS/AHAS, ACCase, and EPSPS pooled and tested, HPPD kept as a deliberate negative
          control, and FAT/DHODH tracked separately as an emerging-target risk table.
        </p>
      </section>

      <section className="stat-grid">
        {HEADLINE_STATS.map((s) => (
          <div className="stat-card" key={s.label}>
            <div className="stat-value">{s.value}</div>
            <div className="stat-label">{s.label}</div>
          </div>
        ))}
      </section>

      <section className="prose-block">
        <h2>The question</h2>
        <p>
          If several herbicide targets evolved resistance completely independently -
          different enzymes, different chemistries, different weeds - do their resistance
          mutations nonetheless land in a structurally similar place relative to the active
          site? We measure that with one consistent yardstick: distance-to-core percentile,
          relative solvent accessibility, conservation, and (as of the latest pass) a static
          biophysical perturbation score - applied identically across families, then tested
          against 10,000 random same-family residue draws.
        </p>
      </section>

      <section className="prose-block">
        <h2>What the enrichment test is really for</h2>
        <p>
          &ldquo;Resistance mutations are near the active site&rdquo; is the expected
          result, not the finding - for direct-contact residues it is close to a
          restatement of the definition. The real contribution is the reproducible{' '}
          <strong>typology</strong>: sorting each accepted position by <em>how</em> it
          relates to the pocket, and showing that the signal survives even after every
          guaranteed-zero direct-contact residue is removed.
        </p>
        {mechanisms && (
          <div className="mechanism-legend">
            {Object.entries(MECHANISM_LABELS).map(([key, label]) => (
              <div className="legend-item" key={key}>
                <span className="legend-swatch" style={{ background: COLORS[key] }} />
                <span>{label}</span>
                <span className="legend-count">{counts[key] || 0}</span>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="prose-block">
        <h2>Scope, stated plainly</h2>
        <ul className="plain-list">
          <li>Static structural context only - no binding free energy, no molecular dynamics.</li>
          <li>Non-target-site resistance (metabolism, expression, uptake) is out of scope.</li>
          <li>ACCase runs on a homology model (53.3% identity to its 1UYS template) - flagged everywhere it appears.</li>
          <li>FAT and DHODH are held in a separate Phase 5 risk table until a weed-evolved target-site mutation is verified for either.</li>
        </ul>
      </section>
    </div>
  )
}

export default Overview
