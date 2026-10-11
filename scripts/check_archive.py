#!/usr/bin/env python3
"""Check the extracted release candidate using the Python standard library."""
from pathlib import Path
import csv, hashlib, sys, zipfile
root=Path(__file__).resolve().parent.parent
errors=[]; count=0
with (root/'docs/FILE_MANIFEST_SHA256.tsv').open(encoding='utf8') as f:
    for row in csv.DictReader(f,delimiter='	'):
        p=root/row['path']
        if not p.is_file(): errors.append('MISSING '+row['path']);continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
            errors.append('CHANGED '+row['path'])
        count+=1
for p in (root/'results/metrics').iterdir():
    if p.suffix not in ('.json','.zip'): continue
    if not zipfile.is_zipfile(p): errors.append('NOT_EVO_ZIP '+str(p))
    else:
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None or 'stats.json' not in z.namelist():
                errors.append('INVALID_EVO '+str(p))
print('Verified entries:',count,'Status:','PASS' if not errors else 'FAIL')
for err in errors:print(err,file=sys.stderr)
raise SystemExit(2 if errors else 0)
