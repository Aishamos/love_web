<template>
  <main class="pt-24 pb-16 min-h-screen">
    <div class="max-w-7xl mx-auto px-6">
      <!-- 标题栏：与首页区块风格一致 -->
      <div class="mb-10">
        <h1 v-if="!albumNotFound" class="text-lg font-light">
          {{ title }}
          <span v-if="total" class="text-base text-gray-400 ml-2">{{ total }}</span>
        </h1>
        <p v-if="albumDescription" class="mt-2 text-sm text-gray-400">{{ albumDescription }}</p>
      </div>

      <!-- 相册不存在 -->
      <div v-if="albumNotFound" class="py-20 text-center text-sm text-gray-300">
        相册不存在
      </div>

      <!-- 照片网格 -->
      <div
        v-else-if="photos.length"
        class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-5"
      >
        <PhotoCard
          v-for="(photo, index) in photos"
          :key="photo.id"
          :photo="photo"
          @click="openViewer(index)"
        />
      </div>

      <!-- 首屏加载中 -->
      <div v-else-if="loading" class="py-20 text-center text-sm text-gray-400">
        加载中...
      </div>

      <!-- 空状态 -->
      <div v-else class="py-20 text-center text-sm text-gray-300">
        {{ albumId ? '该相册暂无照片' : '暂无照片，去上传吧' }}
      </div>

      <!-- 底部哨兵：进入视口触发加载下一页 -->
      <div v-if="!albumNotFound" ref="sentinelRef" class="pt-10">
        <div v-if="loading" class="text-center text-sm text-gray-400">加载中...</div>
        <div v-else-if="error" class="text-center text-sm text-red-400">
          {{ error }}
          <button class="underline ml-2" @click="loadMore">重试</button>
        </div>
        <div v-else-if="!hasMore && photos.length" class="text-center text-sm text-gray-300">
          已加载全部
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import PhotoCard from '@/components/common/PhotoCard.vue'
import { fetchPhotos, fetchAlbum } from '@/api'
import { usePhotoViewer } from '@/composables/usePhotoViewer'
import type { Photo } from '@/types'

const PAGE_SIZE = 20

const route = useRoute()
const { open } = usePhotoViewer()

const albumId = computed(() => {
  const id = route.params.id
  return id ? Number(id) : undefined
})
const albumTitle = ref('')
const albumDescription = ref('')
const albumNotFound = ref(false)
const photos = ref<Photo[]>([])
const total = ref(0)
const page = ref(0)
const hasMore = ref(true)
const loading = ref(false)
const error = ref('')
const sentinelRef = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | null = null

const title = computed(() => (albumId.value ? albumTitle.value : 'All Photos'))

function openViewer(index: number) {
  open(photos.value, index)
}

async function loadMore() {
  if (loading.value || !hasMore.value) return
  loading.value = true
  error.value = ''
  try {
    const data = await fetchPhotos(albumId.value, page.value + 1, PAGE_SIZE)
    photos.value.push(...data.items)
    total.value = data.total
    hasMore.value = data.hasMore
    page.value += 1
  } catch {
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (albumId.value) {
    try {
      const album = await fetchAlbum(albumId.value)
      albumTitle.value = album.title
      albumDescription.value = album.description ?? ''
    } catch {
      albumNotFound.value = true
      return
    }
  }
  await loadMore()
  observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) loadMore()
    },
    { rootMargin: '300px' }
  )
  if (sentinelRef.value) observer.observe(sentinelRef.value)
})

onUnmounted(() => {
  observer?.disconnect()
})
</script>
