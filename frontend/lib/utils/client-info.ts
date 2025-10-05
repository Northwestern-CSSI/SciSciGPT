import { headers } from 'next/headers'

export async function getClientInfo(): Promise<Record<string, string>> {
  const headersList = headers()
  
  const clientInfo: Record<string, string> = {
    timestamp: new Date().toISOString()
  }

  const networkHeaders = [
    'x-forwarded-for',
    'x-real-ip', 
    'cf-connecting-ip',
    'x-client-ip',
    'x-forwarded',
    'forwarded-for',
    'forwarded',
    'via'
  ]

  const deviceHeaders = [
    'user-agent',
    'sec-ch-ua',
    'sec-ch-ua-mobile',
    'sec-ch-ua-platform'
  ]

  const geoHeaders = [
    'cf-ipcountry',
    'cf-region', 
    'cf-ipcity',
    'cf-timezone',
    'x-country-code',
    'cloudfront-viewer-country'
  ]

  const otherHeaders = [
    'referer',
    'accept-language',
    'accept-encoding',
    'origin'
  ]

  const allHeaders = [...networkHeaders, ...deviceHeaders, ...geoHeaders, ...otherHeaders]

  allHeaders.forEach(headerName => {
    const value = headersList.get(headerName)
    if (value) {
      clientInfo[headerName] = value
    }
  })

  return clientInfo
}