import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { fetchTodos, createTodo, toggleTodo } from '@/api'
import type { Todo } from '@/types'

interface UseTodosOptions {
  /** 未登录时跳转登录页的 redirect 地址 */
  redirect: string
  /** 登录成功后的锚点定位（可选） */
  anchor?: string
}

export function useTodos(options: UseTodosOptions) {
  const router = useRouter()
  const { checkAuth } = useAuth()

  const todos = ref<Todo[]>([])
  const newContent = ref('')
  const adding = ref(false)

  const pending = computed(() => todos.value.filter((t) => !t.done))
  const completed = computed(() =>
    todos.value
      .filter((t) => t.done)
      .sort((a, b) => (b.doneTime ?? '').localeCompare(a.doneTime ?? ''))
  )

  function formatDoneTime(iso: string | null | undefined): string {
    if (!iso) return ''
    const d = new Date(iso)
    if (isNaN(d.getTime())) return ''
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const hh = String(d.getHours()).padStart(2, '0')
    const mm = String(d.getMinutes()).padStart(2, '0')
    return `${y}.${m}.${day} ${hh}:${mm}`
  }

  async function loadTodos() {
    try {
      todos.value = await fetchTodos()
    } catch {
      // 保持空列表
    }
  }

  async function ensureLogin(): Promise<boolean> {
    if (await checkAuth()) return true
    router.push({
      path: '/login',
      query: { redirect: options.redirect, ...(options.anchor ? { anchor: options.anchor } : {}) },
    })
    return false
  }

  async function onAdd() {
    const content = newContent.value.trim()
    if (!content || adding.value) return
    if (!(await ensureLogin())) return
    adding.value = true
    try {
      const t = await createTodo(content)
      todos.value = [t, ...todos.value]
      newContent.value = ''
    } catch {
      // 失败保持现状
    } finally {
      adding.value = false
    }
  }

  async function onToggle(todo: Todo) {
    if (!(await ensureLogin())) return
    const msg = todo.done ? '确认取消该事项的完成？' : '确认完成该事项？'
    if (!window.confirm(msg)) return
    const prev = todo.done
    const prevDoneTime = todo.doneTime
    todo.done = !prev
    todo.doneTime = todo.done ? new Date().toISOString() : null
    try {
      const updated = await toggleTodo(todo.id, todo.done)
      todo.doneTime = updated.doneTime
    } catch {
      todo.done = prev
      todo.doneTime = prevDoneTime
    }
  }

  return {
    todos,
    newContent,
    adding,
    pending,
    completed,
    formatDoneTime,
    loadTodos,
    onAdd,
    onToggle,
  }
}
