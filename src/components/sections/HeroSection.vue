<template>
  <section id="hero" class="pt-24 px-5">
    <div
      ref="sectionRef"
      class="max-w-7xl mx-auto relative h-[50vh] md:h-[70vh] lg:h-[80vh] overflow-hidden rounded-3xl"
    >
      <img
        :src="hero.imageUrl"
        :alt="hero.title"
        class="w-full h-full object-cover"
        fetchpriority="high"
      />

      <div class="absolute bottom-10 left-10 text-white">
        <div class="text-3xl md:text-5xl lg:text-6xl font-light">
          {{ hero.title }}
        </div>
        <div class="mt-3 text-sm opacity-80">
          {{ hero.subtitle }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { HeroContent } from '@/types'
import { useFadeUpOnScroll } from '@/composables/useGsapAnimation'

defineProps<{ hero: HeroContent }>()

const sectionRef = ref<HTMLElement | null>(null)
useFadeUpOnScroll(sectionRef)
</script>
