<template>
  <div class="border-l-4 border-[#146b8c] bg-white dark:bg-black p-4 my-4">
    <strong class="text-black dark:text-white">Definition: {{ title }}.</strong>
    <slot />
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  title: { type: String, default: 'Definition' },
})
</script>

<style scoped>
/* Additional styling can be added here */
</style>
