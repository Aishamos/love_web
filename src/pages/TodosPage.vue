<template>
  <main class="pt-24 pb-16 min-h-screen">
    <div class="max-w-7xl mx-auto px-6">
      <h1 class="text-lg font-light mb-10">TodoList</h1>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- 未完成：全部 -->
        <div>
          <div class="mb-4 text-sm text-gray-400">未完成 ({{ pending.length }})</div>
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

        <!-- 已完成：全部 -->
        <div>
          <div class="mb-4 text-sm text-gray-400">已完成 ({{ completed.length }})</div>
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

      <!-- 添加新事项 -->
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
          {{ adding ? '添加中...' : '添加' }}
        </button>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useTodos } from '@/composables/useTodos'

const {
  pending,
  completed,
  newContent,
  adding,
  formatDoneTime,
  loadTodos,
  onAdd,
  onToggle,
} = useTodos({ redirect: '/todos' })

onMounted(loadTodos)
</script>
