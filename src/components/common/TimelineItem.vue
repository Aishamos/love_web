<template>
  <div class="border-b pb-8 flex justify-between items-start">
    <div>
      <div class="text-lg md:text-xl font-light">{{ moment.title }}</div>
      <div class="text-gray-400 text-sm mt-2">
        {{ moment.location }} · {{ moment.date }}
      </div>
    </div>
    <div class="text-gray-400 text-sm mt-1">
      {{ moment.photoCount }} Photos
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Moment } from '@/types'
defineProps<{ moment: Moment }>()
</script>
