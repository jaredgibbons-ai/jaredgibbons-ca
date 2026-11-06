// True in every normal build (the whole preview is closed). The launch build (PUBLIC_PREVIEW=false, needs Jared's approval) sets it false,
// which removes the review notes ("Draft for ...", "Open item ...", "not connected in the preview") from the page output.
export const isPreview: boolean = import.meta.env.PUBLIC_PREVIEW !== 'false';
export const isDraftNote = (t: unknown): boolean => String(t).startsWith('Draft for Jared');
