
import Header from "@/src/components/ui/header";
import Footer from "@/src/components/ui/footer";
import PageIllustration from "@/src/components/page-illustration";

import "../css/style.css"; // Adjust path from src/app/(public)/
import "../css/additional-styles/theme.css";
import "../css/additional-styles/utility-patterns.css";


// import { ChakraProvider } from "@chakra-ui/react";
// import initialTheme from "@/theme/theme"; // Adjust path
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


export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (

  <div className="flex min-h-screen flex-col overflow-hidden bg-gray-950 supports-[overflow:clip]:overflow-clip">
    <Header />
      <main className="relative flex grow flex-col">
      <PageIllustration multiple />
        {children}
      </main>
  </div>
  );
}













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
























// import PageIllustration from "@/src/components/page-illustration";
// import localFont from "next/font/local";
// import { Inter } from "next/font/google";

// import Header from "@/src/components/ui/header";

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

// export const metadata = {
//   title: "Auth - TPMA",
//   description: "Sign in or Sign up  to the Teaching Practice Management Application",
// };



// export default function AuthLayout({
//   children,
// }: {
//   children: React.ReactNode;
// }) {
//   return (
// <body className={`${inter.variable} ${nacelle.variable} bg-gray-950 font-inter text-base text-gray-200 antialiased`}
// >
//   <div className="flex min-h-screen flex-col overflow-hidden supports-[overflow:clip]:overflow-clip">
//     <Header />
//       <main className="relative flex grow flex-col">
//         <PageIllustration multiple />

//         {children}
//       </main>
//   </div>
// </body>


//   );
// }















