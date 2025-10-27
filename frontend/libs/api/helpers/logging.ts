export function logRequestStart(
    context: string,
    details: Record<string, any>
): void {
    console.log(`=== ${context} ===`);
    Object.entries(details).forEach(([key, value]) => {
        console.log(`${key}:`, value);
    });
}

export function logRequestError(context: string, error: any): void {
    console.error(`❌ ${context} error:`, error);
}
