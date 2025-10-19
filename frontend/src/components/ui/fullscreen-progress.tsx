"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Progress } from "@/components/ui/progress";
import { Sparkles, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import type {
    FullScreenProgressProps,
    FullScreenProgressMinimalProps,
} from "@/types";

export const FullScreenProgress = ({
    loading,
    progress,
    message,
    title = "Processing Your CV",
    subtitle = "AI is enhancing your CV to match the job requirements",
}: FullScreenProgressProps) => {
    return (
        <AnimatePresence>
            {loading && (
                <motion.div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-background/95 backdrop-blur-sm"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                >
                    <div className="flex flex-col items-center justify-center max-w-md mx-auto px-6 py-8 nb-border nb-shadow bg-white">
                        {/* Animated Icon */}
                        <motion.div
                            className="relative mb-8"
                            animate={{
                                scale: [1, 1.1, 1],
                                rotate: [0, 5, -5, 0],
                            }}
                            transition={{
                                duration: 2,
                                repeat: Infinity,
                                ease: "easeInOut",
                            }}
                        >
                            <div className="relative">
                                <Sparkles className="h-16 w-16 text-foreground" />
                                <motion.div
                                    className="absolute inset-0"
                                    animate={{ rotate: 360 }}
                                    transition={{
                                        duration: 3,
                                        repeat: Infinity,
                                        ease: "linear",
                                    }}
                                >
                                    <Loader2 className="h-16 w-16 text-muted-foreground" />
                                </motion.div>
                            </div>
                        </motion.div>

                        {/* Title and Subtitle */}
                        <motion.div
                            className="text-center mb-8"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                        >
                            <h2 className="text-2xl font-bold uppercase text-foreground mb-2">
                                {title}
                            </h2>
                            <p className="text-foreground text-sm leading-relaxed">
                                {subtitle}
                            </p>
                        </motion.div>

                        {/* Progress Section */}
                        <motion.div
                            className="w-full space-y-4"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.4 }}
                        >
                            {/* Progress Bar */}
                            <div className="space-y-2">
                                <Progress value={progress} className="h-3" />
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-foreground">
                                        {message || "Processing..."}
                                    </span>
                                    <span className="font-medium text-foreground">
                                        {progress}%
                                    </span>
                                </div>
                            </div>

                            {/* Animated Dots */}
                            <motion.div
                                className="flex justify-center space-x-2"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.6 }}
                            >
                                {[0, 1, 2].map((i) => (
                                    <motion.div
                                        key={i}
                                        className="w-3 h-3 bg-accent nb-border"
                                        animate={{
                                            scale: [1, 1.2, 1],
                                            opacity: [0.5, 1, 0.5],
                                        }}
                                        transition={{
                                            duration: 1.5,
                                            repeat: Infinity,
                                            delay: i * 0.2,
                                        }}
                                    />
                                ))}
                            </motion.div>
                        </motion.div>

                        {/* Additional Info */}
                        <motion.div
                            className="mt-8 text-center"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.8 }}
                        >
                            <p className="text-xs text-muted-foreground">
                                This may take a few moments...
                            </p>
                        </motion.div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

// Alternative minimal version for smaller screens
export const FullScreenProgressMinimal = ({
    loading,
    progress,
    message,
}: FullScreenProgressMinimalProps) => {
    return (
        <AnimatePresence>
            {loading && (
                <motion.div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-background/95 backdrop-blur-sm"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                >
                    <div className="flex flex-col items-center justify-center max-w-sm mx-auto px-6 py-8">
                        {/* Spinner */}
                        <motion.div
                            className="mb-6"
                            animate={{ rotate: 360 }}
                            transition={{
                                duration: 1,
                                repeat: Infinity,
                                ease: "linear",
                            }}
                        >
                            <Loader2 className="h-12 w-12 text-primary" />
                        </motion.div>

                        {/* Progress */}
                        <div className="w-full space-y-3">
                            <Progress value={progress} className="h-2" />
                            <div className="text-center">
                                <p className="text-sm text-muted-foreground mb-1">
                                    {message || "Processing..."}
                                </p>
                                <p className="text-lg font-medium text-foreground">
                                    {progress}%
                                </p>
                            </div>
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};
