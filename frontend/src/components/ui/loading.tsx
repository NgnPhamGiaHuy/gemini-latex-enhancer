"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import type {
    LoadingSpinnerProps,
    LoadingButtonProps,
    LoadingCardProps,
} from "@/types";

export const LoadingSpinner = ({
    size = "md",
    className,
}: LoadingSpinnerProps) => {
    const sizeClasses = {
        sm: "h-4 w-4",
        md: "h-6 w-6",
        lg: "h-8 w-8",
    };

    return (
        <motion.div
            className={cn(
                "border-2 border-foreground border-t-transparent",
                sizeClasses[size],
                className
            )}
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
    );
};

export const LoadingButton = ({
    isLoading,
    children,
    className,
    disabled,
    onClick,
}: LoadingButtonProps) => {
    return (
        <motion.button
            className={cn(
                "inline-flex items-center justify-center gap-2 px-6 py-2 text-sm font-semibold nb-border nb-shadow bg-accent text-accent-foreground disabled:pointer-events-none disabled:opacity-50",
                className
            )}
            disabled={disabled || isLoading}
            onClick={onClick}
            whileHover={{
                x: disabled || isLoading ? 0 : -2,
                y: disabled || isLoading ? 0 : -2,
            }}
        >
            {isLoading && <LoadingSpinner size="sm" />}
            {children}
        </motion.button>
    );
};

export const LoadingCard = ({
    isLoading,
    children,
    className,
}: LoadingCardProps) => {
    return (
        <div className={cn("relative", className)}>
            {children}
            {isLoading && (
                <motion.div
                    className="absolute inset-0 flex items-center justify-center bg-background/80 backdrop-blur-sm"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                >
                    <div className="flex flex-col items-center gap-2">
                        <LoadingSpinner size="lg" />
                        <p className="text-sm text-muted-foreground">
                            Processing...
                        </p>
                    </div>
                </motion.div>
            )}
        </div>
    );
};
