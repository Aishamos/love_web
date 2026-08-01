<template>
  <div class="bg-white h-dvh overflow-hidden">
    <div class="h-full flex flex-col">
      <div class="flex-1 flex items-center justify-center px-5 pt-16 md:pt-24">
        <form
          class="w-full max-w-sm md:pt-24"
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
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { setLoggedIn } = useAuth()
const username = ref('')
const password = ref('')
const loading = ref(false)
const loginError = ref('')

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
    setLoggedIn(true)
    router.push('/upload')
  } else {
    loginError.value = '账号或密码错误'
  }
  loading.value = false
}
</script>
