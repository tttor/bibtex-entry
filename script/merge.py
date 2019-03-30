#!/usr/bin/env python3
# https://stackoverflow.com/questions/13613336/python-concatenate-text-files
# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
import sys, os
from glob import glob

delim = '_'
ext = '.bib'
cmds = ['\cite{', '\citep{']

def main():
    assert len(sys.argv)==2
    outbibfpath = sys.argv[1]
    outdir = os.path.dirname(outbibfpath)
    entrydir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'entry')
    bib_keys = find_bib(entrydir)
    cite_keys = find_cite(outdir)
    # print(cite_keys)

    with open(outbibfpath, 'w') as outfile:
        for ck in cite_keys:
            if ck not in bib_keys: continue
            with open(os.path.join(entrydir, ck+ext), 'r') as infile:
                outfile.write(infile.read())

def find_bib(entrydir):
    bib_keys = []
    for fname in os.listdir(entrydir):
        if ext not in fname: continue
        bib_keys.append(fname.replace(ext, ''))
    return bib_keys

def find_cite(outdir):
    def _find_cite(fpath):
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
                        if end_idx==-1:
                            print('!!! FATAL: can not handle multirow citations !!!')
                            print(fpath)
                            print(row)
                            exit()
                        cite_str = row[start_idx:end_idx].replace(k,'')
                        cite_keys += [i.strip() for i in cite_str.split(',')]
                        start_idx = end_idx+1
        return cite_keys

    tex_fpaths = [y for x in os.walk(outdir) for y in glob(os.path.join(x[0], '*.tex'))] # https://stackoverflow.com/questions/18394147/recursive-sub-folder-search-and-return-files-in-a-list-python
    cite_keys = [_find_cite(fpath) for fpath in tex_fpaths]
    cite_keys = [item for sublist in cite_keys for item in sublist] # https://stackoverflow.com/questions/14807689/python-list-comprehension-to-join-list-of-lists
    return list(set(cite_keys))

if __name__ == '__main__':
    main()
