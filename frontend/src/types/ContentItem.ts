export interface ContentItemText {
  type: 'text';
  content: string;
}

export interface ContentItemImage {
  type: 'image';
  src: string;
  srcset: string | null;
  alt: string;
  caption: string | null;
}

export type ContentItem = ContentItemText | ContentItemImage;