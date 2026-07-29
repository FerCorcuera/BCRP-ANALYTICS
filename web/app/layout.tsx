import type { Metadata } from "next";
import { Zilla_Slab } from "next/font/google";
import "./globals.css";

const zillaSlab = Zilla_Slab({
  variable: "--font-zilla-slab",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "BCRP Nowcasting Lab",
  description:
    "Experimental nowcasting models for Peruvian macroeconomic series.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={zillaSlab.variable}>{children}</body>
    </html>
  );
}
