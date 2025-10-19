"use client";

import { useTheme } from "next-themes";
import { Toaster as Sonner, ToasterProps } from "sonner";

const Toaster = ({ ...props }: ToasterProps) => {
    const { theme = "system" } = useTheme();

    return (
        <Sonner
            theme={theme as ToasterProps["theme"]}
            className="toaster group"
            style={
                {
                    "--normal-bg": "var(--card)",
                    "--normal-text": "var(--card-foreground)",
                    "--normal-border": "var(--border)",
                    "--success-bg": "var(--card)",
                    "--success-text": "var(--card-foreground)",
                    "--success-border": "var(--border)",
                    "--error-bg": "var(--card)",
                    "--error-text": "var(--card-foreground)",
                    "--error-border": "var(--border)",
                    "--warning-bg": "var(--card)",
                    "--warning-text": "var(--card-foreground)",
                    "--warning-border": "var(--border)",
                } as React.CSSProperties
            }
            toastOptions={{
                style: {
                    border: "3px solid var(--border)",
                    borderRadius: "0px",
                    boxShadow: "6px 6px 0 0 var(--border)",
                    fontWeight: "600",
                },
            }}
            {...props}
        />
    );
};

export { Toaster };
