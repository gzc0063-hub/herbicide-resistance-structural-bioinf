import { useJson } from '../hooks/useJson'

function Phase5() {
  const { data: risk } = useJson('phase5_risk_table.json')
  const { data: status } = useJson('phase5_target_status.json')

  if (!risk || !status) return <div className="page">Loading…</div>

  return (
    <div className="page">
      <h1>Phase 5 — emerging-target risk table</h1>
      <p className="lede">
        FAT and DHODH are audited for evidence quality, but neither is pooled into the Phase
        4 enrichment test: every mutation below is either engineered/computationally
        predicted or lab-selected via EMS mutagenesis - not weed-evolved. They stay here
        until a genuinely weed-evolved target-site mutation is verified for either target.
      </p>

      <div className="family-grid">
        {status.map((s) => (
          <div className="family-card status-phase5" key={s.target}>
            <div className="family-card-header">
              <h2>{s.target}</h2>
              <span className="status-pill">{s.go_no_go}</span>
            </div>
            <p className="family-name">{s.target_full_name}</p>
            <p className="family-role">{s.mutation_evidence_status}</p>
            <p className="notes">{s.notes}</p>
          </div>
        ))}
      </div>

      <section className="prose-block">
        <h2>Risk table</h2>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>Target</th>
                <th>Mutation</th>
                <th>Species</th>
                <th>Evidence type</th>
                <th>Field observed?</th>
                <th>Confidence</th>
              </tr>
            </thead>
            <tbody>
              {risk.map((r, i) => (
                <tr key={i} title={r.notes}>
                  <td>{r.target}</td>
                  <td>{r.mutation_id}</td>
                  <td className="muted">{r.species}</td>
                  <td>{r.evidence_type}</td>
                  <td>{r.field_observed}</td>
                  <td>{r.confidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="muted small">Hover a row for its full source/caveat notes.</p>
      </section>
    </div>
  )
}

export default Phase5
