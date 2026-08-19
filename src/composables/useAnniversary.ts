import { ref, computed, onMounted, onUnmounted } from 'vue'

interface AnniversaryConfig {
  anniversaryStart: string // 在一起的起始日期 YYYY-MM-DD
  anniversaryMonth: number // 纪念日月份（真实在一起的月份）
  anniversaryDay: number // 纪念日日子（真实在一起的日子）
  meetingDate: string // 距离见面的目标日期 YYYY-MM-DD
}

// 兜底配置：读取 anniversary.json 失败时使用（与 public/anniversary.json 保持一致）
const FALLBACK: AnniversaryConfig = {
  anniversaryStart: '2026-06-09',
  anniversaryMonth: 6,
  anniversaryDay: 9,
  meetingDate: '2026-11-14',
}

export function useAnniversary() {
  const now = ref(new Date())
  const loaded = ref(false)
  const config = ref<AnniversaryConfig>({ ...FALLBACK })
  let timer: number | undefined

  onMounted(async () => {
    try {
      const res = await fetch(`/anniversary.json?t=${Date.now()}`, { cache: 'no-store' })
      if (res.ok) {
        const data = (await res.json()) as Partial<AnniversaryConfig>
        config.value = { ...FALLBACK, ...data }
      }
    } catch {
      // 保持兜底配置
    }
    loaded.value = true
    timer = window.setInterval(() => { now.value = new Date() }, 60000)
  })
  onUnmounted(() => {
    window.clearInterval(timer)
  })

  const startDate = computed(() => new Date(`${config.value.anniversaryStart}T00:00:00`))
  const meetingDate = computed(() => new Date(`${config.value.meetingDate}T00:00:00`))

  const totalDays = computed(() =>
    Math.max(0, Math.floor((now.value.getTime() - startDate.value.getTime()) / 86400000))
  )
  // 只显示总天数，不折算成年
  const togetherText = computed(() => `${totalDays.value} 天`)

  const daysToAnniversary = computed(() => {
    const y = now.value.getFullYear()
    let next = new Date(y, config.value.anniversaryMonth - 1, config.value.anniversaryDay)
    if (next.getTime() < now.value.getTime()) {
      next = new Date(y + 1, config.value.anniversaryMonth - 1, config.value.anniversaryDay)
    }
    return Math.ceil((next.getTime() - now.value.getTime()) / 86400000)
  })

  // 距离见面还有多少天（日期已过则为负数，由页面决定展示）
  const daysToMeeting = computed(() =>
    Math.ceil((meetingDate.value.getTime() - now.value.getTime()) / 86400000)
  )

  return { loaded, togetherText, daysToAnniversary, daysToMeeting }
}
