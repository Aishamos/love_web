<template>
  <Teleport to="body">
    <div
      v-if="state.isOpen"
      ref="viewerRef"
      class="fixed inset-0 z-[200] bg-black/95 flex items-center justify-center focus:outline-none"
      tabindex="-1"
      @click.self="close"
      @keydown.esc="close"
      @keydown.left="prev"
      @keydown.right="next"
    >
      <button
        class="absolute top-6 right-6 text-white/70 hover:text-white text-2xl z-10 transition-colors"
        @click="close"
        aria-label="关闭"
      >
        ✕
      </button>

      <button
        v-if="state.currentIndex > 0"
        class="absolute left-4 md:left-8 top-1/2 -translate-y-1/2 text-white/70 hover:text-white text-4xl z-10 transition-colors"
        @click="prev"
        aria-label="上一张"
      >
        ‹
      </button>

      <div class="max-w-[90vw] max-h-[85vh] flex items-center justify-center">
        <img
          :src="state.photos[state.currentIndex]?.url"
          :alt="state.photos[state.currentIndex]?.alt ?? ''"
          class="max-w-full max-h-[85vh] object-contain rounded-lg"
        />
      </div>

      <button
        v-if="state.currentIndex < state.photos.length - 1"
        class="absolute right-4 md:right-8 top-1/2 -translate-y-1/2 text-white/70 hover:text-white text-4xl z-10 transition-colors"
        @click="next"
        aria-label="下一张"
      >
        ›
      </button>

      <div class="absolute bottom-6 text-white/50 text-sm">
        {{ state.currentIndex + 1 }} / {{ state.photos.length }}
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onUnmounted } from 'vue'
import { usePhotoViewer } from '@/composables/usePhotoViewer'

const { state, close, next, prev } = usePhotoViewer()
const viewerRef = ref<HTMLElement | null>(null)

watch(
  () => state.isOpen,
  async (open) => {
    if (open) {
      await nextTick()
      viewerRef.value?.focus()
    }
  }
)

onUnmounted(() => {
  // 组件被卸载时兜底恢复页面滚动，避免滚动锁定残留
  document.body.style.overflow = ''
})
</script>
