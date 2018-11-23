#!/usr/bin/env python3
# https://stackoverflow.com/questions/13613336/python-concatenate-text-files
# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
import sys, os

def main():
    assert len(sys.argv)==2
    outbibfpath = sys.argv[1]
    indir = os.path.dirname(os.path.realpath(__file__))
    outdir = os.path.dirname(outbibfpath)

    bib_keys = normalize(find_bib(indir))
    cite_keys = find_cite(outdir)

    with open(outbibfpath, 'w') as outfile:
        for ck in cite_keys:
            ck = normalize(ck)

        for fname in os.listdir(indir):
            if fname in ['merge.py', 'README.md', 'LICENSE', '.git']: continue
            with open(os.path.join(indir, fname), 'r') as infile:
                print(infile.read())
                exit()
                outfile.write(infile.read())

def normalize(keys):
    delim = '_'; normalized_keys = []
    for k in keys:
        normalized_keys.append( delim.join(sorted(k.split(delim))) )
    return normalized_keys

def find_bib(indir):
    bib_keys = []
    for fname in os.listdir(indir):
        if fname in ['merge.py', 'README.md', 'LICENSE', '.git']: continue
        bib_keys.append(fname.replace('.bib',''))
    return bib_keys

def find_cite(outdir):
    def find(fpath):
        keys = ['\cite{', '\citep{']
        cite_keys = []
        with open(fpath, 'r') as f:
            for row in f:
                row = row.strip()
                for k in keys:
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
