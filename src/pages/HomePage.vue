<template>
  <main>
    <HeroSection :hero="hero" @view="openHero" />
    <div class="md:hidden px-6 pb-12 text-center">
      <p class="text-sm text-gray-500">我们已经在一起 {{ togetherText }}</p>
      <p class="mt-2 text-sm text-gray-400">距离纪念日还有 {{ daysToAnniversary }} 天</p>
    </div>
    <LatestSection :photos="photos" @view="openViewer" />
    <AlbumsSection :albums="albums" />
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

import HeroSection from '@/components/sections/HeroSection.vue'
import LatestSection from '@/components/sections/LatestSection.vue'
import AlbumsSection from '@/components/sections/AlbumsSection.vue'

import { fetchLatestPhotos, fetchAlbums, fetchHero } from '@/api'
import { usePhotoViewer } from '@/composables/usePhotoViewer'
import { useAnniversary } from '@/composables/useAnniversary'
import type { Photo, Album, HeroContent } from '@/types'

const { open } = usePhotoViewer()
const { togetherText, daysToAnniversary } = useAnniversary()

const hero = ref<HeroContent>({ imageUrl: '', title: '', subtitle: '' })
const photos = ref<Photo[]>([])
const albums = ref<Album[]>([])

function openViewer(photo: Photo) {
  const index = photos.value.findIndex(p => p.id === photo.id)
  open(photos.value, index >= 0 ? index : 0)
}

function openHero(photo: Photo) {
  open([photo], 0)
}

onMounted(async () => {
  try {
    const [apiHero, apiPhotos, apiAlbums] = await Promise.all([
      fetchHero(),
      fetchLatestPhotos(12),
      fetchAlbums(),
    ])
    hero.value = apiHero
    photos.value = apiPhotos
    albums.value = apiAlbums
  } catch {
    // API 不可用，保持空状态
  }
})
</script>
