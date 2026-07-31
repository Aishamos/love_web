<template>
  <section id="albums" class="bg-gray-50 py-24">
    <div class="max-w-6xl mx-auto px-6">
      <h2 ref="titleRef" class="text-2xl md:text-3xl font-light mb-12">
        Albums
      </h2>

      <div
        ref="gridRef"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 md:gap-6"
      >
        <AlbumCard
          v-for="album in albums"
          :key="album.id"
          :album="album"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Album } from '@/types'
import AlbumCard from '@/components/common/AlbumCard.vue'
import { useFadeUpOnScroll } from '@/composables/useGsapAnimation'

defineProps<{ albums: Album[] }>()

const titleRef = ref<HTMLElement | null>(null)
const gridRef = ref<HTMLElement | null>(null)

useFadeUpOnScroll(titleRef)
useFadeUpOnScroll(gridRef, { stagger: 0.1 })
</script>
