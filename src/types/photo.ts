export interface Photo {
  id: string | number
  url: string
  thumbnailUrl?: string
  alt?: string
  width?: number
  height?: number
}

export interface Album {
  id: string | number
  title: string
  coverUrl: string
  photoCount: number
  description?: string
}

export interface Moment {
  id: string | number
  title: string
  location?: string
  date: string
  photoCount: number
}

export interface HeroContent {
  imageUrl: string
  title: string
  subtitle: string
}
