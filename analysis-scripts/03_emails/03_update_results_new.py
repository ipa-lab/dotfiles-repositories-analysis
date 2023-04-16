import os, sys, re
import sqlite3, csv
import argparse
from tqdm import tqdm
import json

args = {
    "source_folders": ["/home/gjungwirth/data/02_data/03_analyses/gitleaks_02_own_regexes/output",
        "/home/gjungwirth/data/02_data/03_analyses/gitleaks_02_own_regexes/output2"],
    "db": "/home/gjungwirth/data/02_data/results.db"
}

db = sqlite3.connect(args['db'])

db.execute('''
CREATE TABLE IF NOT EXISTS email (
    email_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    file_id INTEGER NOT NULL,
    commit_id TEXT NOT NULL,
    author TEXT NOT NULL,
    author_email TEXT NOT NULL,
    commit_date TEXT NOT NULL,
    count_per_file INTEGER NOT NULL,
    tfidf_per_repo INTEGER,
    FOREIGN KEY (file_id) REFERENCES file (file_id),
    UNIQUE (file_id, email)
);
''')
db.commit()


src_files = []
for folder in args['source_folders']:
    for root, dirs, filenames in os.walk(folder):
        for filename in filenames:
            repo_folder_name = filename.removesuffix('.json')
            src_files.append([repo_folder_name, os.path.join(root,filename)])

len(src_files)


pbar = tqdm(total=len(src_files))
res = []
for repo_folder, output_file in src_files:
    with open(output_file) as f:
        data = json.load(f)
        for leak in data:
            assert( leak['repo'] == repo_folder )
            file_name = re.search(r'([^/]*)$', leak['file']).group(1)
            my_vars = {
                    "foldername": leak['repo'],
                    "filename": file_name,
                    "filepath": leak['file'],
                    "offender": leak['offender'],
                    "commit": leak['commit'],
                    "author": leak['author'],
                    "email": leak['email'],
                    "mydate": leak['date']
                }
            db.execute('''
                INSERT OR IGNORE INTO file
                (repo_id, file_name, file_path, is_deleted, size, sha, mime, no_lines)
                VALUES
                (
                    (SELECT repo_id FROM repo WHERE folder_name = :foldername),
                    :filename, :filepath,
                    TRUE,
                    -1, "", "", -1
                );''', my_vars)
            db.execute('''
                INSERT OR IGNORE INTO email
                (file_id,
                email, commit_id, author, author_email, commit_date,
                count_per_file)
                VALUES
                (
                    (SELECT file_id FROM file f JOIN repo r ON f.repo_id=r.repo_id WHERE r.folder_name = :foldername AND f.file_path = :filepath),
                    :offender, :commit, :author, :email, :mydate,
                    0
                );''', my_vars)
            db.execute('''
                UPDATE  email SET count_per_file = count_per_file +1 WHERE
                file_id = (SELECT file_id FROM file f JOIN repo r ON f.repo_id=r.repo_id
                    WHERE r.folder_name = :foldername AND f.file_path = :filepath) AND
                    email = :offender;
                ''', my_vars)
            db.commit()
    pbar.update()


db.close()


