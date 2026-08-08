<template>
  <div
    class="photo overflow-hidden rounded-2xl cursor-pointer group"
    @click="$emit('click')"
  >
    <img
      :src="photo.thumbnailUrl ?? photo.url"
      :alt="photo.alt ?? ''"
      loading="lazy"
      class="w-full h-64 md:h-72 lg:h-80 object-cover transition-transform duration-500 group-hover:scale-105"
      @error="onImgError"
    />
  </div>
</template>

<script setup lang="ts">
import { FALLBACK_IMAGE } from '@/utils/imageFallback'
import type { Photo } from '@/types'

const props = defineProps<{ photo: Photo }>()
defineEmits<{ click: [] }>()

function onImgError(e: Event) {
  const img = e.target as HTMLImageElement
  if (img.src !== FALLBACK_IMAGE) {
    img.src = FALLBACK_IMAGE
    img.alt = props.photo.alt || '图片不可用'
  }
}
</script>
