"use client";

import { Brain, Loader2 } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";

interface ModelLoadingStateProps {
    className?: string;
}

const ModelLoadingState = ({ className }: ModelLoadingStateProps) => {
    return (
        <Card className={className}>
            <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-base sm:text-lg lg:text-xl">
                    <Brain className="size-5 text-primary" />
                    AI Model Selection
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="py-8 flex items-center justify-center">
                    <Loader2 className="size-6 animate-spin text-primary" />
                    <span className="ml-2 text-muted-foreground">
                        Loading AI models...
                    </span>
                </div>
            </CardContent>
        </Card>
    );
};

export default ModelLoadingState;
