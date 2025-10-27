export const findFieldIndex = (
    headers: string[],
    keywords: string[]
): number => {
    for (let i = 0; i < headers.length; i++) {
        const headerLower = headers[i].toLowerCase();
        if (keywords.some((keyword) => headerLower.includes(keyword))) {
            return i;
        }
    }
    return -1;
};

export const extractJobDetailsFromPreview = (preview: {
    headers: string[];
    rows: string[][];
}) => {
    const { headers, rows } = preview;

    if (!headers.length || !rows.length) return null;

    const firstRow = rows[0];

    const jobTitleIndex = findFieldIndex(headers, [
        "title",
        "position",
        "role",
        "job",
    ]);
    const jobDescIndex = findFieldIndex(headers, [
        "description",
        "desc",
        "responsibilities",
        "duties",
    ]);
    const companyIndex = findFieldIndex(headers, [
        "company",
        "employer",
        "organization",
        "firm",
    ]);

    if (jobTitleIndex === -1 || jobDescIndex === -1) {
        return null; // Required fields missing
    }

    return {
        jobTitle: firstRow[jobTitleIndex] || "",
        jobDescription: firstRow[jobDescIndex] || "",
        companyName: companyIndex >= 0 ? firstRow[companyIndex] || "" : "",
    };
};
