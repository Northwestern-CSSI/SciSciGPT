import { getChats, getTotalChatsCount } from '@/app/actions'
import { PaginatedSidebarList } from '@/components/paginated-sidebar-list'
import { cache } from 'react'

interface SidebarListProps {
  userId?: string
  children?: React.ReactNode
}

const loadInitialChats = cache(async (userId?: string) => {
  return await getChats(userId, 20, 0)
})

const loadTotalCount = cache(async (userId?: string) => {
  return await getTotalChatsCount(userId)
})

export async function SidebarList({ userId }: SidebarListProps) {
  const [initialChats, totalCount] = await Promise.all([
    loadInitialChats(userId),
    loadTotalCount(userId)
  ])

  return <PaginatedSidebarList userId={userId} initialChats={initialChats} totalCount={totalCount} />
}