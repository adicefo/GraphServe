export interface BaseServiceConfig {
    endpoint: string;
    customEndpoints?: {
        getAll?: string;
        getById?: string;
        create?: string;
        delete?: string;
    };
}
