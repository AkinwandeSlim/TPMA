import Link from "next/link";
import Image from "next/image";
import logo from "/logo.svg";
// import logo from "@/public/images/logo1.svg";
export default function Logo() {
  return (
    <Link href="/" className="inline-flex shrink-0" aria-label="TPMA">
      <Image src={logo} alt="TPMA Logo" width={32} height={32} />
    </Link>
  );
}

