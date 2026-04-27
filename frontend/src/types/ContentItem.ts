export interface ContentItemText {
  type: 'text';
  subtype: string | null;
  content: string;
}

export interface ContentItemImage {
  type: 'image';
  subtype: string | null;
  src: string;
  srcset: string | null;
  alt: string;
  caption: string | null;
}

export type ContentItem = ContentItemText | ContentItemImage;