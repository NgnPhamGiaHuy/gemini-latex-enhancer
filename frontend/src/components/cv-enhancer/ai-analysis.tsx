"use client";

import { Brain } from "lucide-react";
import { useAIAnalysis } from "@/hooks";

import type { AIAnalysisProps } from "@/types";

import { LoadingCard } from "@/components/ui/loading";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const AIAnalysis = ({ summary, loading }: AIAnalysisProps) => {
    const { sections, hasContent } = useAIAnalysis(summary);

    return (
        <LoadingCard isLoading={loading}>
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Brain className="h-5 w-5 text-primary" />
                        AI Analysis
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <ScrollArea className="h-120">
                        <div className="whitespace-pre-wrap text-sm leading-relaxed pr-4">
                            {hasContent ? (
                                <div className="text-muted-foreground text-sm leading-relaxed">
                                    {sections.map((section, index) => {
                                        if (section.isHeader) {
                                            return (
                                                <div key={index} className="mb-1">
                                                    <div className="font-semibold text-foreground uppercase leading-5">{section.title}</div>
                                                </div>
                                            );
                                        } else {
                                            return (
                                                <div key={index} className="mb-3 text-sm leading-normal">
                                                    {section.content}
                                                </div>
                                            );
                                        }
                                    })}
                                </div>
                            ) : (
                                <div className="text-muted-foreground italic">No summary available</div>
                            )}
                        </div>
                    </ScrollArea>
                </CardContent>
            </Card>
        </LoadingCard>
    );
};

export default AIAnalysis;
