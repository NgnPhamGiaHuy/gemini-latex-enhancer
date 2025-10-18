"use client";

import { Upload } from "lucide-react";
import { motion } from "framer-motion";

import type { UploadStepProps } from "@/types";

import ModelSelection from "./model-selection";
import { AppTooltip } from "@/components/ui/tooltip";
import { FileUploadZone } from "@/components/ui/file-upload";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useFileUpload, useModelSelection } from "@/hooks";

const UploadStep = ({ step, selectedModel, onUploadSuccess, onLoadingChange, onModelChange }: UploadStepProps) => {
    const { models, isLoading, error } = useModelSelection({ onModelChange });

    const { handleFileUpload } = useFileUpload({ onUploadSuccess, onLoadingChange, selectedModel });

    if (step !== "upload") return null;

    return (
        <motion.div key="upload" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} transition={{ duration: 0.4 }}>
            <div className="max-w-4xl mx-auto space-y-3 sm:space-y-6">
                {/* Model Selection */}
                <ModelSelection models={models} selectedModel={selectedModel} defaultModel="gemini-2.5-flash" isLoading={isLoading} error={error} onModelChange={onModelChange} />

                {/* File Upload */}
                <Card>
                    <CardHeader className="text-center pb-3 sm:pb-6">
                        <CardTitle className="text-lg sm:text-xl lg:text-2xl flex items-center justify-center gap-2">
                            <Upload className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
                            Upload Your CV
                        </CardTitle>
                        <p className="text-sm sm:text-base lg:text-lg text-muted-foreground">Start by uploading your LaTeX CV file</p>
                    </CardHeader>
                    <CardContent>
                        <AppTooltip content="We support .tex files. Your CV is processed locally before enhancement.">
                            <div>
                                <FileUploadZone onDrop={handleFileUpload} isLoading={false} />
                            </div>
                        </AppTooltip>
                    </CardContent>
                </Card>
            </div>
        </motion.div>
    );
};

export default UploadStep;
