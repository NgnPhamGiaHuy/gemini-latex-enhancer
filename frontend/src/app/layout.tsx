import type { Metadata } from "next";
import { Space_Grotesk, IBM_Plex_Mono } from "next/font/google";

import "./globals.css";

import { Toaster } from "@/components/ui/sonner";
import { AppTooltipProvider } from "@/components/ui/tooltip";

const spaceGrotesk = Space_Grotesk({
    variable: "--font-space-grotesk",
    subsets: ["latin"],
    display: "swap",
    weight: ["400", "600", "700"],
});

const plexMono = IBM_Plex_Mono({
    variable: "--font-plex-mono",
    subsets: ["latin"],
    display: "swap",
    weight: ["400", "600"],
});

export const metadata: Metadata = {
    title: "Gemini LaTeX Enhancer – AI‑assisted CV enhancement with LaTeX outputs",
    description:
        "Transform your LaTeX CV with AI-powered optimization tailored to any job description",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body
                suppressHydrationWarning
                className={`${spaceGrotesk.variable} ${plexMono.variable} antialiased`}
            >
                <AppTooltipProvider>{children}</AppTooltipProvider>
                <Toaster />
            </body>
        </html>
    );
}
