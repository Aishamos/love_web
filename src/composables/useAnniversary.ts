import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  ANNIVERSARY_START,
  ANNIVERSARY_MONTH,
  ANNIVERSARY_DAY,
  MEETING_DATE,
} from '@/data/anniversary'

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
  // 只显示总天数，不折算成年
  const togetherText = computed(() => `${totalDays.value} 天`)

  const daysToAnniversary = computed(() => {
    const y = now.value.getFullYear()
    let next = new Date(y, ANNIVERSARY_MONTH - 1, ANNIVERSARY_DAY)
    if (next.getTime() < now.value.getTime()) {
      next = new Date(y + 1, ANNIVERSARY_MONTH - 1, ANNIVERSARY_DAY)
    }
    return Math.ceil((next.getTime() - now.value.getTime()) / 86400000)
  })

  // 距离见面还有多少天（日期已过则为负数，由页面决定展示）
  const daysToMeeting = computed(() =>
    Math.ceil((MEETING_DATE.getTime() - now.value.getTime()) / 86400000)
  )

  return { togetherText, daysToAnniversary, daysToMeeting }
}
