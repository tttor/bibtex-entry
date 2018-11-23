#!/usr/bin/env python3
# https://stackoverflow.com/questions/13613336/python-concatenate-text-files
# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
import sys, os

delim = '_'
ext = '.bib'
cmds = ['\cite{', '\citep{']

def main():
    assert len(sys.argv)==2
    outbibfpath = sys.argv[1]
    indir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'entry')
    outdir = os.path.dirname(outbibfpath)
    bib_keys = dict([(normalize_key(k), k) for k in find_bib(indir)])
    cite_keys = find_cite(outdir)

    with open(outbibfpath, 'w') as outfile:
        for ck in cite_keys:
            ck = normalize_key(ck); assert ck in bib_keys.keys()
            with open(os.path.join(indir, bib_keys[ck]+ext), 'r') as infile:
                outfile.write(infile.read().replace(bib_keys[ck], ck))

def normalize_key(k):
    return delim.join(sorted(k.split(delim)))

def find_bib(indir):
    bib_keys = []
    for fname in os.listdir(indir):
        if ext not in fname: continue
        bib_keys.append(fname.replace(ext, ''))
    return bib_keys

def find_cite(outdir):
    def find(fpath):
        cite_keys = []
        with open(fpath, 'r') as f:
            for row in f:
                row = row.strip()
                for k in cmds:
                    cnt = row.count(k)
                    if cnt==0: continue

                    start_idx = 0
                    for c in range(cnt):
                        start_idx = row.find(k, start_idx)
                        end_idx = row.find('}', start_idx )
                        cite_str = row[start_idx:end_idx].replace(k,'')
                        cite_keys += [i.strip() for i in cite_str.split(',')]
                        start_idx = end_idx+1
        return cite_keys
    cite_keys = []
    for fname in os.listdir(outdir):
        if '.tex' not in fname: continue
        cite_keys += find(os.path.join(outdir, fname))
    return list(set(cite_keys))

if __name__ == '__main__':
    main()