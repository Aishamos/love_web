<template>
  <div class="bg-white flex-1">
    <Transition name="toast">
      <div
        v-if="toast.show"
        class="fixed top-6 left-1/2 -translate-x-1/2 z-50 px-5 py-2.5 rounded-full text-white text-sm shadow-lg"
        :class="toast.type === 'error' ? 'bg-red-600' : 'bg-green-600'"
      >
        {{ toast.msg }}
      </div>
    </Transition>

    <div class="h-full flex flex-col md:pt-32 md:max-w-2xl md:mx-auto md:px-0 pt-24  px-6">
      <!-- 上传/预览区：未选图显示提示框，选图后图片覆盖此框 -->
      <div
        class="group border-2 border-dashed border-gray-200 rounded-3xl overflow-hidden cursor-pointer hover:border-gray-400 transition-colors"
        :class="{ 'border-gray-900 bg-gray-50': dragging }"
        @dragover.prevent="dragging = true"
        @dragleave="dragging = false"
        @drop.prevent="handleDrop"
        @click="fileInput?.click()"
      >
        <div v-if="!previews.length" class="p-12 text-center">
          <div class="text-4xl mb-4 text-gray-300">+</div>
          <div class="text-sm text-gray-400">拖拽单张图片到此处，或点击选择</div>
          <div class="text-xs text-gray-300 mt-2">支持 JPG / PNG / WebP</div>
        </div>

        <div v-else class="relative aspect-square">
          <img :src="previews[0].url" class="w-full h-full object-cover" />
          <button
            class="absolute top-3 right-3 w-8 h-8 bg-black/60 rounded-full text-white text-sm transition-opacity"
            @click.stop="removePreview(0)"
            aria-label="移除"
          >
            ✕
          </button>
          <div class="absolute bottom-3 inset-x-0 text-center text-white text-xs bg-black/40 py-1.5">
            点击更换图片
          </div>
        </div>
      </div>

      <input
        ref="fileInput"
        type="file"
        accept="image/jpeg,image/png,image/webp"
        class="hidden"
        @change="handleFiles"
      />

      <!-- 元数据表单 -->
      <div v-if="previews.length" class="mt-10 space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="block text-xs text-gray-400 mb-2">地区</label>
            <input
              v-model="region"
              type="text"
              placeholder="如 Tokyo"
              class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-400 transition-colors"
            />
          </div>
          <div>
            <label class="block text-xs text-gray-400 mb-2">时间</label>
            <input
              v-model="photoDate"
              type="text"
              placeholder="如 2025.03.14"
              class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-400 transition-colors"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs text-gray-400 mb-2">备注</label>
          <input
            v-model="remark"
            type="text"
            placeholder="备注，如拍摄故事/地点细节"
            class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-400 transition-colors"
          />
        </div>

        <div>
          <label class="block text-xs text-gray-400 mb-2">归属相册</label>
          <select
            v-model="albumId"
            class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-400 transition-colors bg-white"
          >
            <option value="">不归入相册</option>
            <option v-for="a in albums" :key="a.id" :value="a.id">{{ a.title }}</option>
          </select>
        </div>

        <div class="flex gap-4">
          <button
            :disabled="uploading"
            class="flex-1 bg-gray-900 text-white rounded-xl py-3 text-sm hover:bg-gray-800 transition-colors disabled:opacity-50"
            @click="doUpload"
          >
            {{ uploading ? `上传中 ${progress}%` : '上传图片' }}
          </button>
          <button
            class="px-6 border border-gray-200 rounded-xl py-3 text-sm text-gray-500 hover:border-gray-400 transition-colors"
            @click="clearAll"
          >
            清除
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { fetchAlbums, uploadPhotos, ApiError } from '@/api'
import { parse as parseExif } from 'exifr'
import type { Album } from '@/types'

const { checkAuth, setLoggedIn } = useAuth()

const MAX_SIZE = 16 * 1024 * 1024

const files = ref<File[]>([])
const previews = ref<{ url: string; file: File }[]>([])
const dragging = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
let exifSeq = 0

const remark = ref('')
const region = ref('')
const photoDate = ref('')
const albumId = ref('')
const albums = ref<Album[]>([])

const uploading = ref(false)
const progress = ref(0)
const toast = ref<{ show: boolean; msg: string; type: 'success' | 'error' }>({ show: false, msg: '', type: 'success' })
let toastTimer: number | undefined

const router = useRouter()

function showToast(msg: string, type: 'success' | 'error' = 'success', duration = 3000) {
  toast.value = { show: true, msg, type }
  window.clearTimeout(toastTimer)
  toastTimer = window.setTimeout(() => { toast.value.show = false }, duration)
}

onMounted(async () => {
  if (!(await checkAuth())) {
    router.replace('/login')
    return
  }
  try {
    albums.value = await fetchAlbums()
  } catch {}
})

onUnmounted(() => {
  previews.value.forEach(p => URL.revokeObjectURL(p.url))
  window.clearTimeout(toastTimer)
})

function handleDrop(e: DragEvent) {
  dragging.value = false
  if (e.dataTransfer?.files) addFiles(e.dataTransfer.files)
}

function handleFiles(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files) addFiles(target.files)
  target.value = ''
}

function addFiles(fileList: FileList) {
  const f = fileList[0]
  if (!f || !f.type.startsWith('image/')) return
  if (f.size > MAX_SIZE) {
    showToast('图片超过 16MB，无法上传', 'error', 4000)
    return
  }
  // 单图模式：替换已有选择，并清空上一张的元数据
  clearAll()
  files.value.push(f)
  previews.value.push({ url: URL.createObjectURL(f), file: f })
  fillDateFromExif(f)
}

async function fillDateFromExif(file: File) {
  const seq = ++exifSeq
  try {
    const exif = await parseExif(file, { pick: ['DateTimeOriginal'] })
    if (seq !== exifSeq) return
    const d = exif?.DateTimeOriginal
    if (d instanceof Date && !isNaN(d.getTime())) {
      const y = d.getFullYear()
      const m = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      if (!photoDate.value) photoDate.value = `${y}.${m}.${day}`
    }
  } catch {
    // 无 EXIF 或解析失败，保持手动填写
  }
}

function removePreview(i: number) {
  URL.revokeObjectURL(previews.value[i].url)
  previews.value.splice(i, 1)
  files.value.splice(i, 1)
}

function clearAll() {
  previews.value.forEach(p => URL.revokeObjectURL(p.url))
  previews.value = []
  files.value = []
  remark.value = ''
  region.value = ''
  photoDate.value = ''
  albumId.value = ''
}

async function doUpload() {
  if (!files.value.length) return

  uploading.value = true
  progress.value = 0

  const formData = new FormData()
  files.value.forEach(f => formData.append('files', f))
  formData.append('remark', remark.value)
  formData.append('region', region.value)
  formData.append('photoDate', photoDate.value)
  formData.append('albumId', albumId.value)

  try {
    await uploadPhotos(formData, (p) => { progress.value = p })
    showToast('上传成功')
    setTimeout(() => clearAll(), 800)
  } catch (err) {
    if (err instanceof ApiError && err.status === 401) {
      setLoggedIn(false)
      router.replace({ path: '/login', query: { redirect: '/upload' } })
      clearAll()
    } else {
      showToast(err instanceof Error ? err.message : '上传失败，请重试', 'error', 4000)
    }
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
