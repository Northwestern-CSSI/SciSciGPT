/** @type {import('next').NextConfig} */
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'avatars.githubusercontent.com',
        port: '',
        pathname: '**'
      }
    ]
  },
  serverExternalPackages: ['@langchain/core'],
  compress: false,
  poweredByHeader: false,

  experimental: {
    serverActions: {
      allowedOrigins: ['https://sciscigpt.com', 'https://sciscigpt.ngrok.app', 'http://localhost:3000']
    }
  }
}
