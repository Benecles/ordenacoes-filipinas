#!/usr/bin/env python3
"""When each course last changed, and when its backstage last caught up (20/10: "a system for knowing when the
backstage is out of date"). Read by backstage/bar.js (marks a back that lags its course) and by the CEO's bell.

  course  last commit touching courses/<c>/
  back    last commit touching backstage/<c>/ or backstage/courses/<c>/, or now when --rebuilt (CI rebuilt it)
usage: backstage_fresh.py OUT_DIR [--rebuilt]   writes OUT_DIR/backstage/fresh.json
"""
import datetime as dt, json, os, subprocess, sys

def last(*paths):
    return subprocess.run(['git', 'log', '-1', '--format=%cI', '--', *paths], capture_output=True, text=True).stdout.strip()

now = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
out = {}
for c in sorted(os.listdir('courses')):
    if not os.path.isdir(os.path.join('courses', c)): continue
    course = last(f'courses/{c}')
    back = now if '--rebuilt' in sys.argv else last(f'backstage/{c}', f'backstage/courses/{c}')
    if course: out[c] = {'course': course, 'back': back or None}
os.makedirs(os.path.join(sys.argv[1], 'backstage'), exist_ok=True)
json.dump({'at': now, 'courses': out}, open(os.path.join(sys.argv[1], 'backstage', 'fresh.json'), 'w'), indent=1)
stale = [c for c, d in out.items() if not d['back'] or dt.datetime.fromisoformat(d['back']) < dt.datetime.fromisoformat(d['course'])]
print('fresh:', len(out), 'courses;', 'behind: ' + ', '.join(stale) if stale else 'none behind')
