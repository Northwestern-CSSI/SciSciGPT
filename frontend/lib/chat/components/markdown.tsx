'use client'
import { MemoizedReactMarkdown } from '@/components/markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeRaw from 'rehype-raw'
import { CodeBlock } from './codeblock'
import CollapsibleUI from '@/lib/chat/components/collapsible-ui'
import React, { useState } from 'react'

export function Markdown({ text, header }: { text: string, header: string }) {
  const components = {
    p({ children }: any) {
      return (
        <p className="mb-2 last:mb-0">
          {children}
        </p>
      )
    },

    details({ children }: any) {
      const childrenArray = React.Children.toArray(children)
      const summaryElement = childrenArray.find((child: any) => 
        child?.type === 'summary'
      )
      const contentElements = childrenArray.filter((child: any) => 
        child?.type !== 'summary'
      )
      // ).map((child, index) => (
      //   <Markdown text={String(child)} header={header} key={index}/>
      // ))
      
      return <CollapsibleUI header={summaryElement}> {contentElements} </CollapsibleUI>
    },

    // summary({ children }: any) {
    //   return (
    //     <div className="font-semibold text-blue-600 dark:text-blue-400 mb-2">
    //       {children}
    //     </div>
    //   )
    // },

    code({ node, inline, className, children, ...props }: any) {
      if (children.length) {
        if (children[0] == '▍') {
          return (
            <span className="mt-1 animate-pulse cursor-default">▍</span>
          )
        }
        children[0] = (children[0] as string).replace('`▍`', '▍')
      }

      const match = /language-(\w+)/.exec(className || '')

      if (inline) {
        return (
          <code className={className} {...props}>
            {children}
          </code>
        )
      }

      return (
        <CodeBlock
          key={`codeblock-${text.length}-${match?.[1] || 'plain'}`}
          language={match?.[1] || 'plain'}
          header={header}
          value={String(children).replace(/\n$/, '')}
          {...props}
        />
      )
    }
  }
  
  return text.length > 0 ? (
    <MemoizedReactMarkdown
      className="prose break-words dark:prose-invert prose-p:leading-relaxed prose-pre:p-0 max-w-4xl"
      remarkPlugins={[remarkGfm, remarkMath]}
      rehypePlugins={[rehypeRaw as any]}
      components={components}
    >
      {text}
    </MemoizedReactMarkdown>
  ) : null
}