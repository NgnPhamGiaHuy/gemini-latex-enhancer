"use client";

import * as TooltipPrimitive from "@radix-ui/react-tooltip";

import { cn } from "@/lib/utils";

type TooltipProps = {
    content: string;
    children: React.ReactNode;
    side?: "top" | "right" | "bottom" | "left";
    align?: "start" | "center" | "end";
    className?: string;
};

export const AppTooltip = ({
    content,
    children,
    side = "top",
    align = "center",
    className,
}: TooltipProps) => {
    return (
        <TooltipPrimitive.Root
            delayDuration={200}
            disableHoverableContent={false}
        >
            <TooltipPrimitive.Trigger asChild>
                {children}
            </TooltipPrimitive.Trigger>
            <TooltipPrimitive.Portal>
                <TooltipPrimitive.Content
                    side={side}
                    align={align}
                    sideOffset={8}
                    className={cn(
                        "z-50 bg-white px-3 py-2 text-xs text-foreground nb-border nb-shadow",
                        "max-w-[260px]",
                        className
                    )}
                >
                    {content}
                </TooltipPrimitive.Content>
            </TooltipPrimitive.Portal>
        </TooltipPrimitive.Root>
    );
};

export const AppTooltipProvider = TooltipPrimitive.Provider;
