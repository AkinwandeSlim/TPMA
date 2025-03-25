"use client";

import { useState, useEffect } from "react";
import { getUserRole, logout, ROLES } from "@/src/lib/auth";
import Link from "next/link";
import Logo from "./logo";
import { usePathname } from "next/navigation";

export default function Header() {
  const [role, setRole] = useState<string | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    const currentRole = getUserRole();
    setRole(currentRole);
  }, []);

  const handleLogout = () => {
    logout();
    setRole(null);
    window.location.href = "/signin";
  };

  const isDashboardRoute = ["/trainee", "/supervisor", "/admin"].includes(pathname);

  return (
    <header className="z-30 mt-2 w-full md:mt-5">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="relative flex h-14 items-center justify-between gap-3 rounded-2xl bg-gray-900/90 px-3 before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,var(--color-gray-800),var(--color-gray-700),var(--color-gray-800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)] after:absolute after:inset-0 after:-z-10 after:backdrop-blur-xs">
          {/* Site branding */}
          <div className="flex flex-1 items-center space-x-2">
            <Logo />
            <Link href="/" className="text-lg font-semibold text-white">TPMA</Link>
          </div>

          {/* Navigation with role-based links */}
          <nav className="flex flex-1 items-center justify-end gap-3">
            {role && isDashboardRoute && role === ROLES.TRAINEE && (
              <Link href="/trainee" className="text-gray-300 hover:text-indigo-400">
                Trainee Dashboard
              </Link>
            )}
            {role && isDashboardRoute && role === ROLES.SUPERVISOR && (
              <Link href="/supervisor" className="text-gray-300 hover:text-indigo-400">
                Supervisor Dashboard
              </Link>
            )}
            {role && isDashboardRoute && role === ROLES.ADMINISTRATOR && (
              <>
                <Link href="/admin" className="text-gray-300 hover:text-indigo-400">
                  Admin Dashboard
                </Link>
                <Link href="/trainee" className="text-gray-300 hover:text-indigo-400">
                  Trainee View
                </Link>
                <Link href="/supervisor" className="text-gray-300 hover:text-indigo-400">
                  Supervisor View
                </Link>
              </>
            )}
            {role ? (


              <button
                onClick={handleLogout}
                className="btn-sm bg-linear-to-t from-indigo-600 to-indigo-500 bg-[length:100%_100%] bg-[bottom] py-[5px] text-white shadow-[inset_0px_1px_0px_0px_--theme(--color-white/.16)] hover:bg-[length:100%_150%]"
              >
                Logout
              </button>
            ) : (
              <>
                <Link
                  href="/signin"
                  className="btn-sm relative bg-linear-to-b from-gray-800 to-gray-800/60 bg-[length:100%_100%] bg-[bottom] py-[5px] text-gray-300 before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,var(--color-gray-800),var(--color-gray-700),var(--color-gray-800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)] hover:bg-[length:100%_150%]"
                >
                  Sign In
                </Link>
                <Link
                  href="/signup"
                  className="btn-sm bg-linear-to-t from-indigo-600 to-indigo-500 bg-[length:100%_100%] bg-[bottom] py-[5px] text-white shadow-[inset_0px_1px_0px_0px_--theme(--color-white/.16)] hover:bg-[length:100%_150%]"
                >
                  Register
                </Link>
              </>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}
// "use client";

// import { useState, useEffect } from "react";
// import { getUserRole, logout, ROLES } from "@/src/lib/auth";
// import Link from "next/link";
// import Logo from "./logo";
// import { usePathname } from "next/navigation";

// export default function Header() {
//   const [role, setRole] = useState<string | null>(null);
//   const pathname = usePathname();

//   useEffect(() => {
//     const currentRole = getUserRole();
//     setRole(currentRole);
//   }, []);

//   const handleLogout = () => {
//     logout();
//     setRole(null);
//     window.location.href = "/signin";
//   };

//   const isDashboardRoute = ["/trainee", "/supervisor", "/admin"].includes(pathname);

//   return (
//     <header className="z-30 mt-2 w-full md:mt-5">
//       <div className="mx-auto max-w-6xl px-4 sm:px-6">
//         <div className="relative flex h-14 items-center justify-between gap-3 rounded-2xl bg-gray-900/90 px-3 before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,var(--color-gray-800),var(--color-gray-700),var(--color-gray-800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)] after:absolute after:inset-0 after:-z-10 after:backdrop-blur-xs">
//           <div className="flex flex-1 items-center space-x-2">
//             <Logo />
//             <Link href="/" className="text-lg font-semibold text-white">TPMA</Link>
//           </div>
//         <nav className="space-x-4">
//           {role && isDashboardRoute && role === ROLES.TRAINEE && (
//             <Link href="/trainee" className="hover:text-indigo-400">Trainee Dashboard</Link>
//           )}
//           {role && isDashboardRoute && role === ROLES.SUPERVISOR && (
//             <Link href="/supervisor" className="hover:text-indigo-400">Supervisor Dashboard</Link>
//           )}
//           {role && isDashboardRoute && role === ROLES.ADMINISTRATOR && (
//             <>
//               <Link href="/admin" className="hover:text-indigo-400">Admin Dashboard</Link>
//               <Link href="/trainee" className="hover:text-indigo-400">Trainee View</Link>
//               <Link href="/supervisor" className="hover:text-indigo-400">Supervisor View</Link>
//             </>
//           )}
//           {role ? (
//             <button onClick={handleLogout} className="hover:text-indigo-400">Logout</button>
//           ) : (
//             <Link href="/signin" className="hover:text-indigo-400">Sign In</Link>
//           )}
//         </nav>
//       </div>
//       </div>
//     </header>
//   );
// }














// "use client";

// import { useState, useEffect } from "react";
// import { getUserRole, logout, ROLES } from "@/src/lib/auth";
// import Link from "next/link";

// export default function Header() {
//   const [role, setRole] = useState<string | null>(null);

//   useEffect(() => {
//     const currentRole = getUserRole();
//     setRole(currentRole);
//   }, []);

//   const handleLogout = () => {
//     logout();
//     setRole(null);
//     window.location.href = '/signin';
//   };

//   return (
//     <header className="bg-gray-900 text-white p-4">
//       <div className="max-w-6xl mx-auto flex justify-between items-center">
//         <Link href="/" className="text-xl font-bold">TPMA</Link>
//         <nav className="space-x-4">
//           {role === ROLES.TRAINEE && (
//             <Link href="/trainee" className="hover:text-indigo-400">Trainee Dashboard</Link>
//           )}
//           {role === ROLES.SUPERVISOR && (
//             <Link href="/supervisor" className="hover:text-indigo-400">Supervisor Dashboard</Link>
//           )}
//           {role === ROLES.ADMINISTRATOR && (
//             <>
//               <Link href="/admin" className="hover:text-indigo-400">Admin Dashboard</Link>
//               <Link href="/trainee" className="hover:text-indigo-400">Trainee View</Link>
//               <Link href="/supervisor" className="hover:text-indigo-400">Supervisor View</Link>
//             </>
//           )}
//           {role ? (
//             <button onClick={handleLogout} className="hover:text-indigo-400">Logout</button>
//           ) : (
//             <Link href="/signin" className="hover:text-indigo-400">Sign In</Link>
//           )}
//         </nav>
//       </div>
//     </header>
//   );
// }