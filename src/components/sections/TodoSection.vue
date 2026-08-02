<template>
  <section id="todo" class="max-w-7xl mx-auto px-6 py-12">
    <div ref="headerRef" class="flex justify-between mb-10">
      <h2 class="text-2xl md:text-3xl font-light">TodoList</h2>
      <button class="text-sm border rounded-full px-5 py-2 hover:bg-gray-50 transition-colors">View All</button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
      <div>
        <div class="mb-4 text-sm text-gray-400">未完成</div>
        <ul v-if="pending.length" class="space-y-3">
          <li
            v-for="t in pending"
            :key="t.id"
            class="flex items-center gap-3 bg-white border border-gray-100 rounded-xl px-4 py-3"
          >
            <input
              type="checkbox"
              :checked="t.done"
              class="w-4 h-4 accent-gray-900 cursor-pointer"
              @click.prevent="onToggle(t)"
            />
            <span class="text-sm text-gray-700">{{ t.content }}</span>
          </li>
        </ul>
        <p v-else class="text-sm text-gray-300">暂无未完成事项</p>
      </div>

      <div>
        <div class="mb-4 text-sm text-gray-400">已完成</div>
        <ul v-if="completed.length" class="space-y-3">
          <li
            v-for="t in completed"
            :key="t.id"
            class="flex items-center gap-3 bg-white border border-gray-100 rounded-xl px-4 py-3"
          >
            <input
              type="checkbox"
              :checked="t.done"
              class="w-4 h-4 accent-gray-900 cursor-pointer"
              @click.prevent="onToggle(t)"
            />
            <span class="text-sm text-gray-400 line-through">{{ t.content }}</span>
            <span class="ml-auto text-xs text-gray-300">{{ formatDoneTime(t.doneTime) }}</span>
          </li>
        </ul>
        <p v-else class="text-sm text-gray-300">暂无已完成事项</p>
      </div>
    </div>

    <div class="mt-8 flex gap-3">
      <input
        v-model="newContent"
        type="text"
        placeholder="输入新的事项..."
        class="flex-1 border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-gray-400 transition-colors"
        @keyup.enter="onAdd"
      />
      <button
        class="px-6 bg-gray-900 text-white rounded-xl py-3 text-sm hover:bg-gray-800 transition-colors disabled:opacity-50"
        :disabled="!newContent.trim() || adding"
        @click="onAdd"
      >
        添加
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { fetchTodos, createTodo, toggleTodo } from '@/api'
import { useFadeUpOnScroll } from '@/composables/useGsapAnimation'
import type { Todo } from '@/types'

const router = useRouter()
const { checkAuth } = useAuth()

const todos = ref<Todo[]>([])
const newContent = ref('')
const adding = ref(false)

const pending = computed(() => todos.value.filter(t => !t.done).slice(0, 5))
const completed = computed(() =>
  todos.value
    .filter(t => t.done)
    .sort((a, b) => (b.doneTime ?? '').localeCompare(a.doneTime ?? ''))
    .slice(0, 5)
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

const headerRef = ref<HTMLElement | null>(null)
useFadeUpOnScroll(headerRef)

async function loadTodos() {
  try {
    todos.value = await fetchTodos()
  } catch {}
}

async function ensureLogin(): Promise<boolean> {
  if (await checkAuth()) return true
  router.push('/login')
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
  } catch {} finally {
    adding.value = false
  }
}

async function onToggle(todo: Todo) {
  if (!(await ensureLogin())) return
  // 完成/撤销完成都弹确认
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

onMounted(loadTodos)
</script>
