<template>
  <main>
    <HeroSection :hero="hero" @view="openHero" />
    <div class="md:hidden px-6 pb-12 text-center">
      <p class="text-sm text-gray-500">我们已经在一起 {{ togetherText }}</p>
      <p class="mt-2 text-sm text-gray-400">距离纪念日还有 {{ daysToAnniversary }} 天</p>
    </div>
    <LatestSection :photos="photos" @view="openViewer" @view-all="goAllPhotos" />
    <TodoSection />
    <AlbumsSection :albums="albums" />
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import HeroSection from '@/components/sections/HeroSection.vue'
import LatestSection from '@/components/sections/LatestSection.vue'
import TodoSection from '@/components/sections/TodoSection.vue'
import AlbumsSection from '@/components/sections/AlbumsSection.vue'

import { fetchLatestPhotos, fetchAlbums, fetchHero } from '@/api'
import { usePhotoViewer } from '@/composables/usePhotoViewer'
import { useAnniversary } from '@/composables/useAnniversary'
import type { Photo, Album, HeroContent } from '@/types'

const route = useRoute()
const router = useRouter()
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

function goAllPhotos() {
  router.push('/photos')
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
  // 刷新/首次加载时按 URL hash 定位区块（弥补首次导航 scrollBehavior 不可靠）
  if (route.hash) {
    await nextTick()
    // 等待页面切换过渡动画结束，避免 transform 干扰元素位置计算
    await new Promise((resolve) => setTimeout(resolve, 300))
    const el = document.querySelector(route.hash)
    if (el) {
      const top = el.getBoundingClientRect().top + window.scrollY - 96
      window.scrollTo({ top, behavior: 'smooth' })
    }
  }
})
</script>
