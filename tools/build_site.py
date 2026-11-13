"""Turn the Design Book artifact's data/*.json (images embedded as base64) into a fast website:
small data/*.json that point at separate image files in img/. Browsers then load only the
pictures on screen instead of ~35 MB of text before anything shows.
Usage: python3 -I tools/build_site.py <artifact data dir> <repo root>"""
import sys, os, json, base64, hashlib, glob, re
SRC, ROOT = sys.argv[1], sys.argv[2]
data_out, img_out = os.path.join(ROOT, 'data'), os.path.join(ROOT, 'img')
os.makedirs(data_out, exist_ok=True); os.makedirs(img_out, exist_ok=True)
for f in glob.glob(os.path.join(data_out, '*.json')): os.remove(f)
keep, n = set(), 0
for f in sorted(glob.glob(os.path.join(SRC, '*.json'))):
    name = os.path.basename(f)
    d = json.load(open(f))
    if name != 'index.json':
        for e in d:
            m = re.match(r'data:image/(\w+);base64,(.*)$', e.get('img', ''), re.S)
            if not m: continue
            b = base64.b64decode(m.group(2)); ext = 'jpg' if m.group(1) in ('jpeg', 'jpg') else m.group(1)
            fn = hashlib.sha1(b).hexdigest()[:16] + '.' + ext
            p = os.path.join(img_out, fn)
            if not os.path.exists(p): open(p, 'wb').write(b)
            keep.add(fn); e['img'] = 'img/' + fn; e.pop('src', None); n += 1
    json.dump(d, open(os.path.join(data_out, name), 'w'), separators=(',', ':'), ensure_ascii=False)
gone = [x for x in os.listdir(img_out) if x not in keep]
for x in gone: os.remove(os.path.join(img_out, x))
print(f'{n} images, {len(keep)} files kept, {len(gone)} removed')
