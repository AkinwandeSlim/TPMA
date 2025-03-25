// "use client";





// import { Outfit } from "next/font/google";
// import "../../globals.css"; // Adjust path

// import { SidebarProvider } from "@/src/context/SidebarContext";
// import { ThemeProvider } from "@/src/context/ThemeContext";





// import { useSidebar } from "@/src/context/SidebarContext";
// import AppHeader from "@/src/layout/AppHeader";
// import AppSidebar from "@/src/layout/AppSidebar";
// import Backdrop from "@/src/layout/Backdrop";
// import React from "react";



// const outfit = Outfit({
//   variable: "--font-outfit-sans",
//   subsets: ["latin"],
// });



// export default function AdminLayout({
//   children,
// }: {
//   children: React.ReactNode;
// }) {
//   const { isExpanded, isHovered, isMobileOpen } = useSidebar();

//   // Dynamic class for main content margin based on sidebar state
//   const mainContentMargin = isMobileOpen
//     ? "ml-0"
//     : isExpanded || isHovered
//     ? "lg:ml-[290px]"
//     : "lg:ml-[90px]";

//   return (

//       <body className={`${outfit.variable} dark:bg-gray-900`}>
//         <ThemeProvider>
//           <SidebarProvider>
//       <div className="min-h-screen xl:flex">
//         {/* Sidebar and Backdrop */}
//         <AppSidebar />
//         <Backdrop />
//         {/* Main Content Area */}
//         <div
//           className={`flex-1 transition-all  duration-300 ease-in-out ${mainContentMargin}`}
//         >
//           {/* Header */}
//           <AppHeader />
//           {/* Page Content */}
//           <div className="p-4 mx-auto max-w-(--breakpoint-2xl) md:p-6">{children}</div>
//         </div>
//       </div>

//       </SidebarProvider>
//         </ThemeProvider>
//         </body>
//   );
// }




"use client";

import Header from "@/src/components/ui/header";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col overflow-hidden bg-white text-gray-900">
      <Header />
      <main className="flex grow flex-col">
        {children}
      </main>
    </div>
  );
}