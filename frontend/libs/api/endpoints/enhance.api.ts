import { ROUTES } from "../routes";
import { apiClient } from "../core/client";
import { logRequestError, logRequestStart } from "../helpers/logging";

import type { AlignResponse, BatchAlignResponse } from "../core/types";

export interface AlignSectionsParams {
    session_id: string;
    job_title: string;
    job_description: string;
    company_name?: string;
    latex_content: string;
    original_filename?: string;
    model_id?: string;
    slice_projects?: boolean;
}

export const alignSections = async (
    params: AlignSectionsParams
): Promise<AlignResponse> => {
    const formData = new FormData();
    formData.append("session_id", params.session_id);
    formData.append("job_title", params.job_title);
    formData.append("job_description", params.job_description);
    formData.append("latex_content", params.latex_content);

    if (params.company_name) {
        formData.append("company_name", params.company_name);
    }

    if (params.original_filename) {
        formData.append("original_filename", params.original_filename);
    }

    if (params.model_id) {
        formData.append("model_id", params.model_id);
    }

    if (params.slice_projects !== undefined) {
        formData.append("slice_projects", params.slice_projects.toString());
    }

    console.log("FormData created, sending request to:", ROUTES.ENHANCE);

    try {
        const responseData = await apiClient<AlignResponse>(ROUTES.ENHANCE, {
            method: "POST",
            body: formData,
        });

        console.log("✅ Enhance successful, response data:", responseData);
        console.log("=== FRONTEND ENHANCE COMPLETED ===");

        return responseData;
    } catch (error) {
        logRequestError("Enhance", error);
        throw error;
    }
};

export interface AlignSectionsBatchParams {
    session_id: string;
    job_file: File;
    latex_content: string;
    original_filename?: string;
    model_id?: string;
    slice_projects?: boolean;
}

export const alignSectionsBatch = async (
    params: AlignSectionsBatchParams
): Promise<BatchAlignResponse> => {
    logRequestStart("FRONTEND BATCH ENHANCE STARTED", {
        session_id: params.session_id,
        latex_content_length: params.latex_content?.length || 0,
        model_id: params.model_id || "default",
        slice_projects: params.slice_projects || false,
    });

    const formData = new FormData();
    formData.append("session_id", params.session_id);
    formData.append("job_file", params.job_file);
    formData.append("latex_content", params.latex_content);

    if (params.original_filename) {
        formData.append("original_filename", params.original_filename);
    }

    if (params.model_id) {
        formData.append("model_id", params.model_id);
    }

    if (params.slice_projects !== undefined) {
        formData.append("slice_projects", params.slice_projects.toString());
    }

    console.log("FormData created, sending request to:", ROUTES.ENHANCE_BATCH);

    try {
        const responseData = await apiClient<BatchAlignResponse>(
            ROUTES.ENHANCE_BATCH,
            {
                method: "POST",
                body: formData,
            }
        );

        console.log(
            "✅ Batch enhance successful, response data:",
            responseData
        );
        console.log("=== FRONTEND BATCH ENHANCE COMPLETED ===");

        return responseData;
    } catch (error) {
        logRequestError("Batch enhance", error);
        throw error;
    }
};
