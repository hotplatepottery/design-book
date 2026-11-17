"""Apply a website update package (from make_package.py) to this clone.
Usage: python3 -I tools/apply_package.py <package.zip>
Replaces data/*.json, adds the new images, removes images no design uses any more,
and checks every design's image exists. Then commit and push."""
import sys, zipfile, os, json, glob
z = zipfile.ZipFile(sys.argv[1])
names = z.namelist()
assert 'data/index.json' in names, 'not a Design Book package'
for n in names:
    assert n.startswith(('data/', 'img/')) and '..' not in n, n
for f in glob.glob('data/*.json'): os.remove(f)
z.extractall('.')
used = set()
for f in glob.glob('data/*.json'):
    d = json.load(open(f))
    if isinstance(d, list): used |= {e['img'] for e in d if e.get('img')}
missing = [u for u in used if not os.path.exists(u)]
assert not missing, f'{len(missing)} images missing, e.g. {missing[:3]}'
gone = [p for p in glob.glob('img/*') if p not in used]
for p in gone: os.remove(p)
idx = json.load(open('data/index.json'))
print('designs:', sum(m['count'] for m in idx['media']), '| new images:', sum(1 for n in names if n.startswith('img/')), '| removed:', len(gone))
