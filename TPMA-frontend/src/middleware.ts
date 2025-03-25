import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { ROLES } from './lib/auth';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('access_token')?.value; // Check for token in cookies
  const isLoggedIn = !!token;

  // Placeholder: Normally, you'd verify the token and extract role from it
  // For now, assume role is passed via cookie or inferred later
  const roleCookie = request.cookies.get('user_role')?.value;
  const role = roleCookie && Object.values(ROLES).includes(roleCookie as any) ? roleCookie as keyof typeof ROLES : null;

  // Define role-based route restrictions
  const roleRoutes: { [key: string]: string[] } = {
    [ROLES.TRAINEE]: ['/trainee'],
    [ROLES.SUPERVISOR]: ['/supervisor'],
    [ROLES.ADMINISTRATOR]: ['/admin', '/trainee', '/supervisor'],
  };

  // Public routes
  const publicRoutes = ['/signin', '/signup', '/', '/reset-password'];

  // If not logged in, redirect to signin for protected routes
  if (!isLoggedIn && !publicRoutes.includes(pathname)) {
    return NextResponse.redirect(new URL('/signin', request.url));
  }

  // If logged in, redirect to role-specific dashboard from root
  if (isLoggedIn && pathname === '/') {
    const redirectPath =
      role === ROLES.TRAINEE ? '/trainee' :
      role === ROLES.SUPERVISOR ? '/supervisor' :
      role === ROLES.ADMINISTRATOR ? '/admin' : '/signin';
    return NextResponse.redirect(new URL(redirectPath, request.url));
  }

  // Check role-based access
  if (isLoggedIn && role) {
    const allowedRoutes = roleRoutes[role] || [];
    if (!publicRoutes.includes(pathname) && !allowedRoutes.includes(pathname)) {
      return NextResponse.redirect(new URL('/signin', request.url));
    }
  }

  return NextResponse.next();
}

// export const config = {
//   matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
// };



export const config = {
  matcher: ["/((?!_next/static|_next/image|images|favicon.ico|signin).*)"],
};