'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { kv } from '@vercel/kv'

import { auth } from '@/auth'
import { type Chat } from '@/lib/types'

export async function getChats(userId?: string | null, limit = 20, offset = 0) {
  if (!userId) {
    return []
  }

  try {
    const allChats: string[] = await kv.zrange(`user:chat:${userId}`, 0, -1, {
      rev: true
    })

    const activeChats = allChats.filter(chat => 
      chat.startsWith('active:') || (!chat.includes(':chat:'))
    )

    const paginatedChats = activeChats.slice(offset, offset + limit)

    if (paginatedChats.length === 0) {
      return []
    }

    const pipeline = kv.pipeline()
    for (const chat of paginatedChats) {
      const parts = chat.split(':')
      const chatKey = parts[0] === 'active' ? parts.slice(1).join(':') : chat
      pipeline.hgetall(chatKey)
    }

    const results = await pipeline.exec()

    return (results as Chat[]).filter(chat => chat)
  } catch (error) {
    return []
  } 

  return []
}

export async function getChat(id: string, userId: string) {
  const chat = await kv.hgetall<Chat>(`chat:${id}`)

  if (!chat || (userId && chat.userId !== userId)) {
    return null
  }

  const chats = await kv.zrange(`user:chat:${userId}`, 0, -1)
  const isDeleted = chats.some(member => member === `deleted:chat:${id}`)
  if (isDeleted) {
    return null
  }

  return chat
}

export async function removeChat({ id, path }: { id: string; path: string }) {
  const session = await auth()

  if (!session) {
    return {
      error: 'Unauthorized'
    }
  }

  //Convert uid to string for consistent comparison with session.user.id
  const uid = String(await kv.hget(`chat:${id}`, 'userId'))

  if (uid !== session?.user?.id) {
    return {
      error: 'Unauthorized'
    }
  }

  const pipeline = kv.pipeline()
  pipeline.zrem(`user:chat:${session.user.id}`, `active:chat:${id}`)
  pipeline.zrem(`user:chat:${session.user.id}`, `chat:${id}`)
  pipeline.zadd(`user:chat:${session.user.id}`, {
    score: Date.now(),
    member: `deleted:chat:${id}`
  })
  await pipeline.exec()

  revalidatePath('/')
  return revalidatePath(path)
}

export async function clearChats() {
  const session = await auth()

  if (!session?.user?.id) {
    return {
      error: 'Unauthorized'
    }
  }

  const chats: string[] = await kv.zrange(`user:chat:${session.user.id}`, 0, -1)
  if (!chats.length) {
    return redirect('/')
  }
  
  const activeChats = chats.filter(chat => 
    chat.startsWith('active:') || (!chat.includes(':chat:'))
  )
  
  if (!activeChats.length) {
    return redirect('/')
  }
  
  const pipeline = kv.pipeline()
  
  for (const chat of activeChats) {
    const parts = chat.split(':')
    const chatKey = parts[0] === 'active' ? parts.slice(1).join(':') : chat
    const chatId = chatKey.replace('chat:', '')
    
    pipeline.zrem(`user:chat:${session.user.id}`, chat)
    pipeline.zadd(`user:chat:${session.user.id}`, {
      score: Date.now(),
      member: `deleted:chat:${chatId}`
    })
  }

  await pipeline.exec()

  revalidatePath('/')
  return redirect('/')
}

export async function getSharedChat(id: string) {
  const chat = await kv.hgetall<Chat>(`chat:${id}`)

  if (!chat || !chat.sharePath) {
    return null
  }
  
  const chats = await kv.zrange(`user:chat:${chat.userId}`, 0, -1)
  const isDeleted = chats.some(member => member === `deleted:chat:${id}`)
  if (isDeleted) {
    return null
  }
  return chat
}

export async function shareChat(id: string) {
  const session = await auth()

  if (!session?.user?.id) {
    return {
      error: 'Unauthorized'
    }
  }

  const chat = await kv.hgetall<Chat>(`chat:${id}`)

  if (!chat || chat.userId !== session.user.id) {
    return {
      error: 'Something went wrong'
    }
  }

  const chats = await kv.zrange(`user:chat:${session.user.id}`, 0, -1)
  const isDeleted = chats.some(member => member === `deleted:chat:${id}`)
  if (isDeleted) {
    return {
      error: 'Chat not found'
    }
  }

  const payload = {
    ...chat,
    sharePath: `/share/${chat.id}`
  }

  await kv.hmset(`chat:${chat.id}`, payload)

  return payload
}

export async function saveChat(chat: Chat) {
  const session = await auth()

  if (session && session.user) {
    const pipeline = kv.pipeline()
    pipeline.hmset(`chat:${chat.id}`, chat)
    pipeline.zadd(`user:chat:${chat.userId}`, {
      score: Date.now(),
      member: `active:chat:${chat.id}`
    })
    await pipeline.exec()
    
    revalidatePath('/')
  } else {
    return
  }
}

export async function appendClientInfo(chatId: string, clientInfo: Record<string, string>) {
  const session = await auth()

  if (session && session.user) {
    const existingChat = await kv.hgetall<Chat>(`chat:${chatId}`)
    
    if (existingChat && existingChat.userId === session.user.id) {
      let existingHistory: Record<string, string>[] = []
      if (existingChat.clientInfoHistory) {
        try {
          existingHistory = typeof existingChat.clientInfoHistory === 'string' 
            ? JSON.parse(existingChat.clientInfoHistory)
            : existingChat.clientInfoHistory
        } catch (e) {
          existingHistory = []
        }
      }
      
      const updatedHistory = [...existingHistory, clientInfo]
      await kv.hset(`chat:${chatId}`, { clientInfoHistory: JSON.stringify(updatedHistory) })
    }
  }
}

export async function refreshHistory(path: string) {
  redirect(path)
}

export async function getChatsClient(userId: string, limit: number, offset: number) {
  'use server'
  const chats = await getChats(userId, limit, offset)
  return chats
}

export async function getTotalChatsCount(userId?: string | null) {
  'use server'
  if (!userId) {
    return 0
  }

  try {
    const chats: string[] = await kv.zrange(`user:chat:${userId}`, 0, -1)
    const activeChats = chats.filter(chat => 
      chat.startsWith('active:') || (!chat.includes(':chat:'))
    )
    return activeChats.length
  } catch (error) {
    return 0
  }
}

export async function getMissingKeys() {
  return []
}