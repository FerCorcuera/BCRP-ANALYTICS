import type { Metadata } from "next";
import "./globals.css";

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
      <body>{children}</body>
    </html>
  );
}
