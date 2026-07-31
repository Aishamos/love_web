import { onMounted, onUnmounted, type Ref } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

interface FadeUpOptions {
  y?: number
  duration?: number
  stagger?: number
  start?: string
}

export function useFadeUpOnScroll(
  target: Ref<HTMLElement | null>,
  options: FadeUpOptions = {}
) {
  const { y = 30, duration = 1.2, stagger = 0, start = 'top 85%' } = options

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced) return

  let trigger: ScrollTrigger | null = null

  onMounted(() => {
    if (!target.value) return

    trigger = ScrollTrigger.create({
      trigger: target.value,
      start,
      onEnter() {
        gsap.fromTo(
          target.value!,
          { opacity: 0, y },
          { opacity: 1, y: 0, duration, stagger, ease: 'power2.out' }
        )
      },
      once: true,
    })
  })

  onUnmounted(() => {
    trigger?.kill()
  })
}
