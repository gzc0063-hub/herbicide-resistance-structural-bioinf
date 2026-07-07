import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { useJson } from '../hooks/useJson'
import { COLORS } from '../constants'

function formatP(p) {
  const num = Number(p)
  if (num < 0.001) return num.toExponential(1)
  return num.toFixed(4)
}

function Stats() {
  const { data } = useJson('permutation_summary.json')

  if (!data) return <div className="page">Loading…</div>

  const perFamily = data.filter((r) => r.family !== 'ALL_FAMILIES_COMBINED')
  const combined = data.filter((r) => r.family === 'ALL_FAMILIES_COMBINED')

  const chartData = perFamily.map((r) => ({
    label: `${r.family} (${r.position_set === 'all' ? 'all' : 'non-core'})`,
    family: r.family,
    observed: Number(r.observed_mean_percentile),
    random: Number(r.random_mean_percentile_mean),
    p: r.empirical_p_value_lower_tail,
    n: r.n_unique_positions,
  }))

  return (
    <div className="page">
      <h1>Enrichment &amp; the global combined test</h1>
      <p className="lede">
        Lower percentile = closer to the active-site core. Grey bars are the random-draw
        mean (always ≈50 by construction); colored bars are the accepted positions actually
        observed. Both the &ldquo;all positions&rdquo; and &ldquo;non-core only&rdquo; tests
        are shown per family - the non-core test is the non-tautological one, since it drops
        every residue that scores zero distance by definition.
      </p>

      <div className="chart-card">
        <ResponsiveContainer width="100%" height={420}>
          <BarChart data={chartData} layout="vertical" margin={{ left: 40, right: 24 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" domain={[0, 100]} label={{ value: 'Distance-to-core percentile', position: 'insideBottom', offset: -5 }} />
            <YAxis type="category" dataKey="label" width={140} />
            <Tooltip
              cursor={{ fill: 'transparent' }}
              formatter={(value, name) => [Number(value).toFixed(2), name]}
              labelFormatter={(label, payload) =>
                payload?.[0] ? `${label} — p = ${formatP(payload[0].payload.p)} (n=${payload[0].payload.n})` : label
              }
            />
            <Legend />
            <Bar dataKey="random" name="Random mean" fill={COLORS.random} />
            <Bar dataKey="observed" name="Observed">
              {chartData.map((entry, i) => (
                <Cell key={`cell-${i}`} fill={COLORS[entry.family] || COLORS.random} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <section className="prose-block">
        <h2>Family-level results</h2>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>Family</th>
                <th>Position set</th>
                <th>n</th>
                <th>Observed %ile</th>
                <th>Random mean</th>
                <th>Empirical p</th>
              </tr>
            </thead>
            <tbody>
              {perFamily.map((r, i) => (
                <tr key={i}>
                  <td>
                    <span className="family-dot" style={{ background: COLORS[r.family] }} />
                    {r.family}
                  </td>
                  <td>{r.position_set}</td>
                  <td>{r.n_unique_positions}</td>
                  <td>{Number(r.observed_mean_percentile).toFixed(2)}</td>
                  <td>{Number(r.random_mean_percentile_mean).toFixed(2)}</td>
                  <td className={Number(r.empirical_p_value_lower_tail) < 0.05 ? 'sig' : ''}>
                    {formatP(r.empirical_p_value_lower_tail)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="prose-block callout">
        <h2>The global combined permutation test</h2>
        <p>
          Pools every unique accepted position across all four families into one cohort and
          draws random same-size sets from the combined background. This is a pooled-cohort
          statistic, not a family-random-effects mixed model - no R/<code>rpy2</code>/
          <code>lme4</code> was available to build the latter, so this is reported honestly
          as the simpler alternative it is.
        </p>
        <div className="combined-grid">
          {combined.map((r) => (
            <div className="combined-card" key={r.position_set}>
              <div className="combined-n">n = {r.n_unique_positions}</div>
              <div className="combined-label">
                {r.position_set === 'combined_all' ? 'All positions, all families' : 'Non-core positions, all families'}
              </div>
              <div className="combined-p">p = {formatP(r.empirical_p_value_lower_tail)}</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default Stats
