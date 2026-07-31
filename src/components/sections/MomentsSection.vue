<template>
  <section id="moments" class="max-w-5xl mx-auto px-6 py-24">
    <h2 ref="titleRef" class="text-2xl md:text-3xl font-light mb-12">
      Moments
    </h2>

    <div ref="listRef" class="space-y-8">
      <TimelineItem
        v-for="moment in moments"
        :key="moment.id"
        :moment="moment"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Moment } from '@/types'
import TimelineItem from '@/components/common/TimelineItem.vue'
import { useFadeUpOnScroll } from '@/composables/useGsapAnimation'

defineProps<{ moments: Moment[] }>()

const titleRef = ref<HTMLElement | null>(null)
const listRef = ref<HTMLElement | null>(null)

useFadeUpOnScroll(titleRef)
useFadeUpOnScroll(listRef, { stagger: 0.15 })
</script>
