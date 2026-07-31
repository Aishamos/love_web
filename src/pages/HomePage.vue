<template>
  <main>
    <HeroSection :hero="hero" />
    <MomentsSection :moments="moments" />
    <LatestSection :photos="photos" @view="openViewer" />
    <AlbumsSection :albums="albums" />
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

import HeroSection from '@/components/sections/HeroSection.vue'
import MomentsSection from '@/components/sections/MomentsSection.vue'
import LatestSection from '@/components/sections/LatestSection.vue'
import AlbumsSection from '@/components/sections/AlbumsSection.vue'

import { fetchLatestPhotos, fetchAlbums, fetchMoments, fetchHero } from '@/api'
import { usePhotoViewer } from '@/composables/usePhotoViewer'
import type { Photo, Album, Moment, HeroContent } from '@/types'

const { open } = usePhotoViewer()

const hero = ref<HeroContent>({ imageUrl: '', title: '', subtitle: '' })
const moments = ref<Moment[]>([])
const photos = ref<Photo[]>([])
const albums = ref<Album[]>([])

function openViewer(photo: Photo) {
  const index = photos.value.findIndex(p => p.id === photo.id)
  open(photos.value, index >= 0 ? index : 0)
}

onMounted(async () => {
  try {
    const [apiHero, apiPhotos, apiAlbums, apiMoments] = await Promise.all([
      fetchHero(),
      fetchLatestPhotos(12),
      fetchAlbums(),
      fetchMoments(),
    ])
    hero.value = apiHero
    photos.value = apiPhotos
    albums.value = apiAlbums
    moments.value = apiMoments
  } catch {
    // API 不可用，保持空状态
  }
})
</script>
