"use client";

import { useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";
import Header from "@/src/components/ui/header";
import Footer from "@/src/components/ui/footer";
import PageIllustration from "@/src/components/page-illustration";
import "../css/style.css";
import "../css/additional-styles/theme.css";
import "../css/additional-styles/utility-patterns.css";
import localFont from "next/font/local";
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const nacelle = localFont({
  src: [
    { path: "../../../public/fonts/nacelle-regular.woff2", weight: "400", style: "normal" },
    { path: "../../../public/fonts/nacelle-italic.woff2", weight: "400", style: "italic" },
    { path: "../../../public/fonts/nacelle-semibold.woff2", weight: "600", style: "normal" },
    { path: "../../../public/fonts/nacelle-semibolditalic.woff2", weight: "600", style: "italic" },
  ],
  variable: "--font-nacelle",
});

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    AOS.init({
      once: true,
      disable: "phone",
      duration: 600,
      easing: "ease-out-sine",
    });
  }, []);

  return (
<div className="flex min-h-screen flex-col bg-gray-950">
      <Header />
      <main className="relative flex grow flex-col">
        <PageIllustration />
        {children}
      </main>
      <Footer />
    </div>

  );
}















// "use client";

// import { useEffect } from "react";

// import AOS from "aos";
// import "aos/dist/aos.css";
// import Header from "@/src/components/ui/header";
// import Footer from "@/src/components/ui/footer";


// import "../css/style.css"; // Adjust path from src/app/(public)/
// import "../css/additional-styles/theme.css";
// import "../css/additional-styles/utility-patterns.css";


// // import { ChakraProvider } from "@chakra-ui/react";
// // import initialTheme from "@/theme/theme"; // Adjust path
// import localFont from "next/font/local";
// import { Inter } from "next/font/google";
// import PageIllustration from "@/src/components/page-illustration";


// const inter = Inter({
//   subsets: ["latin"],
//   variable: "--font-inter",
//   display: "swap",
// });
// const nacelle = localFont({
//   src: [
//     { path: "../../../public/fonts/nacelle-regular.woff2", weight: "400", style: "normal" },
//     { path: "../../../public/fonts/nacelle-italic.woff2", weight: "400", style: "italic" },
//     { path: "../../../public/fonts/nacelle-semibold.woff2", weight: "600", style: "normal" },
//     { path: "../../../public/fonts/nacelle-semibolditalic.woff2", weight: "600", style: "italic" },
//   ],
//   variable: "--font-nacelle",
// });

// export default function PublicLayout({
//   children,
// }: {
//   children: React.ReactNode;
// }) {
//   useEffect(() => {
//     AOS.init({
//       once: true,
//       disable: "phone",
//       duration: 600,
//       easing: "ease-out-sine",
//     });
//   }, []);{
//     return (
        
//         <div className="flex min-h-screen flex-col overflow-hidden bg-gray-950 supports-[overflow:clip]:overflow-clip">  
//            <Header />
//             <main className="relative flex grow flex-col"> 
//               <PageIllustration/>
//               {children}
//             </main>
//             <Footer />
//         </div>

// );
//   }
// }

  // return (
  //   <body className={`${nacelle.variable} bg-gradient-to-b from-gray-900 to-gray-800 text-white antialiased`}>
  //   <div className="flex min-h-screen flex-col overflow-hidden supports-[overflow:clip]:overflow-clip">
  //   <>
  //     <Header />
  //     <main className="relative flex grow flex-col bg-gray-50 dark:bg-gray-900">
  //       {children}
  //     </main>
  //     <Footer />
  //   </>
  //   </div>
  //   </body>   
  // );




