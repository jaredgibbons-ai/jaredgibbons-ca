// Quick search data (D-255, D-261): pick an area and a home type, land on that search page on this site (each has the live listings
// and the "email me new listings" box). Only real, built, un-gated search pages are offered. Used on the map pages, the homepage hero
// and the homepage quiz result.
import IDX from '../data/idx-embeds.json';
import { isGated } from './inventory';
const idx = IDX as { pages: Record<string, string> };
const PAGE_SLUGS = new Set(Object.keys(import.meta.glob('../data/pages/*.json')).map((k) => k.replace(/^.*\/|\.json$/g, '')));
const LOCAL = import.meta.glob('../data/local/*.json', { eager: true, import: 'default' }) as Record<string, any>;
export const QS_AREAS: [string, string, string, string][] = [   // group, label, slug prefix, the area's all-homes page
  ['South Surrey and White Rock', 'South Surrey', 'south-surrey', 'south-surrey-homes-for-sale'], ['South Surrey and White Rock', 'White Rock', 'white-rock', 'white-rock'],
  ['Langley and Cloverdale', 'Langley', 'langley', 'langley-homes-for-sale'], ['Langley and Cloverdale', 'Cloverdale', 'cloverdale', 'cloverdale-bc'],
  ['Surrey and Delta', 'Surrey', 'surrey', 'surrey-homes-for-sale'], ['Surrey and Delta', 'North Delta', 'north-delta', 'north-delta-homes-for-sale'],
  ['Surrey and Delta', 'Ladner', 'ladner', 'ladner-homes-for-sale'], ['Surrey and Delta', 'Tsawwassen', 'tsawwassen', 'tsawwassen-homes-for-sale'],
  ['Fraser Valley', 'Abbotsford', 'abbotsford', 'abbotsford-homes-for-sale'], ['Fraser Valley', 'Chilliwack', 'chilliwack', 'chilliwack-homes-for-sale'],
  ['Fraser Valley', 'Mission', 'mission', 'mission-homes-for-sale'], ['Fraser Valley', 'Maple Ridge', 'maple-ridge', 'maple-ridge-homes-for-sale'],
  ['Fraser Valley', 'Pitt Meadows', 'pitt-meadows', 'pitt-meadows-homes-for-sale'],
  ['Metro Vancouver', 'Richmond', 'richmond', 'richmond-homes-for-sale'], ['Metro Vancouver', 'Vancouver', 'vancouver', 'vancouver-homes-for-sale'],
  ['Metro Vancouver', 'Burnaby', 'burnaby', 'burnaby-homes-for-sale'], ['Metro Vancouver', 'New Westminster', 'new-westminster', 'new-westminster-homes-for-sale'],
  ['Metro Vancouver', 'Coquitlam', 'coquitlam', 'coquitlam-homes-for-sale'], ['Metro Vancouver', 'Port Coquitlam', 'port-coquitlam', 'port-coquitlam-homes-for-sale'],
  ['Metro Vancouver', 'Port Moody', 'port-moody', 'port-moody-homes-for-sale'],
];
export const QS_TYPES: [string, string][] = [['Houses', 'houses-for-sale'], ['Townhomes', 'townhomes-for-sale'], ['Condos', 'condos-for-sale'], ['Acreages', 'acreages-for-sale'],
  ['Duplexes', 'duplexes-for-sale'], ['Mobile homes', 'mobile-homes'], ['Lots and land', 'lots-land'], ['Farms', 'farms'], ['Open houses', 'open-houses']];
export const qsBuilt = (sl: string) => !!idx.pages[sl] && (PAGE_SLUGS.has(sl) || !!LOCAL[`../data/local/${sl}.json`]?.new_page) && !isGated(sl);
export const quickSearchAreas = () => QS_AREAS.filter(([, , , all]) => qsBuilt(all)).map(([group, label, pre, all]) => ({ group, label, key: pre,
  opts: [['All homes', `/${all}.html`], ...QS_TYPES.filter(([, suf]) => qsBuilt(`${pre}-${suf}`)).map(([t, suf]) => [t, `/${pre}-${suf}.html`])] as [string, string][] }));
export const quickSearchGroups = (areas: { group: string }[]) => [...new Set(areas.map((a) => a.group))];
