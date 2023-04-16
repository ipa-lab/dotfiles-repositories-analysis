#/bin/python3

import os, sys, re
import sqlite3, csv
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("db", help="SQlite Database file")
parser.add_argument("input", help="Input file")
parser.add_argument("total", help="Total Number of Items", type=int)
args = parser.parse_args()

db = sqlite3.connect(args.db)

# adapted from stackoverflow: https://stackoverflow.com/questions/18970830/how-to-find-null-byte-in-a-string-in-python
def readtuples(f, bufsize):
    buf = b''
    data = True
    while data:
        data = f.read(bufsize)
        buf += data
        lines = buf.split(b'\x00')
        buf = lines.pop()
        for line in lines:
            yield line.rstrip() # i try to remove the newline here, because it has been added additionally
    # yield buf + '\x00'


# p = re.compile(r'\./([^/]*)/(.*): (\S*)')
unicode_decode_error_count = 0
with open(args.input, mode="rb") as f:
    pbar = tqdm(total=args.total) 
    for full_path_r in readtuples(f, 65536):
        pbar.update()
        try:
            full_path = full_path_r.decode('utf-8')
        except UnicodeDecodeError as e:
            print("UnicodeDecodeError: ", e, file=sys.stderr)
            unicode_decode_error_count += 1
            continue

        match = re.search(r'\s*(\d+)\s*(\d+)\s*\./([^/]*)/(.*)', full_path)
        if match is None:
            print("Match Error in line: {}".format(full_path))
            continue
        (no_lines, no_bytes, repo_folder, file_path) = match.groups()
        file_name = re.search(r'([^/]*)$', file_path).group(1)
        # print("folder_name: {}, file_path: {}, file_name: {}, lines: {}, bytes: {}".format(
        #     repo_folder, file_path, file_name, no_lines, no_bytes)
        # )
        # continue
        db.execute('''
            UPDATE OR IGNORE file SET
                size = ?, no_lines = ?
            WHERE
                file_path = ? AND
                repo_id = (
                    SELECT repo_id FROM repo
                    WHERE
                    folder_name = ?
                );
            ''',
            (
                no_bytes, no_lines,
                file_path,
                repo_folder
            ))
        db.commit()
    pbar.close()
db.close()
