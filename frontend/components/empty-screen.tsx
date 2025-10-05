import { UseChatHelpers } from 'ai/react'

import { Button } from '@/components/ui/button'
import { ExternalLink } from '@/components/external-link'
import { IconArrowRight } from '@/components/ui/icons'

export function EmptyScreen() {
  return (
    <div className="mx-auto max-w-2xl px-4">
      <div className="flex flex-col gap-2 rounded-lg border bg-background p-8">
        <h1 className="text-lg font-semibold">
          <ExternalLink href="https://arxiv.org/abs/2504.05559">SciSciGPT</ExternalLink>
        </h1>
        <p className="leading-normal text-muted-foreground">
          A prototype AI collaborator for Science of Science research. It uses Anthropic Claude, Google BigQuery, LangChain, and many other tools to provide SciSci assistance for data processing, data analysis, visualization, and literature understanding.
        </p>
        <p className="leading-normal text-muted-foreground">
          SciSciGPT is built upon{' '}
          <ExternalLink href="https://www.nature.com/articles/s41597-023-02198-9">SciSciNet</ExternalLink>. The current prototype version only includes US domestic data (up to 2021).
        </p>
      </div>
    </div>
  )
}
