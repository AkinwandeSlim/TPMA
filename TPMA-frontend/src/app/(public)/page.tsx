

import PageIllustration from "@/src/components/page-illustration";
import HeroHome from "@/src/components/hero-home";
import Workflows from "@/src/components/workflows";
import Features from "@/src/components/features";
import Testimonials from "@/src/components/testimonials";
import Cta from "@/src/components/cta";


export const metadata = {
  title: "TPMA - Education management through AI assistance, automation, and real-time tracking.",
  description:
    "Digitizing and streamlining teaching practice management through AI assistance, automation, and real-time tracking.",
  metadataBase: new URL("https://tpma.dev"),
};

export default function Home() {
  return (
    <>
      <HeroHome />
      <Workflows />
      <Features />
      <Cta />

    </>
  );
}
