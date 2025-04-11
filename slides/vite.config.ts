
import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@master_bari': resolve(__dirname, './decks/master_bari'),
      '@img': resolve(__dirname, './public'),
    },
  },
})
