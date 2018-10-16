#!/usr/bin/env python3
# https://stackoverflow.com/questions/13613336/python-concatenate-text-files
# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
import sys, os

def main():
    assert len(sys.argv)==2
    outbibfpath = sys.argv[1]
    indir = os.path.dirname(os.path.realpath(__file__))

    with open(outbibfpath, 'w') as outfile:
        for fname in os.listdir(indir):
            if fname in ['merge.py', 'README.md', 'LICENSE', '.git']: continue
            with open(os.path.join(indir, fname), 'r') as infile:
                outfile.write(infile.read())

if __name__ == '__main__':
    main()
