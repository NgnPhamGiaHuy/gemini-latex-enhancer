import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/libs/utils";

const buttonVariants = cva(
    "inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-semibold disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none cursor-pointer nb-border nb-shadow nb-hover-shift",
    {
        variants: {
            variant: {
                default: "bg-accent text-accent-foreground",
                destructive: "bg-destructive text-white",
                outline: "bg-background text-foreground",
                secondary: "bg-secondary text-secondary-foreground",
                ghost: "bg-transparent text-foreground",
                link: "text-foreground underline underline-offset-4",
            },
            size: {
                default: "h-11 px-6 py-2",
                sm: "h-10 gap-1.5 px-4",
                lg: "h-12 px-8",
                icon: "size-11",
                "icon-sm": "size-10",
                "icon-lg": "size-12",
            },
        },
        defaultVariants: {
            variant: "default",
            size: "default",
        },
    }
);

function Button({
    className,
    variant,
    size,
    asChild = false,
    ...props
}: React.ComponentProps<"button"> &
    VariantProps<typeof buttonVariants> & {
        asChild?: boolean;
    }) {
    const Comp = asChild ? Slot : "button";

    return (
        <Comp
            data-slot="button"
            className={cn(buttonVariants({ variant, size, className }))}
            {...props}
        />
    );
}

export { Button, buttonVariants };
