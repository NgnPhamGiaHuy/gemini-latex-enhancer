"use client";

import { AlertCircle } from "lucide-react";

import { Alert, AlertDescription } from "@/components/ui/Alert";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";

interface ModelErrorStateProps {
    defaultModel: string;
    className?: string;
}

const ModelErrorState = ({ defaultModel, className }: ModelErrorStateProps) => {
    return (
        <Card className={className}>
            <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-base sm:text-lg lg:text-xl">
                    <AlertCircle className="size-5 text-primary" />
                    AI Model Selection
                </CardTitle>
            </CardHeader>
            <CardContent>
                <Alert variant="destructive">
                    <AlertCircle className="size-4" />
                    <AlertDescription>
                        Failed to load available models. Using default model:{" "}
                        {defaultModel}
                    </AlertDescription>
                </Alert>
            </CardContent>
        </Card>
    );
};

export default ModelErrorState;
