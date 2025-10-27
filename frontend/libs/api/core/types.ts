export interface AIModel {
    id: string;
    name: string;
    description: string;
    provider: string;
    default: boolean;
}

export interface ModelsResponse {
    models: AIModel[];
    default_model: string;
}

export interface Section {
    title: string;
    content: string;
}

export interface UploadResponse {
    session_id: string;
    sections: Section[];
    original_filename: string;
}

export interface AlignResponse {
    session_id: string;
    tex_path: string;
    pdf_path: string | null;
    clean_tex_filename?: string;
    clean_pdf_filename?: string | null;
}

export interface BatchJobResult {
    job_title: string;
    company_name?: string | null;
    tex_path: string;
    pdf_path: string | null;
}

export interface BatchAlignResponse {
    session_id: string;
    jobs_count: number;
    results: BatchJobResult[];
    zip_path: string;
}

export interface ProgressResponse {
    current: number;
    total: number;
    percent: number;
    status: string;
    message: string;
    zip_path?: string | null;
    errors: number;
}

export interface PreviewFileResponse {
    headers: string[];
    rows: string[][];
}

export interface ApiResponse<T> {
    success: boolean;
    data: T;
}
