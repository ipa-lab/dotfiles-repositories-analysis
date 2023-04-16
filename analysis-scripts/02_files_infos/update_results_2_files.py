#/bin/python3

import os, sys, re
import sqlite3, csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("db", help="SQlite Database file", type=str) # usually result.db
parser.add_argument("input", help="Input file") # usually allfiles_mime_00
args = parser.parse_args()

db = sqlite3.connect(args.db)

# adapted from stackoverflow: https://stackoverflow.com/questions/18970830/how-to-find-null-byte-in-a-string-in-python
def readtuples(f, bufsize):
    buf = b''
    data = True
    a = None
    while data:
        data = f.read(bufsize)
        buf += data
        lines = buf.split(b'\x00')
        buf = lines.pop()
        for line in lines:
            if a is None:
                a = line
            else:
                yield (a, line)
                a = None
    # yield buf + '\x00'


# p = re.compile(r'\./([^/]*)/(.*): (\S*)')
unicode_decode_error_count = 0
with open(args.input, mode="rb") as f:
    for (full_path_r, mime_r) in readtuples(f, 10000):
        try:
            full_path = full_path_r.decode('utf-8')
            mime = mime_r.decode('utf-8')
        except UnicodeDecodeError as e:
            print("UnicodeDecodeError: ", e, file=sys.stderr)
            unicode_decode_error_count += 1
            continue

        (repo_folder, file_path) = re.search(r'\./([^/]*)/(.*)', full_path).groups()
        file_name = re.search(r'([^/]*)$', file_path).group(1)
        # print("folder_name: {}, file_path: {}, file_name: {}, mime: {}".format(
        #     repo_folder, file_path, file_name, mime)
        # )
        # continue
        db.execute('''
            INSERT OR IGNORE INTO file
            (repo_id, file_name, file_path, size, sha, mime, no_lines, is_deleted)
            SELECT
            repo_id, ?, ?, 0, '', ?, 0, false
            FROM repo 
            WHERE folder_name = ?;
            ''',
            (
                file_name, file_path, mime,
                repo_folder
            ))
        db.commit()
db.close()
