import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Global Retail Intelligence Engine",
  description: "Ask about products, regional pricing, and warranty.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
