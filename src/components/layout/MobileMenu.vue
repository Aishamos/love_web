<template>
  <Teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 z-[100]"
      @click.self="$emit('close')"
    >
      <div class="absolute inset-0 bg-black/40" />

      <div
        ref="panelRef"
        class="absolute top-0 right-0 h-full w-64 bg-white shadow-xl flex flex-col p-8 pt-20"
      >
        <button
          class="absolute top-6 right-6 text-2xl text-gray-400 hover:text-gray-900 transition-colors"
          @click="$emit('close')"
          aria-label="关闭"
        >
          ✕
        </button>

        <nav v-if="isHome" class="flex flex-col gap-6 text-xl font-light text-gray-700">
          <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="closeAndScroll('#hero')">首页</a>
          <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="closeAndScroll('#albums')">相册</a>
          <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="closeAndScroll('#moments')">旅行</a>
          <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="goPage('/upload')">上传</a>
        </nav>
        <nav v-else class="flex flex-col gap-6 text-xl font-light text-gray-700">
          <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="goPage('/')">返回首页</a>
        </nav>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps<{ open: boolean; isHome: boolean }>()
const emit = defineEmits<{ close: [] }>()

const router = useRouter()
const panelRef = ref<HTMLElement | null>(null)

function closeAndScroll(hash: string) {
  emit('close')
  const el = document.querySelector(hash)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

function goPage(path: string) {
  emit('close')
  router.push(path)
}

watch(() => props.open, (val) => {
  document.body.style.overflow = val ? 'hidden' : ''
})
</script>
