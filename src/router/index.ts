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
      path: '/photos',
      name: 'photos',
      component: () => import('@/pages/PhotosPage.vue'),
    },
    {
      path: '/todos',
      name: 'todos',
      component: () => import('@/pages/TodosPage.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/LoginPage.vue'),
    },
  ],
  scrollBehavior(to, from) {
    if (to.hash) {
      // 刷新/首次加载或跨页面导航（如登录后跳回）时，目标页面组件会重新挂载，
      // 滚动交给组件在数据加载完成后统一执行，避免与 scrollBehavior 产生两次目标不同的滚动竞争。
      if (from.name === undefined || from.path !== to.path) {
        return false
      }
      // 同页面 hash 导航（如菜单栏点击）：页面已就绪，直接平滑滚动
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
