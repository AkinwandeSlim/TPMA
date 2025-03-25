// import { Outfit } from "next/font/google";
// import "./globals.css";

// import { SidebarProvider } from "@/src/context/SidebarContext";
// import { ThemeProvider } from "@/src/context/ThemeContext";

// const outfit = Outfit({
//   variable: "--font-outfit-sans",
//   subsets: ["latin"],
// });

// export default function RootLayout({
//   children,
// }: Readonly<{
//   children: React.ReactNode;
// }>) {
//   return (
//     <html lang="en">
//       <body className={`${outfit.variable} dark:bg-gray-900`}>
//         <ThemeProvider>
//           <SidebarProvider>{children}</SidebarProvider>
//         </ThemeProvider>
//       </body>
//     </html>
//   );
// }



import "./css/style.css"; // Adjust path from src/app/(public)/
import "./css/additional-styles/theme.css";
import "./css/additional-styles/utility-patterns.css";

import localFont from "next/font/local";
import { Inter } from "next/font/google";


const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});
const nacelle = localFont({
  src: [
    { path: "../../public/fonts/nacelle-regular.woff2", weight: "400", style: "normal" },
    { path: "../../public/fonts/nacelle-italic.woff2", weight: "400", style: "italic" },
    { path: "../../public/fonts/nacelle-semibold.woff2", weight: "600", style: "normal" },
    { path: "../../public/fonts/nacelle-semibolditalic.woff2", weight: "600", style: "italic" },
  ],
  variable: "--font-nacelle",
});

export const metadata = {
  title: "TPMA - Education management through AI assistance, automation, and real-time tracking.",
  description:
    "Digitizing and streamlining teaching practice management through AI assistance, automation, and real-time tracking.",
  metadataBase: new URL("https://tpma.dev"),
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${nacelle.variable} font-inter text-base text-gray-200 antialiased`}>
        {children}
      </body>
    </html>
  );
}