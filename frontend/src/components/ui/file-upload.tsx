"use client";

import { motion } from "framer-motion";
import { Upload, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import type { FileUploadZoneProps } from "@/types";

export const FileUploadZone = ({
    onDrop,
    isLoading,
    className,
    accept = ".tex",
    title = "Upload your LaTeX CV",
    description = "Drag and drop your .tex file here, or click to browse",
    processingText = "Processing your CV...",
}: FileUploadZoneProps) => {
    return (
        <motion.div
            className={cn("relative", className)}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div
                className={cn(
                    "group relative p-4 sm:p-8 lg:p-12 text-center cursor-pointer nb-border nb-shadow bg-white",
                    {
                        "pointer-events-none opacity-50": isLoading,
                    }
                )}
                onDrop={(e) => {
                    e.preventDefault();
                    if (!isLoading) {
                        onDrop(Array.from(e.dataTransfer.files));
                    }
                }}
                onDragOver={(e) => e.preventDefault()}
                onClick={() => {
                    if (!isLoading) {
                        const input = document.createElement("input");
                        input.type = "file";
                        input.accept = accept;
                        input.onchange = (e) => {
                            const files = (e.target as HTMLInputElement).files;
                            if (files) onDrop(Array.from(files));
                        };
                        input.click();
                    }
                }}
                role="button"
                tabIndex={0}
                aria-label={title}
                onKeyDown={(e) => {
                    if ((e.key === "Enter" || e.key === " ") && !isLoading) {
                        e.preventDefault();
                        const input = document.createElement("input");
                        input.type = "file";
                        input.accept = accept;
                        input.onchange = (e) => {
                            const files = (e.target as HTMLInputElement).files;
                            if (files) onDrop(Array.from(files));
                        };
                        input.click();
                    }
                }}
            >
                <motion.div
                    className="flex flex-col items-center gap-3 sm:gap-4"
                    whileHover={{ scale: 1.02 }}
                    transition={{ duration: 0.2 }}
                >
                    <div className="relative">
                        <Upload className="h-8 w-8 sm:h-10 sm:w-10 lg:h-12 lg:w-12 text-foreground" />
                    </div>

                    <div className="space-y-1 sm:space-y-2">
                        <h3 className="text-base sm:text-lg lg:text-xl font-semibold text-foreground">
                            {title}
                        </h3>
                        <p className="text-xs sm:text-sm lg:text-base text-foreground max-w-md px-2">
                            {description}
                        </p>
                    </div>

                    <div className="flex items-center gap-2 text-xs sm:text-sm text-muted-foreground">
                        <Sparkles className="h-3 w-3" />
                        <span>AI-powered CV optimization</span>
                    </div>
                </motion.div>

                {isLoading && (
                    <motion.div
                        className="absolute inset-0 flex items-center justify-center bg-white/80 backdrop-blur-sm nb-border nb-shadow"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        role="status"
                        aria-label="Processing file"
                    >
                        <div className="flex flex-col items-center gap-2">
                            <div className="animate-spin h-6 w-6 sm:h-8 sm:w-8 border-2 border-foreground border-t-transparent" />
                            <p className="text-xs sm:text-sm lg:text-base text-foreground">
                                {processingText}
                            </p>
                        </div>
                    </motion.div>
                )}
            </div>
        </motion.div>
    );
};
