"use client";

import { useState } from "react";
import { Target } from "lucide-react";

import { useFormValidation } from "@/hooks";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import JobFileUploadSection from "@/components/features/job-details/JobFileUploadSection";
import ManualJobDetailsSection from "@/components/features/job-details/ManualJobDetailsSection";

const JobDetailsForm = ({ loading }: { loading: boolean }) => {
    const [mode, setMode] = useState<"manual" | "file">("manual");
    const [touchedFields, setTouchedFields] = useState({
        jobTitle: false,
        jobDescription: false,
        companyName: false,
    });

    const { isValid, errors, warnings } = useFormValidation();

    const handleFieldBlur = (fieldName: string) => {
        setTouchedFields((prev) => ({ ...prev, [fieldName]: true }));
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Target className="size-5 text-primary" />
                    Target Job Details
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <Tabs
                    value={mode}
                    onValueChange={(v: string) =>
                        setMode(v as "manual" | "file")
                    }
                >
                    <TabsList className="grid grid-cols-2 w-full">
                        <TabsTrigger value="manual">Manual Input</TabsTrigger>
                        <TabsTrigger value="file">File Upload</TabsTrigger>
                    </TabsList>

                    <TabsContent value="manual" className="space-y-4">
                        <ManualJobDetailsSection
                            loading={loading}
                            touchedFields={touchedFields}
                            isValid={isValid}
                            errors={errors}
                            warnings={warnings}
                            handleFieldBlur={handleFieldBlur}
                        />
                    </TabsContent>

                    <TabsContent value="file" className="space-y-4">
                        <JobFileUploadSection loading={loading} />
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card>
    );
};

export default JobDetailsForm;
