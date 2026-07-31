import { reactive } from 'vue'
import type { Photo } from '@/types'

interface ViewerState {
  isOpen: boolean
  photos: Photo[]
  currentIndex: number
}

const state = reactive<ViewerState>({
  isOpen: false,
  photos: [],
  currentIndex: 0,
})

export function usePhotoViewer() {
  function open(photos: Photo[], index: number) {
    state.photos = photos
    state.currentIndex = index
    state.isOpen = true
    document.body.style.overflow = 'hidden'
  }

  function close() {
    state.isOpen = false
    document.body.style.overflow = ''
  }

  function next() {
    if (state.currentIndex < state.photos.length - 1) {
      state.currentIndex++
    }
  }

  function prev() {
    if (state.currentIndex > 0) {
      state.currentIndex--
    }
  }

  return { state, open, close, next, prev }
}
