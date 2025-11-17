import { defineConfig, loadEnv } from "vite"
import vue from "@vitejs/plugin-vue"
import path from "path"

export default ({ mode }) => {
  // Load env (.env.development, .env.production)
  const env = loadEnv(mode, process.cwd(), "")

  return defineConfig({
    plugins: [vue()],
    server: {
      host: true,
      port: 5173,
      proxy: {
      // Proxy to the API on Django side
      '/api': {
          target: env.VITE_BACKEND_URL || "http://backend:8000",
          changeOrigin: true,
        },
      },
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src"),
      },
    },

    // ← ← ← これが "build" セクション
    build: {
      outDir: "../backend/static/dist", // Django collectstatic をサポート
      emptyOutDir: true,
    },
  })
}
