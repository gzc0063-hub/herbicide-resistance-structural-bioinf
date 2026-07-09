import { useJson } from '../hooks/useJson'

function Figures() {
  const { data, error } = useJson('figures.json')

  if (error) return <div className="page">Failed to load figures: {error.message}</div>
  if (!data) return <div className="page">Loading…</div>

  return (
    <div className="page">
      <h1>Manuscript figures</h1>
      <p className="lede">
        The same five figures used in the manuscript draft, generated directly from the
        pipeline&rsquo;s own tables (never hand-drawn). Each caption is the manuscript&rsquo;s
        own figure caption; the paragraph below it explains the result in plain language.
      </p>

      <div className="figure-list">
        {data.map((fig) => (
          <section className="figure-card" key={fig.id} id={fig.id}>
            <h2>{fig.title}</h2>
            <div className="figure-image-wrap">
              <img
                src={`${import.meta.env.BASE_URL}figures/${fig.svg}`}
                alt={fig.title}
                loading="lazy"
              />
            </div>
            <p className="figure-caption">
              <strong>Caption: </strong>
              {fig.caption}
            </p>
            <p className="figure-explanation">{fig.explanation}</p>
          </section>
        ))}
      </div>
    </div>
  )
}

export default Figures
