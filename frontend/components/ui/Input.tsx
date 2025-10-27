import * as React from "react";

import { cn } from "@/libs/utils";

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
    return (
        <input
            type={type}
            data-slot="input"
            className={cn(
                "file:text-foreground placeholder:text-foreground selection:bg-accent selection:text-accent-foreground h-12 w-full min-w-0 bg-white px-4 py-2 text-base outline-none file:inline-flex file:h-8 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm nb-border nb-shadow",
                className
            )}
            {...props}
        />
    );
}

export { Input };
