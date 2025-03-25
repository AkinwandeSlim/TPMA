"use client";

import { useState } from "react";
import { saveLoginResponse, ROLES } from "@/src/lib/auth";
import { useRouter } from "next/navigation";
import api from "@/src/lib/axios";
import Link from "next/link";

export default function SignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await api.post("/token/", { email, password }, { withCredentials: true });
      console.log("Backend Response:", response.data); // Check this
      saveLoginResponse(response.data);

      // Set cookies for middleware
      document.cookie = `access_token=${response.data.access}; path=/; max-age=3600; SameSite=Lax`;
      const role = response.data?.user?.role || null;
      if (role && Object.values(ROLES).includes(role)) {
        document.cookie = `user_role=${role}; path=/; max-age=3600; SameSite=Lax`;
        const redirectPath =
          role === ROLES.TRAINEE ? "/trainee" :
          role === ROLES.SUPERVISOR ? "/supervisor" :
          role === ROLES.ADMINISTRATOR ? "/admin" : "/";
        router.push(redirectPath);
      } else {
        setError("Invalid or missing user role");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Sign-in failed");
    } finally {
      setLoading(false);
    }
  };
  return (
    <section>
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="py-12 md:py-20">
          <div className="pb-12 text-center">
            <h1 className="animate-[gradient_6s_linear_infinite] bg-[linear-gradient(to_right,var(--color-gray-200),var(--color-indigo-200),var(--color-gray-50),var(--color-indigo-300),var(--color-gray-200))] bg-[length:200%_auto] bg-clip-text font-nacelle text-3xl font-semibold text-transparent md:text-4xl">
              Sign In
            </h1>
          </div>
          <form className="mx-auto max-w-[400px]" onSubmit={handleSignIn}>
            {error && <p className="text-red-500 text-sm mb-4 text-center">{error}</p>}
            <div className="space-y-5">
              <div>
                <label className="mb-1 block text-sm font-medium text-indigo-200/65" htmlFor="email">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  className="w-full p-2 bg-gray-800 text-white border border-gray-700 rounded disabled:bg-gray-600"
                  placeholder="Your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={loading}
                />
              </div>
              <div>
                <div className="mb-1 flex items-center justify-between gap-3">
                  <label className="block text-sm font-medium text-indigo-200/65" htmlFor="password">
                    Password
                  </label>
                  <Link className="text-sm text-gray-400 hover:underline" href="/reset-password">
                    Forgot?
                  </Link>
                </div>
                <input
                  id="password"
                  type="password"
                  className="w-full p-2 bg-gray-800 text-white border border-gray-700 rounded disabled:bg-gray-600"
                  placeholder="Your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={loading}
                />
              </div>
            </div>
            <div className="mt-6 space-y-5">
              <button
              type="submit"
              className="w-full p-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:bg-indigo-400"
              disabled={loading}
            >
              {loading ? "Signing In..." : "Sign In"}
            </button>
              <div className="flex items-center gap-3 text-center text-sm italic text-gray-600 before:h-px before:flex-1 before:bg-linear-to-r before:from-transparent before:via-gray-400/25 after:h-px after:flex-1 after:bg-linear-to-r after:from-transparent after:via-gray-400/25">
                or
              </div>
              <button
                className="btn relative w-full bg-linear-to-b from-gray-800 to-gray-800/60 bg-[length:100%_100%] bg-[bottom] text-gray-300 before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,var(--color-gray-800),var(--color-gray-700),var(--color-gray-800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)] hover:bg-[length:100%_150%] disabled:opacity-50"
                disabled={loading}
              >
                Sign In with Google
              </button>
            </div>
          </form>
          <div className="mt-6 text-center text-sm text-indigo-200/65">
            Don't you have an account?{" "}
            <Link className="font-medium text-indigo-500 hover:underline" href="/signup">
              Sign Up
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
  
































  
  // return (
  //   <section>
  //     <div className="mx-auto max-w-6xl px-4 sm:px-6">
  //       <div className="py-12 md:py-20">
  //         {/* Section header */}
  //         <div className="pb-12 text-center">
  //           <h1 className="animate-[gradient_6s_linear_infinite] bg-[linear-gradient(to_right,var(--color-gray-200),var(--color-indigo-200),var(--color-gray-50),var(--color-indigo-300),var(--color-gray-200))] bg-[length:200%_auto] bg-clip-text font-nacelle text-3xl font-semibold text-transparent md:text-4xl">
  //             Welcome back
  //           </h1>
  //         </div>
  //         {/* Contact form */}
  //         {error && <p className="text-red-500 mb-4">{error}</p>}
  //         <form className="mx-auto max-w-[400px]" onSubmit={handleSignIn}>
  //           <div className="space-y-5">
  //             <div>
  //               <label
  //                 className="mb-1 block text-sm font-medium text-indigo-200/65"
  //                 htmlFor="email"
  //               >
  //                 Email
  //               </label>
  //               <input
  //                 id="email"
  //                 type="email"
  //                 className="form-input w-full"
  //                 placeholder="Your email"
  //                 value={email}
  //                 onChange={(e) => setEmail(e.target.value)}    
  //                 required            
  //               />
  //             </div>
  //             <div>
  //               <div className="mb-1 flex items-center justify-between gap-3">
  //                 <label
  //                   className="block text-sm font-medium text-indigo-200/65"
  //                   htmlFor="password"
  //                 >
  //                   Password
  //                 </label>
  //                 <Link
  //                   className="text-sm text-gray-600 hover:underline"
  //                   href="/reset-password"
  //                 >
  //                   Forgot?
  //                 </Link>
  //               </div>
  //               <input
  //                 id="password"
  //                 type="password"
  //                 className="form-input w-full"
  //                 placeholder="Your password"
  //                 value={password}
  //                 onChange={(e) => setPassword(e.target.value)}
  //                 required
  //               />
  //             </div>
  //           </div>
  //           <div className="mt-6 space-y-5">
  //             <button type='submit' className="btn w-full bg-linear-to-t from-indigo-600 to-indigo-500 bg-[length:100%_100%] bg-[bottom] text-white shadow-[inset_0px_1px_0px_0px_--theme(--color-white/.16)] hover:bg-[length:100%_150%]">
  //               Sign in
  //             </button>
  //             <div className="flex items-center gap-3 text-center text-sm italic text-gray-600 before:h-px before:flex-1 before:bg-linear-to-r before:from-transparent before:via-gray-400/25 after:h-px after:flex-1 after:bg-linear-to-r after:from-transparent after:via-gray-400/25">
  //               or
  //             </div>
  //             <button className="btn relative w-full bg-linear-to-b from-gray-800 to-gray-800/60 bg-[length:100%_100%] bg-[bottom] text-gray-300 before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,var(--color-gray-800),var(--color-gray-700),var(--color-gray-800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)] hover:bg-[length:100%_150%]">
  //               Sign In with Google
  //             </button>
  //           </div>
  //         </form>
  //         {/* Bottom link */}
  //         <div className="mt-6 text-center text-sm text-indigo-200/65">
  //           Don't you have an account?{" "}
  //           <Link className="font-medium text-indigo-500" href="/signup">
  //             Sign Up
  //           </Link>
  //         </div>
  //       </div>
  //     </div>
  //   </section>
  // );}
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  // (
  //   <section>
  //     <div className="mx-auto max-w-6xl px-4 sm:px-6">
  //       <div className="py-12 md:py-20">
  //         {/* Section header */}
  //         <div className="pb-12 text-center">
  //           <h1 className="animate-[gradient_6s_linear_infinite] bg-[linear-gradient(to_right,var(--color-gray-200),var(--color-indigo-200),var(--color-gray-50),var(--color-indigo-300),var(--color-gray-200))] bg-[length:200%_auto] bg-clip-text font-nacelle text-3xl font-semibold text-transparent md:text-4xl">
  //             Welcome back
  //           </h1>
  //         </div>
  //         {/* Contact form */}
  //         {error && <p className="text-red-500 mb-4">{error}</p>}
  //         <form className="mx-auto max-w-[400px]" onSubmit={handleSignIn}>
  //           <div className="space-y-5">
  //             <div>
  //               <label
  //                 className="mb-1 block text-sm font-medium text-indigo-200/65"
  //                 htmlFor="email"
  //               >
  //                 Email
  //               </label>
  //               <input
  //                 id="email"
  //                 type="email"
  //                 className="form-input w-full"
  //                 placeholder="Your email"
  //                 value={email}
  //                 onChange={(e) => setEmail(e.target.value)}    
  //                 required            
  //               />

  //             </div>
  //             <div>
  //               <div className="mb-1 flex items-center justify-between gap-3">
  //                 <label
  //                   className="block text-sm font-medium text-indigo-200/65"
  //                   htmlFor="password"
  //                 >
  //                   Password
  //                 </label>
  //                 <Link
  //                   className="text-sm text-gray-600 hover:underline"
  //                   href="/reset-password"
  //                 >
  //                   Forgot?
  //                 </Link>
  //               </div>
  //               <input
  //                 id="password"
  //                 type="password"
  //                 className="form-input w-full"
  //                 placeholder="Your password"
  //                 value={password}
  //                 onChange={(e) => setPassword(e.target.value)}
  //                 required
  //               />

  //             </div>
  //           </div>
  //           <div className="mt-6 space-y-5">
  //             <button className="btn w-full bg-linear-to-t from-indigo-600 to-indigo-500 bg-[length:100%_100%] bg-[bottom] text-white shadow-[inset_0px_1px_0px_0px_--theme(--color-white/.16)] hover:bg-[length:100%_150%]">
  //               Sign in
  //             </button>
  //             <div className="flex items-center gap-3 text-center text-sm italic text-gray-600 before:h-px before:flex-1 before:bg-linear-to-r before:from-transparent before:via-gray-400/25 after:h-px after:flex-1 after:bg-linear-to-r after:from-transparent after:via-gray-400/25">
  //               or
  //             </div>
  //             <button className="btn relative w-full bg-linear-to-b from-gray-800 to-gray-800/60 bg-[length:100%_100%] bg-[bottom] text-gray-300 before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,var(--color-gray-800),var(--color-gray-700),var(--color-gray-800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)] hover:bg-[length:100%_150%]">
  //               Sign In with Google
  //             </button>
  //           </div>
  //         </form>

  //         {/* Bottom link */}
  //         <div className="mt-6 text-center text-sm text-indigo-200/65">
  //           Don't you have an account?{" "}
  //           <button className="font-medium text-indigo-500" type="submit">
  //             Sign Up
  //           </button>
  //         </div>
  //       </div>
  //     </div>
  //   </section>
  // );}