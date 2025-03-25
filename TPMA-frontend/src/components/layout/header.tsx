"use client";

import Link from "next/link";
import Logo from "./logo";
import { useState, useEffect } from "react";
import { auth_isLoggedIn, logout, getUserRole } from "@/lib/auth";

export default function Header() {

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    setIsLoggedIn(auth_isLoggedIn());
    setRole(getUserRole());
  }, []);

  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
    setRole(null);
    window.location.href = "/signin";
  };





  return (
    <header className="z-30 mt-2 w-full md:mt-5">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="relative flex h-14 items-center justify-between gap-3 rounded-2xl bg-gray-900/90 px-3 before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,var(--color-gray-800),var(--color-gray-700),var(--color-gray-800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)] after:absolute after:inset-0 after:-z-10 after:backdrop-blur-xs">
          {/* Site branding */}
          <div className="flex flex-1 items-center space-x-2">
              <Logo />
            <span className="text-white text-xl font-bold">TPMA</span>
          </div>

          {/* Desktop sign in links */}
          {/* <ul className="flex flex-1 items-center justify-end gap-3">
            <li>
              <Link
                href="/signin"
                className="btn-sm relative bg-linear-to-b from-gray-800 to-gray-800/60 bg-[length:100%_100%] bg-[bottom] py-[5px] text-gray-300 before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,var(--color-gray-800),var(--color-gray-700),var(--color-gray-800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)] hover:bg-[length:100%_150%]"
              >
                Sign In
              </Link>
            </li>
            <li>
              <Link
                href="/signup"
                className="btn-sm bg-linear-to-t from-indigo-600 to-indigo-500 bg-[length:100%_100%] bg-[bottom] py-[5px] text-white shadow-[inset_0px_1px_0px_0px_--theme(--color-white/.16)] hover:bg-[length:100%_150%]"
              >
                Register
              </Link>
            </li>
          </ul> */}



          <nav className="flex grow">
            <ul className="flex grow justify-end flex-wrap items-center">
              {isLoggedIn ? (
                <>
                  {role === "trainee" && <li><Link href="/trainee" className="text-gray-300 hover:text-gray-200 px-4">Dashboard</Link></li>}
                  {role === "supervisor" && <li><Link href="/supervisor" className="text-gray-300 hover:text-gray-200 px-4">Dashboard</Link></li>}
                  {role === "administrator" && <li><Link href="/admin" className="text-gray-300 hover:text-gray-200 px-4">Dashboard</Link></li>}
                  <li><button onClick={handleLogout} className="text-gray-300 hover:text-gray-200 px-4">Logout</button></li>
                </>
              ) : (
                <>
                  <li><Link href="/signin" className="text-gray-300 hover:text-gray-200 px-4">Sign In</Link></li>
                  <li><Link href="/signup" className="btn-sm text-white bg-blue-600 hover:bg-blue-700 ml-3">Sign Up</Link></li>
                </>
              )}
            </ul>
          </nav>



          
        </div>
      </div>
    </header>
  );
}







