/** Short headings (<= 6 words and <= 40 characters) are set in uppercase; longer ones stay in normal case. Returns a class string to append. */
export const capsClass = (t: unknown): string => {
  const s = String(t ?? '').replace(/<[^>]*>/g, '').trim();
  return s.split(/\s+/).filter(Boolean).length <= 6 && s.length <= 40 ? ' caps' : '';
};
