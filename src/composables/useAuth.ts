import { ref } from 'vue'

const isLoggedIn = ref<boolean | null>(null)

export async function checkAuth(): Promise<boolean> {
  if (isLoggedIn.value !== null) return isLoggedIn.value
  try {
    const res = await fetch('/api/auth/check', { credentials: 'same-origin' })
    isLoggedIn.value = res.ok ? (await res.json()).code === 0 : false
  } catch {
    isLoggedIn.value = false
  }
  return isLoggedIn.value
}

export function useAuth() {
  return { isLoggedIn, checkAuth, setLoggedIn: (v: boolean) => { isLoggedIn.value = v } }
}
