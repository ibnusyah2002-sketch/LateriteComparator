import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Laterite Comparator — Grade Control",
  description: "Scan. Compare. Identify. AI Comparator for laterite material grade control.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${inter.variable} h-full antialiased`}>
      <body className="min-h-full bg-lcgc-background text-lcgc-text-primary">
        {children}
      </body>
    </html>
  );
}
