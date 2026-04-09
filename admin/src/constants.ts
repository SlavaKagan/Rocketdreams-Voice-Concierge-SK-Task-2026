export const FAQ_CATEGORIES = [
  "General",
  "Gaming",
  "Dining",
  "Accommodations",
  "Bars",
  "Entertainment",
  "Events",
  "Partners",
] as const;

export type FAQCategory = typeof FAQ_CATEGORIES[number];