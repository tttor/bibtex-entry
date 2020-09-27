#!/usr/bin/env python3
# https://stackoverflow.com/questions/13613336/python-concatenate-text-files
# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
import sys, os
from glob import glob

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

delim = '_'
ext = '.bib'
cmdtypes = ['\cite{', '\cite[', '\citep{', 'citep[']

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
            outfile.write('\n') # a blank line between 2 entries

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
            for rowidx, row in enumerate(f):
                row = row.strip()
                for cmd in cmdtypes:
                    ncmd = row.count(cmd) # number of cmds found in this row/line
                    if ncmd==0: continue

                    start_idx = 0
                    for _ in range(ncmd):
                        cmd_start_idx = row.find(cmd, start_idx)
                        cmd_end_idx = cmd_start_idx + (len(cmd) - 1)
                        if '[' in cmd: # cmd with option
                            opt_end_idx = row.find(']', cmd_end_idx + 1)
                            cmd_end_idx = opt_end_idx

                        start_idx = row.find('{', cmd_end_idx)
                        end_idx = row.find('}', start_idx)
                        if start_idx==-1 or end_idx==-1: # `-1`: not found
                            print(bcolors.FAIL + '!!! FATAL: can not handle multirow citations !!!')
                            print('FPATH', fpath)
                            print('ROW', rowidx+1, row)
                            exit()
                        cite_str = row[start_idx + 1:end_idx]
                        cite_keys += [i.strip() for i in cite_str.split(',')]
                        start_idx = end_idx+1
        return cite_keys

    tex_fpaths = [y for x in os.walk(outdir) for y in glob(os.path.join(x[0], '*.tex'))] # https://stackoverflow.com/questions/18394147/recursive-sub-folder-search-and-return-files-in-a-list-python
    cite_keys = [_find_cite(fpath) for fpath in tex_fpaths]
    cite_keys = [item for sublist in cite_keys for item in sublist] # https://stackoverflow.com/questions/14807689/python-list-comprehension-to-join-list-of-lists
    return list(set(cite_keys))

if __name__ == '__main__':
    main()
