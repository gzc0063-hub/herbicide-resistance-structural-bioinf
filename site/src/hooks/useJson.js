import { useEffect, useState } from 'react'

// Fetches a JSON file exported by scripts/export_site_data.py from
// output/tables/*.csv - this hook never invents data, it only reads what the
// Python pipeline already produced and wrote to public/data/.
export function useJson(filename) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    fetch(`${import.meta.env.BASE_URL}data/${filename}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load ${filename}: ${res.status}`)
        return res.json()
      })
      .then((json) => {
        if (!cancelled) setData(json)
      })
      .catch((err) => {
        if (!cancelled) setError(err)
      })
    return () => {
      cancelled = true
    }
  }, [filename])

  return { data, error }
}
