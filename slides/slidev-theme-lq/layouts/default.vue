<!--
  Usage:
```md
---
layout: lq_default 
---
This shows up across both
::left::
# Left
This shows on the left
::right::
# Right
This shows on the right
```
-->

<script setup lang="ts">
const props = defineProps({
  class: {
    type: String,
  },
})
</script>


<template>
  <div class="absolute top-2 text-xs text-#146b8c w-full text-center">
    <img src="/LQ_logo.png" alt="LuxQuanta Technologies S.L." class="w-25 inline-block"/>
  </div>
  <div class="slidev-layout two-cols-with-full w-full h-full space-y-4">
    <!-- Optional header slot (full width) -->
    <div v-if="$slots.header" class="w-full">
      <slot name="header" />
    </div>
    <!-- Two-column area -->
    <div v-if="$slots.left || $slots.right" class="grid grid-cols-2 gap-4 w-full">
      <div class="col-left">
        <slot name="left" />
      </div>
      <div class="col-right">
        <slot name="right" />
      </div>
    </div>
    <!-- Default slot for full width content if no two-col content is provided -->
    <div v-if="!$slots.left && !$slots.right" class="w-full">
      <slot />
    </div>
    <!-- Optional footer slot (full width) -->
    <div v-if="$slots.footer" class="w-full">
      <slot name="footer" />
    </div>
    <!-- notes-->
    <div v-if="$slots.notes" class="absolute bottom-0 text-xs text-gray-400 text-center mt-4text-xs text-gray-400 text-center mt-4">
      <hr class="w-1/2 mx-auto border-t border-gray-300 mb-2">
      <slot name="notes" />
    </div>
  </div>
</template>
