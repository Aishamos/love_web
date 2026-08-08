<template>
  <div
    class="bg-white p-8 rounded-3xl shadow-sm cursor-pointer transition-shadow duration-300 hover:shadow-md"
    @click="$emit('click')"
  >
    <h3 class="text-lg font-light">{{ album.title }}</h3>
    <p class="text-gray-400 mt-3 text-sm">{{ album.photoCount }} Photos</p>
  </div>
</template>

<script setup lang="ts">
import type { Album } from '@/types'
defineProps<{ album: Album }>()
defineEmits<{ click: [] }>()
</script>
