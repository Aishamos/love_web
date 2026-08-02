import { createRouter, createWebHistory } from 'vue-router'
import { checkAuth } from '@/composables/useAuth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/pages/HomePage.vue'),
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('@/pages/UploadPage.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/LoginPage.vue'),
    },
  ],
  scrollBehavior(to) {
    if (to.hash) {
      const el = document.querySelector(to.hash)
      if (el) {
        const top = el.getBoundingClientRect().top + window.scrollY - 96
        return { top, behavior: 'smooth' }
      }
      return { top: 0 }
    }
    return { top: 0 }
  },
})

router.beforeEach(async (to) => {
  if (to.path === '/upload') {
    const ok = await checkAuth()
    if (!ok) return { path: '/login', query: { redirect: to.fullPath } }
  }
})

export default router
