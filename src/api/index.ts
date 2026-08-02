import type { Photo, Album, HeroContent, Todo, ApiResponse, PaginatedData } from '@/types'

const BASE = ''

async function request<T>(url: string): Promise<T> {
  const res = await fetch(`${BASE}${url}`)
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  const json: ApiResponse<T> = await res.json()
  if (json.code !== 0) throw new Error(json.message)
  return json.data
}

async function jsonRequest<T>(url: string, method: 'POST' | 'PATCH', body?: unknown): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    method,
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
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
