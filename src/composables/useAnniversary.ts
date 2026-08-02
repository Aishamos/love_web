import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ANNIVERSARY_START, ANNIVERSARY_MONTH, ANNIVERSARY_DAY } from '@/data/anniversary'

export function useAnniversary() {
  const now = ref(new Date())
  let timer: number | undefined

  onMounted(() => {
    timer = window.setInterval(() => { now.value = new Date() }, 60000)
  })
  onUnmounted(() => {
    window.clearInterval(timer)
  })

  const totalDays = computed(() =>
    Math.max(0, Math.floor((now.value.getTime() - ANNIVERSARY_START.getTime()) / 86400000))
  )
  const togetherYears = computed(() => Math.floor(totalDays.value / 365))
  const togetherDays = computed(() => totalDays.value % 365)
  const togetherText = computed(() =>
    togetherYears.value > 0
      ? `${togetherYears.value} 年 ${togetherDays.value} 天`
      : `${togetherDays.value} 天`
  )

  const daysToAnniversary = computed(() => {
    const y = now.value.getFullYear()
    let next = new Date(y, ANNIVERSARY_MONTH - 1, ANNIVERSARY_DAY)
    if (next.getTime() < now.value.getTime()) {
      next = new Date(y + 1, ANNIVERSARY_MONTH - 1, ANNIVERSARY_DAY)
    }
    return Math.ceil((next.getTime() - now.value.getTime()) / 86400000)
  })

  return { togetherYears, togetherDays, togetherText, daysToAnniversary }
}
