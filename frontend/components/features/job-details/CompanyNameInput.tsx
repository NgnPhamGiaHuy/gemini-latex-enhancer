"use client";

import { Input } from "@/components/ui/Input";
import { AppTooltip } from "@/components/ui/Tooltip";
import { setCompanyName } from "@/store/slices/jobDataSlice";
import { useAppSelector, useAppDispatch } from "@/store/hooks";

interface CompanyNameInputProps {
    touched: boolean;
    error?: string;
    onBlur: () => void;
}

const CompanyNameInput = ({
    touched,
    error,
    onBlur,
}: CompanyNameInputProps) => {
    const dispatch = useAppDispatch();
    const companyName = useAppSelector((state) => state.jobData.companyName);

    return (
        <div className="space-y-2">
            <label className="text-sm font-medium">Company Name</label>
            <AppTooltip content="Optional. Improves tone and relevance if provided.">
                <Input
                    placeholder="e.g., Google, Microsoft"
                    value={companyName}
                    onChange={(e) => dispatch(setCompanyName(e.target.value))}
                    onBlur={onBlur}
                    className="h-11"
                />
            </AppTooltip>
            {touched && error && (
                <p className="text-sm text-red-500">{error}</p>
            )}
        </div>
    );
};

export default CompanyNameInput;
