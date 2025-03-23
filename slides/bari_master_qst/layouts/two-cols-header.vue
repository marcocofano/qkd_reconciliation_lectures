<!--
  Usage:
```md
---
layout: two-cols-header
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
  </div>
</template>
<!-- <template> -->
<!--   <div class="slidev-layout two-columns w-full h-full"> -->
<!--     <div class="col-span-2"> -->
<!--       <slot /> -->
<!--     </div> -->
<!--     <div class="grid grid-cols-2 grid-rows-2"> -->
<!--       <div class="col-left" :class="props.class"> -->
<!--         <slot name="left" /> -->
<!--       </div> -->
<!--       <div class="col-right" :class="props.class"> -->
<!--         <slot name="right" /> -->
<!--       </div> -->
<!--     </div> -->
<!--   </div> -->
<!-- </template> -->
