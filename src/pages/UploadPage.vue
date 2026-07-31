<template>
  <div class="bg-white" :class="authed ? 'min-h-screen' : 'h-dvh overflow-hidden'">
    <!-- 登录表单 -->
    <div
      v-if="!authed"
      class="h-full flex flex-col"
    >
      <div class="max-w-7xl mx-auto px-6 py-5 mb-6 flex justify-between items-center">
        <div class="text-xl tracking-widest">OUR GALLERY</div>
        <RouterLink to="/" class="text-sm text-gray-400 hover:text-gray-700 transition-colors">返回首页</RouterLink>
      </div>

      <div class="flex-1 flex items-center justify-center px-5">
        <form
          class="w-full max-w-sm"
          @submit.prevent="login"
        >
          <div class="text-center mb-12">
            <div class="text-sm text-gray-400">身份验证</div>
          </div>

        <div v-if="loginError" class="text-red-500 text-sm text-center mb-6">
          {{ loginError }}
        </div>

        <input
          v-model="username"
          type="text"
          placeholder="账号"
          class="w-full border border-gray-200 rounded-xl px-4 py-3 mb-4 text-sm focus:outline-none focus:border-gray-400 transition-colors"
          autocomplete="username"
        />
        <input
          v-model="password"
          type="password"
          placeholder="密码"
          class="w-full border border-gray-200 rounded-xl px-4 py-3 mb-6 text-sm focus:outline-none focus:border-gray-400 transition-colors"
          autocomplete="current-password"
        />
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-gray-900 text-white rounded-xl py-3 text-sm hover:bg-gray-800 transition-colors disabled:opacity-50"
          >
            {{ loading ? '验证中...' : '登录' }}
          </button>
        </form>
      </div>
    </div>

    <!-- 上传界面 -->
    <div v-else class="max-w-7xl mx-auto px-6 py-5">
      <!-- 顶栏 -->
      <div class="flex justify-between items-center mb-12">
        <div class="text-xl tracking-widest">OUR GALLERY</div>
        <button
          class="text-sm text-gray-400 hover:text-gray-700 transition-colors"
          @click="goHome"
        >
          返回首页
        </button>
      </div>

      <!-- 拖拽区域 -->
      <div
        class="border-2 border-dashed border-gray-200 rounded-3xl p-12 text-center cursor-pointer hover:border-gray-400 transition-colors"
        :class="{ 'border-gray-900 bg-gray-50': dragging }"
        @dragover.prevent="dragging = true"
        @dragleave="dragging = false"
        @drop.prevent="handleDrop"
        @click="fileInput?.click()"
      >
        <div class="text-4xl mb-4 text-gray-300">+</div>
        <div class="text-sm text-gray-400">拖拽图片到此处，或点击选择</div>
        <div class="text-xs text-gray-300 mt-2">支持 JPG / PNG / WebP</div>
      </div>

      <input
        ref="fileInput"
        type="file"
        multiple
        accept="image/jpeg,image/png,image/webp"
        class="hidden"
        @change="handleFiles"
      />

      <!-- 预览 -->
      <div v-if="previews.length" class="grid grid-cols-3 md:grid-cols-4 gap-3 mt-8">
        <div
          v-for="(p, i) in previews"
          :key="i"
          class="relative rounded-2xl overflow-hidden aspect-square group"
        >
          <img :src="p.url" class="w-full h-full object-cover" />
          <button
            class="absolute top-2 right-2 w-6 h-6 bg-black/50 rounded-full text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity"
            @click.stop="removePreview(i)"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- 元数据表单 -->
      <div v-if="previews.length" class="mt-10 space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div>
            <label class="block text-xs text-gray-400 mb-2">季节</label>
            <select
              v-model="season"
              class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-400 transition-colors bg-white"
            >
              <option value="">选择季节</option>
              <option value="spring">春</option>
              <option value="summer">夏</option>
              <option value="autumn">秋</option>
              <option value="winter">冬</option>
            </select>
          </div>
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
              placeholder="如 2025.03"
              class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-400 transition-colors"
            />
          </div>
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
            {{ uploading ? `上传中 ${progress}%` : `上传 ${files.length} 张图片` }}
          </button>
          <button
            class="px-6 border border-gray-200 rounded-xl py-3 text-sm text-gray-500 hover:border-gray-400 transition-colors"
            @click="clearAll"
          >
            清除
          </button>
        </div>

        <div v-if="uploadMsg" class="text-sm text-center" :class="uploadOk ? 'text-green-600' : 'text-red-500'">
          {{ uploadMsg }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import type { Album } from '@/types'

const authed = ref(false)
const username = ref('')
const password = ref('')
const loading = ref(false)
const loginError = ref('')

const files = ref<File[]>([])
const previews = ref<{ url: string; file: File }[]>([])
const dragging = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const season = ref('')
const region = ref('')
const photoDate = ref('')
const albumId = ref('')
const albums = ref<Album[]>([])

const uploading = ref(false)
const progress = ref(0)
const uploadMsg = ref('')
const uploadOk = ref(false)

onMounted(async () => {
  const res = await fetch('/api/auth/check', { credentials: 'same-origin' })
  if (res.ok) {
    const json = await res.json()
    authed.value = json.code === 0
  }
  if (authed.value) {
    try {
      const r = await fetch('/api/albums')
      const j = await r.json()
      if (j.code === 0) albums.value = j.data
    } catch {}
  }
})

async function login() {
  if (!username.value || !password.value) {
    loginError.value = '请输入账号和密码'
    return
  }
  loading.value = true
  loginError.value = ''

  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin',
    body: JSON.stringify({ username: username.value, password: password.value }),
  })

  if (res.ok) {
    authed.value = true
    try {
      const r = await fetch('/api/albums')
      const j = await r.json()
      if (j.code === 0) albums.value = j.data
    } catch {}
  } else {
    loginError.value = '账号或密码错误'
  }
  loading.value = false
}

const router = useRouter()

function goHome() {
  router.push('/')
}

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
  for (let i = 0; i < fileList.length; i++) {
    const f = fileList[i]
    if (!f.type.startsWith('image/')) continue
    files.value.push(f)
    previews.value.push({ url: URL.createObjectURL(f), file: f })
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
  uploadMsg.value = ''
}

async function doUpload() {
  if (!files.value.length) return
  uploading.value = true
  progress.value = 0
  uploadMsg.value = ''

  const formData = new FormData()
  files.value.forEach(f => formData.append('files', f))
  formData.append('season', season.value)
  formData.append('region', region.value)
  formData.append('photoDate', photoDate.value)
  formData.append('albumId', albumId.value)

  try {
    const res = await fetch('/api/upload', {
      method: 'POST',
      credentials: 'same-origin',
      body: formData,
    })

    const json = await res.json()
    uploading.value = false
    uploadOk.value = json.code === 0
    uploadMsg.value = json.message

    if (json.code === 0) {
      setTimeout(() => clearAll(), 1500)
    } else if (res.status === 401) {
      // session 过期
      authed.value = false
      clearAll()
    }
  } catch {
    uploading.value = false
    uploadMsg.value = '网络错误，请重试'
    uploadOk.value = false
  }
}
</script>
