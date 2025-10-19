import * as React from "react";

import { cn } from "@/lib/utils";

function Textarea({ className, ...props }: React.ComponentProps<"textarea">) {
    return (
        <textarea
            data-slot="textarea"
            className={cn(
                "placeholder:text-foreground h-36 w-full bg-white px-4 py-3 text-base outline-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm nb-border nb-shadow",
                className
            )}
            {...props}
        />
    );
}

export { Textarea };
