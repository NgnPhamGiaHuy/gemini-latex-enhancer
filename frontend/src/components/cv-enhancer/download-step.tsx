"use client";

import { motion } from "framer-motion";
import { CheckCircle } from "lucide-react";

import type { DownloadStepProps } from "@/types";

import DownloadLinks from "./download-links";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const DownloadStep = ({ step, generateResult, onStartOver }: DownloadStepProps) => {
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

                    <div className="pt-4 border-t">
                        <Button variant="outline" onClick={onStartOver} className="w-full">
                            Start Over
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </motion.div>
    );
};

export default DownloadStep;
