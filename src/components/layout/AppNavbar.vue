<template>
  <header class="fixed top-0 w-full bg-white/80 backdrop-blur z-50">
    <div class="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
      <div class="text-xl tracking-widest">
        OUR STORY
      </div>

      <nav v-if="isHome" class="hidden md:flex gap-10 text-sm text-gray-500">
        <RouterLink :to="{ hash: '#hero' }" class="hover:text-gray-900 transition-colors">首页</RouterLink>
        <RouterLink :to="{ hash: '#albums' }" class="hover:text-gray-900 transition-colors">相册</RouterLink>
        <RouterLink :to="{ hash: '#moments' }" class="hover:text-gray-900 transition-colors">旅行</RouterLink>
        <RouterLink :to="{ hash: '#moments' }" class="hover:text-gray-900 transition-colors">TodoList</RouterLink>
        <RouterLink to="/upload" class="hover:text-gray-900 transition-colors">上传</RouterLink>
      </nav>
      <RouterLink v-if="!isHome" to="/" class="hidden md:block text-sm text-gray-400 hover:text-gray-700 transition-colors">返回首页</RouterLink>

      <button class="md:hidden text-xl" @click="mobileOpen = true" aria-label="菜单">
        ☰
      </button>
    </div>

    <MobileMenu :open="mobileOpen" :is-home="isHome" @close="mobileOpen = false" />
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import MobileMenu from './MobileMenu.vue'

const route = useRoute()
const mobileOpen = ref(false)
const isHome = computed(() => route.path === '/')
</script>
