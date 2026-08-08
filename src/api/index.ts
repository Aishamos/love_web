import type { Photo, Album, HeroContent, Todo, ApiResponse, PaginatedData } from '@/types'

const BASE = ''

let csrfTokenPromise: Promise<string> | null = null

/** 带 HTTP 状态码的 API 错误，便于调用方区分 401 等场景 */
export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function getCsrfToken(): Promise<string> {
  if (!csrfTokenPromise) {
    csrfTokenPromise = fetch('/api/auth/csrf', { credentials: 'same-origin' })
      .then((res) => res.json())
      .then((json: ApiResponse<{ token: string }>) => {
        if (json.code !== 0) throw new Error(json.message)
        return json.data.token
      })
      .catch((err) => {
        csrfTokenPromise = null
        throw err
      })
  }
  return csrfTokenPromise
}

async function request<T>(url: string): Promise<T> {
  const res = await fetch(`${BASE}${url}`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  const json: ApiResponse<T> = await res.json()
  if (json.code !== 0) throw new Error(json.message)
  return json.data
}

async function jsonRequest<T>(url: string, method: 'POST' | 'PATCH', body?: unknown): Promise<T> {
  const token = await getCsrfToken()
  const res = await fetch(`${BASE}${url}`, {
    method,
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': token },
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  const json: ApiResponse<T> = await res.json()
  if (json.code !== 0) throw new Error(json.message)
  return json.data
}

export async function fetchLatestPhotos(count = 12): Promise<Photo[]> {
  return request<Photo[]>(`/api/photos/latest?count=${count}`)
}

export async function fetchPhotos(albumId?: number, page = 1, pageSize = 20): Promise<PaginatedData<Photo>> {
  const params = new URLSearchParams({ page: String(page), pageSize: String(pageSize) })
  if (albumId) params.set('albumId', String(albumId))
  return request<PaginatedData<Photo>>(`/api/photos?${params}`)
}

export async function fetchAlbums(): Promise<Album[]> {
  return request<Album[]>('/api/albums')
}

export async function fetchAlbum(id: string | number): Promise<Album> {
  return request<Album>(`/api/albums/${id}`)
}

export async function fetchHero(): Promise<HeroContent> {
  return request<HeroContent>('/api/hero')
}

export async function fetchTodos(): Promise<Todo[]> {
  return request<Todo[]>('/api/todos')
}

export async function createTodo(content: string): Promise<Todo> {
  return jsonRequest<Todo>('/api/todos', 'POST', { content })
}

export async function toggleTodo(id: string | number, done: boolean): Promise<Todo> {
  return jsonRequest<Todo>(`/api/todos/${id}`, 'PATCH', { done })
}

export async function login(username: string, password: string): Promise<void> {
  const token = await getCsrfToken()
  const res = await fetch(`${BASE}/api/auth/login`, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': token },
    body: JSON.stringify({ username, password }),
  })
  const json: ApiResponse<unknown> | null = await res.json().catch(() => null)
  if (!res.ok || json?.code !== 0) {
    throw new ApiError(json?.message || `登录失败（${res.status}）`, res.status)
  }
}

export async function uploadPhotos(
  formData: FormData,
  onProgress?: (percent: number) => void
): Promise<{ message: string }> {
  const token = await getCsrfToken()
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', `${BASE}/api/upload`)
    xhr.withCredentials = true
    xhr.setRequestHeader('X-CSRF-Token', token)
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable && onProgress) {
        onProgress(Math.round((e.loaded / e.total) * 100))
      }
    }
    xhr.onload = () => {
      let json: ApiResponse<unknown> | null = null
      try {
        json = JSON.parse(xhr.responseText)
      } catch {
        // 非 JSON 响应（如网关错误页），走下方统一报错
      }
      if (xhr.status === 401) {
        reject(new ApiError(json?.message || '登录已过期，请重新登录', 401))
        return
      }
      if (json && json.code === 0) {
        resolve(json as ApiResponse<{ message: string }>)
        return
      }
      reject(new ApiError(json?.message || '上传失败，请重试', xhr.status))
    }
    xhr.onerror = () => reject(new ApiError('网络错误，请重试', 0))
    xhr.send(formData)
  })
}
