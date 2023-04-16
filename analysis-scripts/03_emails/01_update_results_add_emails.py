#/bin/env python3

# call: python dotfiles-analyse/03_emails/01_update_results_add_emails.py results.db 03_analyses/gitleaks_02_own_regexes/analyses/all_emails_compressed.csv 1000

import os, sys, re
import sqlite3, csv
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("db", help="SQlite Database file")
parser.add_argument("input", help="Input file (CSV)")
parser.add_argument("total", help="Total Number of Items", type=int)
args = parser.parse_args()

db = sqlite3.connect(args.db)


def create_tables(db):
    db.execute('''
        CREATE TABLE IF NOT EXISTS email (
            email_id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            count_per_file INTEGER NOT NULL,
            stat_tf INTEGER,
            stat_tf_idf INTEGER,
            file_id INTEGER NOT NULL,
            FOREIGN KEY (file_id) REFERENCES file (file_id)
        );
    ''')
    db.commit()
create_tables(db)


# p = re.compile(r'\./([^/]*)/(.*): (\S*)')
unicode_decode_error_count = 0
with open(args.input, mode="r", newline='') as f:
    pbar = tqdm(total=args.total)
    testvals = 0
    reader = csv.reader(f)
    for row in reader:
        pbar.update(); testvals+=1
        if len(row) != 4:
            print('wrong length ({}): {}'.format(len(row), str(row)), file=sys.stderr)
            continue

        (count_per_file, email, file_path, repo_folder) = row

        repo_folder = repo_folder.removesuffix('.json')

        if testvals < 1000 and (testvals-5) % 100 == 0:
            print('TESTVALS: count_per_file: {}, email: {}, file_path: {}, repo_folder: {}'.format(
                count_per_file, email, file_path, repo_folder
            ))
        
        try:
            db.execute('''
                INSERT INTO email
                    (email, count_per_file, file_id)
                VALUES
                (
                    ?,
                    ?,
                    (
                        SELECT file_id FROM file f JOIN repo r ON f.repo_id = r.repo_id
                        WHERE
                        folder_name = ? AND
                        file_path = ?
                    )
                );
                ''',
                (
                    email,
                    count_per_file,
                    repo_folder,
                    file_path
                ))
            db.commit()
        except sqlite3.IntegrityError:
            print('integrityError: {}'.format(str(row)), file=sys.stderr)
    pbar.close()
db.close()
