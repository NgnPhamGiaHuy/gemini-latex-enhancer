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

export const AppTooltip = ({ content, children, side = "top", align = "center", className }: TooltipProps) => {
    return (
        <TooltipPrimitive.Root delayDuration={200} disableHoverableContent={false}>
            <TooltipPrimitive.Trigger asChild>{children}</TooltipPrimitive.Trigger>
            <TooltipPrimitive.Portal>
                <TooltipPrimitive.Content side={side} align={align} sideOffset={8} className={cn("z-50 rounded-md bg-popover px-3 py-2 text-xs text-popover-foreground shadow-md border", "data-[state=delayed-open]:data-[side=top]:animate-in data-[state=delayed-open]:data-[side=top]:fade-in-0 data-[state=delayed-open]:data-[side=top]:slide-in-from-bottom-1", "max-w-[260px]", className)}>
                    {content}
                    <TooltipPrimitive.Arrow className="fill-popover" />
                </TooltipPrimitive.Content>
            </TooltipPrimitive.Portal>
        </TooltipPrimitive.Root>
    );
};

export const AppTooltipProvider = TooltipPrimitive.Provider;
