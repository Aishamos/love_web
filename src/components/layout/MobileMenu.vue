<template>
  <Teleport to="body">
    <Transition name="menu">
      <div
        v-if="open"
        class="fixed inset-0 z-[100] bg-black/40"
        @click.self="$emit('close')"
      >
        <div class="mobile-menu-panel absolute top-0 right-0 h-full w-[150px] bg-white shadow-xl flex flex-col p-8 pt-20">
          <button
            class="absolute top-6 right-6 text-2xl text-gray-400 hover:text-gray-900 transition-colors"
            @click="$emit('close')"
            aria-label="关闭"
          >
            ✕
          </button>

          <nav v-if="isHome" class="flex flex-col gap-6 text-xl font-light text-gray-700">
            <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="closeAndScroll('#hero')">首页</a>
            <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="closeAndScroll('#moments')">TodoList</a>
            <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="closeAndScroll('#albums')">相册</a>
            <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="goPage('/upload')">上传</a>
          </nav>
          <nav v-else class="flex flex-col gap-6 text-xl font-light text-gray-700">
            <a class="hover:text-gray-900 transition-colors cursor-pointer" @click="goPage('/')">返回首页</a>
          </nav>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps<{ open: boolean; isHome: boolean }>()
const emit = defineEmits<{ close: [] }>()

const router = useRouter()

function closeAndScroll(hash: string) {
  emit('close')
  const el = document.querySelector(hash)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

function goPage(path: string) {
  emit('close')
  router.push(path)
}

// 路由变化时兜底关闭，避免菜单打开状态残留
watch(() => router.currentRoute.value.fullPath, () => emit('close'))

watch(() => props.open, (val) => {
  document.body.style.overflow = val ? 'hidden' : ''
})
</script>

<style>
.menu-enter-active,
.menu-leave-active {
  transition: opacity 0.3s ease;
}
.menu-enter-from,
.menu-leave-to {
  opacity: 0;
}
.menu-enter-active .mobile-menu-panel,
.menu-leave-active .mobile-menu-panel {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.menu-enter-from .mobile-menu-panel,
.menu-leave-to .mobile-menu-panel {
  transform: translateX(100%);
}
</style>
