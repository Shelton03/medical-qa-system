import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Auth is handled client-side via JWT in localStorage.
  // The backend is the ultimate authority for access control.
  // Middleware here can be used for non-auth concerns (CSP headers, etc.)
  // but per the architecture docs we do NOT do cookie-based redirects.
  return NextResponse.next()
}

export const config = {
  matcher: ['/doctor/:path*', '/patient/:path*'],
}
