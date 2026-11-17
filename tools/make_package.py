"""Make a small website update package for designs.hotplatepottery.com.
Run inside a fresh clone of hotplatepottery/design-book, AFTER
  python3 -I tools/build_site.py <full gallery data dir> .
Usage: python3 -I tools/make_package.py <out.zip>
The zip holds every data/*.json plus only the img/ files the live site doesn't have yet.
If nothing changed, it writes nothing and prints NO CHANGES."""
import sys, subprocess, zipfile, os
out = sys.argv[1]
st = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=all', 'data', 'img'],
                    capture_output=True, text=True, check=True).stdout.splitlines()
if not st:
    print('NO CHANGES'); sys.exit(0)
new_imgs = [l[3:] for l in st if l.startswith('??') and l[3:].startswith('img/')]
with zipfile.ZipFile(out, 'w', zipfile.ZIP_STORED) as z:
    for f in sorted(os.listdir('data')):
        if f.endswith('.json'): z.write(os.path.join('data', f))
    for f in new_imgs: z.write(f)
print(f'{out}: data files + {len(new_imgs)} new images, {os.path.getsize(out)//1024} KB')
