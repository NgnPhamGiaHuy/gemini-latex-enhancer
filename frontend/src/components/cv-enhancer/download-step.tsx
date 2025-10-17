"use client";

import { motion } from "framer-motion";
import { CheckCircle } from "lucide-react";

import type { DownloadStepProps } from "@/types";

import DownloadLinks from "./download-links";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AppTooltip } from "@/components/ui/tooltip";

const DownloadStep = ({ step, generateResult, onStartOver, onStartAgain, onBackToJobDetails }: DownloadStepProps) => {
    if (step !== "download") return null;

    return (
        <motion.div key="download" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} transition={{ duration: 0.4 }}>
            <Card className="max-w-2xl mx-auto">
                <CardHeader className="text-center pb-6">
                    <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ duration: 0.5, delay: 0.2 }}>
                        <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
                    </motion.div>
                    <CardTitle className="text-2xl">Your Tailored CV is Ready!</CardTitle>
                    <p className="text-muted-foreground">Download your optimized CV in your preferred format</p>
                </CardHeader>
                <CardContent className="space-y-4">
                    <DownloadLinks generateResult={generateResult} />

                    {/* Top row: Regenerate & Back to Job Details side-by-side on >= sm, stacked on mobile */}
                    <div className="pt-4 border-t">
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
                            <AppTooltip content="Re-run enhancement with the same job details.">
                                <Button variant="secondary" onClick={onStartAgain} className="w-full transition-colors duration-200">
                                    Regenerate
                                </Button>
                            </AppTooltip>
                            <AppTooltip content="Return to job details, keep your uploaded CV, and edit the job info.">
                                <Button variant="default" onClick={onBackToJobDetails} className="w-full transition-colors duration-200">
                                    Back to Job Details
                                </Button>
                            </AppTooltip>
                        </div>

                        {/* Bottom: full-width Start Over */}
                        <AppTooltip content="Reset everything and upload a new CV.">
                            <Button variant="outline" onClick={onStartOver} className="w-full transition-colors duration-200">
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
