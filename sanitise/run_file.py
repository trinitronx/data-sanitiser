#!/usr/local/bin/python3
'''
    run_file.py: Runs sanitize module on filename passed as argv[1]
'''
import sys
import os
import time
import fileinput
import tqdm
import nltk
import sanitise

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

if len(sys.argv) < 2:
    print('Exit code 10: Please enter a string to regexReplace and optionally -v for verbose')
    sys.exit(10)

def main():
    '''
    Main function for run_file.py
    '''
    filename = sys.argv[1]
    debug = False
    test_list = ''
    milli_sec_start = int(round(time.time() * 1000))

    if len(sys.argv) == 3:
        if sys.argv[2] == '-v':
            debug = True

    with tqdm.tqdm(total=os.path.getsize(filename)) as pbar:
        for line in fileinput.FileInput(filename, inplace=1):
            original = line

            replaced_line = sanitise.tokenise(line)
            replaced_line = sanitise.replacePPI(line)
            if debug:
                sys.stderr.write('%-20s "%s"' % ('Unsanitised', original))
                sys.stderr.write('%-20s "%s"' % ('Test list: ', test_list))
                sys.stderr.write(original)
                sys.stderr.write(replaced_line)

            pbar.update(len(line))
            # fileinput will write stdout to file in place
            sys.stdout.write((replaced_line))

    if debug:
        milli_sec_end = int(round(time.time() * 1000))
        sys.stderr.write('%-20s "%s"' %
                         ('Processing time milli seconds: ', milli_sec_end - milli_sec_start))

if __name__ == "__main__":
    main()
