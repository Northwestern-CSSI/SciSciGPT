import { nanoid } from '@/lib/utils'
import { Chat } from '@/components/chat'
import { AI } from '@/lib/chat/actions'
import { auth } from '@/auth'
import { Session } from '@/lib/types'
import { getMissingKeys } from '@/app/actions'
import LoginForm from '@/components/login-form'

export const metadata = {
  title: 'SciSciGPT'
}

function RedirectScript() {
  const enableRedirect = process.env.ENABLE_REDIRECT === 'true'
  const redirectTarget = process.env.REDIRECT_TARGET
  
  if (!enableRedirect || !redirectTarget) {
    return null
  }

  console.log('RedirectScript', {
    enableRedirect,
    redirectTarget
  })
  
  return (
    <script
      dangerouslySetInnerHTML={{
        __html: `
          if (window.location.hostname !== '${redirectTarget}') {
            window.location.href = 'https://${redirectTarget}' + window.location.pathname + window.location.search;
          }
        `
      }}
    />
  )
}

export default async function IndexPage() {
  const session = (await auth()) as Session
  
  if (!session) {
    return (
      <main className="flex flex-col items-center w-full min-h-screen">
        <RedirectScript />
        <div className="w-full max-w-md px-4 mt-8">
          <LoginForm />
        </div>
      </main>
    )
  } else {
    const id = nanoid()
    const missingKeys = await getMissingKeys()
    return (
      <>
        <RedirectScript />
        <AI initialAIState={{ chatId: id, messages: [] }}>
          <Chat key={id} id={id} session={session} missingKeys={missingKeys} />
        </AI>
      </>
    )
  }
}
