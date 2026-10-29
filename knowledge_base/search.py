"""Search extracted course pages: python search.py 关键路径 [--limit 10]."""

import argparse
import sqlite3
from pathlib import Path
from build import LOCAL, SOURCE

parser = argparse.ArgumentParser()
parser.add_argument('query')
parser.add_argument('--limit', type=int, default=10)
args = parser.parse_args()
db = sqlite3.connect(LOCAL / 'kb.sqlite')
rows = db.execute('''
    SELECT d.path, p.page_number, p.text FROM pages p
    JOIN documents d ON d.id = p.document_id
    WHERE p.text LIKE ? ORDER BY
      CASE WHEN d.category LIKE '06.%' THEN 0
           WHEN d.category LIKE '02.%' THEN 1
           WHEN d.category LIKE '03.%' THEN 2 ELSE 3 END,
      d.path, p.page_number LIMIT ?
''', ('%' + args.query + '%', args.limit)).fetchall()
for path, page, content in rows:
    pos = content.find(args.query)
    excerpt = content[max(0, pos - 100):pos + len(args.query) + 180].replace('\n', ' ')
    print(f'{SOURCE / path}  第 {page} 页\n  {excerpt}\n')
print(f'{len(rows)} result(s)')
