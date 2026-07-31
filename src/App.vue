<template>
  <div>
    <AppNavbar v-if="!isUploadPage" />
    <RouterView />
    <AppFooter v-if="!isUploadPage" />
    <PhotoViewer />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import PhotoViewer from '@/components/viewer/PhotoViewer.vue'

const route = useRoute()
const isUploadPage = computed(() => route.path === '/upload')
</script>
