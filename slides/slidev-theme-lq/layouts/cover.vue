<script setup lang="ts">
import { computed } from 'vue'
import { handleBackground } from "../layoutHelper"

const props = defineProps({
  subtitle: {
    default: "SubTitle"
  },
  backgroundImg: {
    type: String,
    default: ''
  }
})

// Compute the background style only for the first slide.
const backgroundStyle = computed(() => 
  handleBackground(props.backgroundImg, false)
)
console.log("bgimg: ", backgroundStyle)
</script>

<template>
  <div class="slidev-layout cover text-center" :style="backgroundStyle">
    <div class="my-auto w-full">
      <!-- Render header info only on the first (cover) slide -->
      <header class="slide-header">
        <h1>{{ $slidev.configs.title }}</h1>
        <h2>{{ subtitle }}</h2>
        <div class="slide-info" v-html="$slidev.configs.info"></div>
      </header>
      <main class="slide-content">
        <slot />
      </main>
    </div>
  </div>
</template>


<!--   h1 { -->
<!--   /* background-color: #2b90b6; */ -->
<!--   /* background-image: linear-gradient(45deg, #4ec5d4 10%, #146b8c 20%); */ -->
<!--   /* background-size: 100%; */ -->
<!--   /* -webkit-background-clip: text; */ -->
<!--   /* -moz-background-clip: text; */ -->
<!--   /* -webkit-text-fill-color: transparent; */ -->
<!--   /* -moz-text-fill-color: transparent; */ -->
<!--   color: #2b90b6 !important; /* Or another color of your choice */ -->
<!-- } -->
<!---->
<!-- @media print { -->
<!--   .slidev-slide__header h1 { -->
<!--     background: none !important; -->
<!--     -webkit-background-clip: initial !important; -->
<!--     -moz-background-clip: initial !important; -->
<!--     -webkit-text-fill-color: initial !important; -->
<!--     -moz-text-fill-color: initial !important; -->
<!--     color: #2b90b6 !important; /* Or another color of your choice */ -->
<!--   } -->
<!--  .slidev-slide { -->
<!--     background-color: #0B0C0E !important; /* Dark background */ -->
<!--     color: #E2E8F0 !important;            /* Light text color */ -->
<!--   } -->
<!-- } -->
