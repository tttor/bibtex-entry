#!/usr/bin/env python3
import os, sys

def main():
    indir = os.path.dirname(os.path.realpath(__file__))
    delim = '_'; ext = '.bib'
    for fname in os.listdir(indir):
        if ext not in fname: continue
        with open(os.path.join(indir, fname), 'r') as infile:
            key = fname.replace(ext,'')
            print(key)
            parts = key.split(delim)
            new_key = delim.join([parts[2], parts[0], parts[1]])
            content = infile.read().replace(key, new_key)
            with open(os.path.join(indir, 'tmp', new_key+ext), 'w') as outfile:
                outfile.write(content)

if __name__ == '__main__':
    main()
