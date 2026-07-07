import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
// base must match the GitHub Pages URL path: https://<user>.github.io/<repo>/
export default defineConfig({
  base: '/herbicide-resistance-structural-bioinf/',
  plugins: [react()],
})
