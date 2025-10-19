"use client";

import { motion } from "framer-motion";
import { CheckCircle } from "lucide-react";

import type { DownloadStepProps } from "@/types";

import DownloadLinks from "./download-links";
import { Button } from "@/components/ui/button";
import { AppTooltip } from "@/components/ui/tooltip";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const DownloadStep = ({
    step,
    generateResult,
    onStartOver,
    onBackToJobDetails,
    inputMethod,
    onRegenerateSingle,
    onRegenerateBatch,
}: DownloadStepProps) => {
    if (step !== "download") return null;

    return (
        <motion.div
            key="download"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            transition={{ duration: 0.4 }}
        >
            <Card className="max-w-2xl mx-auto">
                <CardHeader className="text-center pb-3 sm:pb-6">
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        aria-hidden="true"
                    >
                        <CheckCircle className="h-12 w-12 sm:h-16 sm:w-16 text-foreground mx-auto mb-3 sm:mb-4" />
                    </motion.div>
                    <CardTitle className="text-lg sm:text-xl lg:text-2xl font-bold uppercase">
                        Your Tailored CV is Ready!
                    </CardTitle>
                    <p className="text-sm sm:text-base lg:text-lg text-foreground">
                        Download your optimized CV in your preferred format
                    </p>
                </CardHeader>
                <CardContent className="space-y-4">
                    <DownloadLinks generateResult={generateResult} />

                    {/* Action Buttons */}
                    <div className="pt-4">
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
                            {inputMethod === "file" ? (
                                <AppTooltip content="Re-run batch enhancement with all jobs from the uploaded file.">
                                    <Button
                                        variant="secondary"
                                        onClick={onRegenerateBatch}
                                        className="w-full h-10 sm:h-11"
                                        aria-label="Regenerate all jobs from uploaded file"
                                    >
                                        Regenerate All Jobs
                                    </Button>
                                </AppTooltip>
                            ) : (
                                <AppTooltip content="Re-run enhancement with the same job details.">
                                    <Button
                                        variant="secondary"
                                        onClick={onRegenerateSingle}
                                        className="w-full h-10 sm:h-11"
                                        aria-label="Regenerate CV with same job details"
                                    >
                                        Regenerate
                                    </Button>
                                </AppTooltip>
                            )}
                            <AppTooltip content="Return to job details, keep your uploaded CV, and edit the job info.">
                                <Button
                                    variant="secondary"
                                    onClick={onBackToJobDetails}
                                    className="w-full h-10 sm:h-11"
                                    aria-label="Go back to job details step"
                                >
                                    Back to Job Details
                                </Button>
                            </AppTooltip>
                        </div>

                        {/* Start Over Button */}
                        <AppTooltip content="Reset everything and upload a new CV.">
                            <Button
                                variant="destructive"
                                onClick={onStartOver}
                                className="w-full h-10 sm:h-11"
                                aria-label="Start over with new CV upload"
                            >
                                Start Over
                            </Button>
                        </AppTooltip>
                    </div>
                </CardContent>
            </Card>
        </motion.div>
    );
};

export default DownloadStep;
