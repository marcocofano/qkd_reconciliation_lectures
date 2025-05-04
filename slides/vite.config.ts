
import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@slides': resolve(__dirname, './decks'),
      '@img': resolve(__dirname, './decks/public'),
    },
  },
})
