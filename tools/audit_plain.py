#!/usr/bin/env python3
"""Finds page sections that are only plain text (no table, card, image, accordion, tiles, form, map) and are long enough to read as a wall of words.
Usage: python3 tools/audit_plain.py [dist] [--min 500] [--csv out.csv]"""
import sys, re, glob, csv, os
from html.parser import HTMLParser
RICH_TAGS = {'table','img','figure','details','form','iframe','svg','picture','canvas','video'}
RICH_CLS = re.compile(r'(lines--links|sourcelist|srclist)|\b(cards|statcards|chips|tiles|linklist|callout|dl|checks|steps|timeline|stats|areamap|awm|idx|faqlist|subs|kv|dtable|plain-ok)\b')
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.secs=[]; s.cur=None; s.depth=0; s.stack=[]; s.skip=0; s.h2=''; s.inh=False; s.main=False
    def handle_starttag(s,t,a):
        a=dict(a); c=a.get('class','') or ''
        if t=='main': s.main=True
        if t in ('script','style'): s.skip+=1
        if s.cur is None and t=='div' and re.search(r'(^|\s)pg(\s|$)',c):
            s.cur={'text':0,'rich':0,'h2':'','h1':False,'p':0,'li':0}; s.depth=1; return
        if s.cur is not None:
            if t=='div' or t=='section' or t=='ul' or t=='ol' or t=='details': s.depth+=1 if t=='div' else 0
            if t in RICH_TAGS or RICH_CLS.search(c): s.cur['rich']+=1
            if t=='p': s.cur['p']+=1
            if t=='li': s.cur['li']+=1
            if t in('h2','h3'): s.inh=True
            if t=='h1': s.cur['h1']=True
    def handle_endtag(s,t):
        if t in ('script','style'): s.skip-=1
        if s.cur is not None:
            if t=='div':
                s.depth-=1
                if s.depth==0: s.secs.append(s.cur); s.cur=None
            if t in('h2','h3'): s.inh=False
    def handle_data(s,d):
        if s.cur is not None and not s.skip:
            d=d.strip()
            if not d: return
            if s.inh and not s.cur['h2']: s.cur['h2']=d
            else: s.cur['text']+=len(d)
def main():
    dist=sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else 'dist'
    mn=int(sys.argv[sys.argv.index('--min')+1]) if '--min' in sys.argv else 500
    out=sys.argv[sys.argv.index('--csv')+1] if '--csv' in sys.argv else None
    rows=[]; pages=0
    for f in sorted(glob.glob(dist+'/**/*.html',recursive=True)):
        h=open(f,errors='ignore').read()
        if 'noindex' in h[:3000] and 'internal' in f: continue
        p=P(); p.feed(h); pages+=1
        for i,s in enumerate(p.secs):
            if s['rich']==0 and s['text']>=mn and not s['h1']:
                rows.append((os.path.relpath(f,dist),i,s['h2'][:60],s['text'],s['p'],s['li']))
    print(f'{pages} pages, {len(rows)} plain-text sections >= {mn} chars, {len({r[0] for r in rows})} pages affected')
    if out:
        with open(out,'w',newline='') as fh: w=csv.writer(fh); w.writerow(['page','section','heading','chars','paragraphs','list_items']); w.writerows(rows)
    return rows
if __name__=='__main__':
    r=main()
    import collections
    c=collections.Counter(x[2] for x in r)
    for k,v in c.most_common(25): print(v,k)
