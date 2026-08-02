<template>
  <section id="latest" class="max-w-7xl mx-auto px-6 py-12">
    <div ref="headerRef" class="flex justify-between mb-10">
      <h2 class="text-2xl md:text-3xl font-light">
        Latest
      </h2>
      <button class="text-sm border rounded-full px-5 py-2 hover:bg-gray-50 transition-colors">
        View All
      </button>
    </div>

    <div
      ref="gridRef"
      class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-5"
    >
      <PhotoCard
        v-for="photo in photos"
        :key="photo.id"
        :photo="photo"
        @click="$emit('view', photo)"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Photo } from '@/types'
import PhotoCard from '@/components/common/PhotoCard.vue'
import { useFadeUpOnScroll } from '@/composables/useGsapAnimation'

defineProps<{ photos: Photo[] }>()
defineEmits<{ view: [photo: Photo] }>()

const headerRef = ref<HTMLElement | null>(null)
const gridRef = ref<HTMLElement | null>(null)

useFadeUpOnScroll(headerRef)
useFadeUpOnScroll(gridRef, { stagger: 0.08 })
</script>
