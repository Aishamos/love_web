import { ref, computed, onMounted, onUnmounted } from 'vue'

// ===== 纪念日数据（请改成真实日期）=====
export const ANNIVERSARY_START = new Date(2026, 5, 9) // 在一起的起始日期（年, 月-1, 日）
export const ANNIVERSARY_MONTH = 6 // 纪念日月份（真实在一起的月份）
export const ANNIVERSARY_DAY = 9 // 纪念日日子（真实在一起的日子）
export const MEETING_DATE = new Date(2026, 11, 31) // 距离见面的目标日期（年, 月-1, 日）

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
