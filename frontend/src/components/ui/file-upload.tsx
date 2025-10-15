"use client";

import { motion } from "framer-motion";
import { Upload, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import type { FileUploadZoneProps } from "@/types";

export const FileUploadZone = ({ onDrop, isLoading, className, accept = ".tex", title = "Upload your LaTeX CV", description = "Drag and drop your .tex file here, or click to browse", processingText = "Processing your CV..." }: FileUploadZoneProps) => {
    return (
        <motion.div className={cn("relative", className)} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <div
                className={cn("group relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300", "hover:border-primary hover:bg-primary/5 cursor-pointer", "border-muted-foreground/25 bg-muted/10", {
                    "pointer-events-none opacity-50": isLoading,
                })}
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
            >
                <motion.div className="flex flex-col items-center gap-4" whileHover={{ scale: 1.02 }} transition={{ duration: 0.2 }}>
                    <div className="relative">
                        <Upload className="h-12 w-12 text-muted-foreground group-hover:text-primary transition-colors" />
                    </div>

                    <div className="space-y-2">
                        <h3 className="text-lg font-semibold text-foreground">{title}</h3>
                        <p className="text-sm text-muted-foreground max-w-md">{description}</p>
                    </div>

                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        <Sparkles className="h-3 w-3" />
                        <span>AI-powered CV optimization</span>
                    </div>
                </motion.div>

                {isLoading && (
                    <motion.div className="absolute inset-0 flex items-center justify-center bg-background/80 backdrop-blur-sm rounded-xl" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <div className="flex flex-col items-center gap-2">
                            <div className="animate-spin rounded-full h-8 w-8 border-2 border-primary border-t-transparent" />
                            <p className="text-sm text-muted-foreground">{processingText}</p>
                        </div>
                    </motion.div>
                )}
            </div>
        </motion.div>
    );
};
