import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: "../generated/static",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: "index.html"
      }
    }
  },
  server: {
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8765",
      "/login.html": "http://127.0.0.1:8765",
      "/admin.html": "http://127.0.0.1:8765",
      "/expired.html": "http://127.0.0.1:8765"
    }
  }
});
