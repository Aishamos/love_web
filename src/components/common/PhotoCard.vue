<template>
  <div
    class="photo overflow-hidden rounded-2xl cursor-pointer group"
    @click="$emit('click')"
  >
    <img
      :src="photo.url"
      :alt="photo.alt ?? ''"
      loading="lazy"
      class="w-full h-64 md:h-72 lg:h-80 object-cover transition-transform duration-500 group-hover:scale-105"
    />
  </div>
</template>

<script setup lang="ts">
import type { Photo } from '@/types'
defineProps<{ photo: Photo }>()
defineEmits<{ click: [] }>()
</script>
