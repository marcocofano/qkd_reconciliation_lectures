<template>
  <div class="flex gap-4">
    <div class="flex-1 text-center">
      <slot name="left" />
    </div>
    <div class="flex-1 text-center">
      <slot name="right" />
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    this.$nextTick(() => {
      // Ensure that KaTeX auto-render is available on the window.
      if (window.renderMathInElement) {
        window.renderMathInElement(this.$el, {
          // You can specify options here if needed, for example:
          delimiters: [
            {left: "$$", right: "$$", display: true},
            {left: "$", right: "$", display: false},
          ],
        });
      }
    });
  },
};
</script>
