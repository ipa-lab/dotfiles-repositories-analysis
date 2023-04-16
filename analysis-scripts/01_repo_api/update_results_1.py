#/bin/python3

import os, sys
import sqlite3, csv

db = sqlite3.connect("results.db")

# with open("full_names_and_repo_names") as f:
#     for line in f:
#         full_name, folder_name = line.split()
#         #%% print(full_name)
#         db.execute('UPDATE repo SET folder_name = ? WHERE full_name = ?',
#         (
#             folder_name,
#             full_name
#         ))
#         db.commit()
# db.close()

with open("cloned") as f:
    for line in f:
        folder_name = line.strip()
        db.execute('''
            UPDATE repo
            SET is_downloaded = true
            WHERE folder_name = ?;
            ''',
            (
                folder_name,
            ))
        db.commit()
db.close()
