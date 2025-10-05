'use client'

import { useState, useCallback, useEffect } from 'react'
import { getChatsClient, clearChats } from '@/app/actions'
import { ClearHistory } from '@/components/clear-history'
import { SidebarItems } from '@/components/sidebar-items'
import { ThemeToggle } from '@/components/theme-toggle'
import { type Chat } from '@/lib/types'

interface PaginatedSidebarListProps {
  userId?: string
  initialChats: Chat[]
  totalCount: number
}

export function PaginatedSidebarList({ userId, initialChats, totalCount }: PaginatedSidebarListProps) {
  const [chats, setChats] = useState<Chat[]>(initialChats)
  const [loading, setLoading] = useState(false)
  const [hasMore, setHasMore] = useState(initialChats.length < totalCount)
  const [offset, setOffset] = useState(20)

  const loadMoreChats = useCallback(async () => {
    if (loading || !hasMore || !userId) return

    setLoading(true)
    try {
      const newChats = await getChatsClient(userId, 20, offset)
      if (newChats && Array.isArray(newChats)) {
        setChats(prev => {
          const updatedChats = [...prev, ...newChats]
          setHasMore(updatedChats.length < totalCount)
          return updatedChats
        })
        setOffset(prev => prev + newChats.length)
      }
    } catch (error) {
      console.error('Failed to load more chats:', error)
    } finally {
      setLoading(false)
    }
  }, [userId, offset, loading, hasMore, totalCount])

  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    const { scrollTop, scrollHeight, clientHeight } = e.currentTarget
    if (scrollHeight - scrollTop <= clientHeight + 100 && hasMore && !loading) {
      loadMoreChats()
    }
  }, [loadMoreChats, hasMore, loading])

  const handleRemove = useCallback((chatId: string) => {
    setChats(prev => prev.filter(chat => chat.id !== chatId))
  }, [])

  const handleShare = useCallback((chatId: string, updatedChat: Chat) => {
    setChats(prev => prev.map(chat => 
      chat.id === chatId ? { ...chat, ...updatedChat } : chat
    ))
  }, [])

  const handleAddChat = useCallback((newChat: Chat) => {
    setChats(prev => {
      if (prev.some(chat => chat.id === newChat.id)) {
        return prev
      }
      return [newChat, ...prev]
    })
  }, [])

  const refreshChats = useCallback(async () => {
    if (!userId || loading) return
    
    try {
      const freshChats = await getChatsClient(userId, Math.max(20, chats.length), 0)
      setChats(freshChats)
    } catch (error) {
      console.error('Failed to refresh chats:', error)
    }
  }, [userId, loading, chats.length])

  useEffect(() => {
    const handleFocus = () => {
      refreshChats()
    }

    window.addEventListener('focus', handleFocus)
    
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        refreshChats()
      }
    }
    
    document.addEventListener('visibilitychange', handleVisibilityChange)

    return () => {
      window.removeEventListener('focus', handleFocus)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, [refreshChats])

  useEffect(() => {
    const handleNewChat = (e: CustomEvent) => {
      const newChatData = e.detail
      if (newChatData && newChatData.id) {
        handleAddChat(newChatData)
      }
    }

    window.addEventListener('newChatAdded', handleNewChat as EventListener)
    
    return () => {
      window.removeEventListener('newChatAdded', handleNewChat as EventListener)
    }
  }, [handleAddChat])

  return (
    <div className="flex flex-1 flex-col overflow-hidden">
      <div className="flex-1 overflow-auto" onScroll={handleScroll}>
        {chats?.length ? (
          <div className="space-y-2 px-2">
            <SidebarItems 
              chats={chats} 
              onRemove={handleRemove}
              onShare={handleShare}
            />
            {loading && (
              <div className="flex items-center justify-center py-4">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900 dark:border-gray-100"></div>
              </div>
            )}
            {!hasMore && chats.length > 0 && (
              <div className="text-center py-4 text-sm text-muted-foreground">
                No more chats to load
              </div>
            )}
          </div>
        ) : (
          <div className="p-8 text-center">
            <p className="text-sm text-muted-foreground">No chat history</p>
          </div>
        )}
      </div>
      <div className="flex items-center justify-between p-4">
        <ThemeToggle />
        <ClearHistory clearChats={clearChats} isEnabled={chats?.length > 0} />
      </div>
    </div>
  )
}