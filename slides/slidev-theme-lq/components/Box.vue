<template>
  <div class="border-l-4 border-[#4ec5d4] bg-white dark:bg-black p-4 my-4">
    <strong class="text-black dark:text-white">{{ title }}</strong>
    <slot />
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  title: { type: String, default: '' },
})
</script>

<style scoped>
/* Additional styling can be added here */
</style>
