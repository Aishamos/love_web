<template>
  <header class="fixed top-0 w-full bg-white/80 backdrop-blur z-50">
    <div class="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
      <div class="text-xl tracking-widest">
        OUR GALLERY
      </div>

      <nav class="hidden md:flex gap-10 text-sm text-gray-500">
        <RouterLink :to="{ hash: '#hero' }" class="hover:text-gray-900 transition-colors">首页</RouterLink>
        <RouterLink :to="{ hash: '#albums' }" class="hover:text-gray-900 transition-colors">相册</RouterLink>
        <RouterLink :to="{ hash: '#moments' }" class="hover:text-gray-900 transition-colors">旅行</RouterLink>
        <RouterLink :to="{ hash: '#moments' }" class="hover:text-gray-900 transition-colors">时间</RouterLink>
        <RouterLink to="/upload" class="hover:text-gray-900 transition-colors">上传</RouterLink>
      </nav>

      <button class="md:hidden text-xl" @click="mobileOpen = true" aria-label="菜单">
        ☰
      </button>
    </div>

    <MobileMenu :open="mobileOpen" @close="mobileOpen = false" />
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import MobileMenu from './MobileMenu.vue'

const mobileOpen = ref(false)
</script>
