import type { ContentItem } from "./ContentItem";

export type APIResponse = {
    content: ContentItem[];
    author: (ContentItem | null)[];
    title: string;
    fetchStatus: string;
};
