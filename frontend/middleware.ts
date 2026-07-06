import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token')?.value
  const path = request.nextUrl.pathname

  // Doctor routes require doctor role
  if (path.startsWith('/doctor') && !path.startsWith('/doctor/login')) {
    // Check token and role - for now just check token presence
    if (!token) {
      return NextResponse.redirect(new URL('/doctor/login', request.url))
    }
  }

  // Patient routes require patient role
  if (path.startsWith('/patient') && !path.startsWith('/patient/login')) {
    if (!token) {
      return NextResponse.redirect(new URL('/patient/login', request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/doctor/:path*', '/patient/:path*'],
}
