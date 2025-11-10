"use client";

import { Scissors } from "lucide-react";

import { useAppSelector, useAppDispatch } from "@/store/hooks";
import { setSliceProjects } from "@/store/slices/modelSelectionSlice";

import { Checkbox } from "@/components/ui/Checkbox";
import { AppTooltip } from "@/components/ui/Tooltip";

interface SliceProjectsCheckboxProps {
    id?: string;
    showDescription?: boolean;
}

const SliceProjectsCheckbox = ({
    id = "slice-projects",
    showDescription = true,
}: SliceProjectsCheckboxProps) => {
    const dispatch = useAppDispatch();

    const sliceProjects = useAppSelector(
        (state) => state.modelSelection.sliceProjects
    );

    return (
        <div className="space-y-2">
            <div className="flex items-center space-x-2">
                <Checkbox
                    id={id}
                    checked={sliceProjects}
                    onCheckedChange={(checked: boolean) =>
                        dispatch(setSliceProjects(checked))
                    }
                />
                <label
                    htmlFor={id}
                    className="flex items-center gap-2 text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                >
                    <Scissors className="size-4 text-primary" />
                    Slice personal projects to fit one page
                </label>
            </div>
            {showDescription && (
                <AppTooltip content="Keeps the CV concise by limiting projects to the most relevant ones.">
                    <p className="text-xs text-muted-foreground ml-6">
                        When enabled, AI selects up to 3 most relevant projects
                        to keep your CV one page.
                    </p>
                </AppTooltip>
            )}
        </div>
    );
};

export default SliceProjectsCheckbox;
