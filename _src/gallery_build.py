"""Build the gallery from the class's sorted Drive folders (work/drive2, the "ButterflyRanchShotList" folders, 2026-10-25).
Per category: fix orientation, drop near-duplicates (keeps the sharpest of a burst), drop blurry or very dark frames,
write a wall thumb and a viewer size (webp) to assets/gallery/<cat>/, and assets/gallery/gallery.json with the rope's
picks. Class/Team photos are left out: they show students' faces, which need their OK. EXCLUDE lists files to leave out
after a look at the contact sheets (faces, near-misses). Run: python _src/gallery_build.py [--sheets]"""
import json, os, sys
from PIL import Image, ImageOps, ImageFilter, ImageStat, ImageDraw
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.dirname(SITE), 'work', 'drive2')
OUT = os.path.join(SITE, 'assets', 'gallery')

CATS = [  # key, folder, tab title, lede, alt text for every photo in it
    ('horses', 'Horses- No Sorting- All Horses', 'The horses',
     'Every horse at the ranch, as the class found them on 23 October 2026: at the fence, in the pens, out in the pasture.',
     'A horse at Butterfly Rescue Ranch'),
    ('ranch', 'Landscape_Ranch Shots', 'The ranch',
     'Seven acres outside Norman: the pink sign, the pens, the pasture, the wildflowers and a lot of Oklahoma sky.',
     'Butterfly Rescue Ranch, Norman, Oklahoma'),
    ('work', 'Staff_Working Shots', 'At work',
     'Feeding, grooming, leading and mucking out. This is what a day of care looks like.',
     'Care and work at Butterfly Rescue Ranch'),
    ('zoo', 'Petting Zoo Animals', 'The petting zoo',
     'Goats, a pig and the rest of the small crew who come to pony parties and camps.',
     'An animal in the Butterfly Ranch petting zoo'),
]
EXCLUDE = {   # after a look at every contact sheet, 2026-10-25 (files are unique per folder, so one set serves all)
    # students' faces (need their OK; ranch staff in the maroon polos stay)
    '000435.jpg', '000436.jpg', '000441.jpg', '000784.jpg', '000788.jpg', '000797.jpg', '000798.jpg',
    # filler: legs only, dirt, hoses, a trunk, clutter
    '000093.jpg', '000100.jpg', '000245.jpg', '000247.jpg', '000321.jpg', '000323.jpg', '000606.jpg', '000620.jpg',
    '000248.jpg', '000249.jpg', '000332.jpg', '000337.jpg', '000405.jpg', '000412.jpg', '000416.jpg', '000421.jpg',
    '000083.jpg', '000085.jpg', '000094.jpg', '000394.jpg', '000396.jpg', '000397.jpg', '000877.jpg', '000135.jpg',
    '000442.jpg', '000448.jpg', '000753.jpg', '000781.jpg', '000214.jpg',
    # near-repeats the burst grouping missed
    '000099.jpg', '000116.jpg', '000134.jpg', '000136.jpg', '000142.jpg', '000207.jpg', '000212.jpg', '000213.jpg',
    '000481.jpg', '000492.jpg', '000505.jpg', '000536.jpg', '000559.jpg', '000574.jpg', '000587.jpg', '000599.jpg',
    '000640.jpg', '000660.jpg', '000673.jpg', '000683.jpg', '000684.jpg', '000763.jpg', '000807.jpg', '000825.jpg',
    '000831.jpg', '000043.jpg', '000044.jpg', '000108.jpg', '000326.jpg', '000327.jpg', '000328.jpg', '000362.jpg',
    '000363.jpg', '000366.jpg', '000369.jpg', '000170.jpg', '000174.jpg', '000178.jpg', '000179.jpg', '000180.jpg',
    '000279.jpg', '000471.jpg', '000591.jpg', '000894.jpg', '000897.jpg', '000424.jpg',
}
ROPE = [   # (category, file, title on the print, caption under the rope) — no horse names: those are Braxton's to give
    ('horses', '000507.jpg', 'Hello there', 'A chestnut with a white blaze, right up at the fence.'),
    ('ranch', '000196.jpg', 'The pink sign', 'Butterfly Ranch, wildflowers and all.'),
    ('horses', '000639.jpg', 'Two noses', 'Nobody here is shy about visitors.'),
    ('zoo', '000855.jpg', 'The donkey', 'One of the petting-zoo crew.'),
    ('horses', '000800.jpg', 'Up close', 'The paint checks the camera for treats.'),
    ('work', '000181.jpg', 'Breakfast', 'Grain in the pink bucket, every morning.'),
    ('horses', '000724.jpg', 'The pony', 'Small, blond and in charge.'),
    ('ranch', '000359.jpg', 'The front gate', '7475 By Drive, Norman.'),
    ('horses', '000155.jpg', 'The welcome party', 'Two of the herd at the feeder.'),
    ('work', '000710.jpg', 'Grooming', 'Brushing out the gray, one stroke at a time.'),
    ('zoo', '000861.jpg', 'The goat', 'He comes to every pony party.'),
    ('horses', '000562.jpg', 'Lightning', 'The bay with the jagged blaze, by the sign.'),
    ('ranch', '000027.jpg', 'October', 'Wildflowers along the pasture fence.'),
    ('horses', '000523.jpg', 'At the gate', 'A paint waiting for whoever comes next.'),
    ('zoo', '000853.jpg', 'Sheep and lamb', 'In the shade of the trailer.'),
    ('horses', '000254.jpg', 'The little pinto', 'The smallest horse on the ranch.'),
]
DUP = 14                  # dHash Hamming distance at or below which two frames count as the same shot


def dhash(im, n=12):
    g = im.convert('L').resize((n + 1, n), Image.LANCZOS); p = list(g.getdata())
    return sum(1 << i for i, (a, b) in enumerate((p[r * (n + 1) + c], p[r * (n + 1) + c + 1]) for r in range(n) for c in range(n)) if a > b)


def sharp(im):
    g = im.convert('L'); g.thumbnail((640, 640))
    return ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).var[0]


def load(path):
    im = Image.open(path); im = ImageOps.exif_transpose(im); return im.convert('RGB')


def main(sheets=False):
    os.makedirs(OUT, exist_ok=True)
    data = {'cats': [], 'rope': []}
    for key, folder, title, lede, alt in CATS:
        d = os.path.join(SRC, folder)
        files = sorted(f for f in os.listdir(d) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')) and f not in EXCLUDE) if os.path.isdir(d) else []
        items = []
        for f in files:
            try:
                im = load(os.path.join(d, f))
            except Exception as e:
                print('  skip', f, e); continue
            small = im.copy(); small.thumbnail((640, 640)); im.close(); del im       # keep only a small copy: 300 full frames won't fit in memory
            items.append({'f': f, 'path': os.path.join(d, f), 'h': dhash(small), 's': sharp(small), 'lum': ImageStat.Stat(small.convert('L')).mean[0]})
        # bursts: the files are numbered in shooting order, and a handheld burst is 40-60 bits apart (a new scene 70+), so a
        # burst = neighbouring numbers (gap <= 4) still close to the burst's first frame. Keep the sharpest of each burst,
        # plus the most different frame when a long burst really moved.
        def num(f):
            digits = ''.join(ch for ch in os.path.splitext(f)[0] if ch.isdigit())
            return int(digits) if digits else 0
        items.sort(key=lambda x: num(x['f'])); runs = []
        for it in items:
            r = runs[-1] if runs else None
            if r and num(it['f']) - num(r[-1]['f']) <= 4 and bin(it['h'] ^ r[0]['h']).count('1') < 64:
                r.append(it)
            else:
                runs.append([it])
        kept = []
        for r in runs:
            best = max(r, key=lambda x: x['s']); kept.append(best)
            if len(r) >= 5:
                far = max(r, key=lambda x: bin(x['h'] ^ best['h']).count('1'))
                if far is not best and bin(far['h'] ^ best['h']).count('1') >= 60:
                    kept.append(far)
        want = {f for c, f, *_ in ROPE if c == key}            # rope picks always stay, whatever the burst filter chose
        kept += [it for it in items if it['f'] in want and it not in kept]
        sh = sorted(x['s'] for x in kept); floor = sh[len(sh) // 8] if len(sh) > 8 else 0   # bottom eighth by sharpness
        kept = [x for x in kept if x['f'] in want or (x['s'] >= floor * 0.9 and x['lum'] > 38)]
        rank = {f: i for i, (c, f, *_) in enumerate(ROPE) if c == key}
        kept.sort(key=lambda x: (0, rank[x['f']]) if x['f'] in rank else (1, x['f']))   # each set opens on its best shots
        print(key, len(files), 'files ->', len(kept), 'kept')
        cd = os.path.join(OUT, key); os.makedirs(cd, exist_ok=True)
        photos = []
        for i, it in enumerate(kept):
            stem = os.path.splitext(it['f'])[0]
            full = load(it['path'])
            big = full.copy(); big.thumbnail((1400, 1400), Image.LANCZOS); big.save(os.path.join(cd, stem + '.webp'), 'WEBP', quality=76, method=5)
            th = full; th.thumbnail((560, 560), Image.LANCZOS); th.save(os.path.join(cd, stem + '-t.webp'), 'WEBP', quality=70, method=5)
            photos.append({'src': f'assets/gallery/{key}/{stem}.webp', 'thumb': f'assets/gallery/{key}/{stem}-t.webp', 'w': th.width, 'h': th.height, 'alt': alt, 'file': it['f']})
        data['cats'].append({'key': key, 'title': title, 'lede': lede, 'photos': photos})
        if sheets:
            contact(key, photos)
    for cat, f, t, cap in ROPE:
        stem = os.path.splitext(f)[0]
        data['rope'].append({'cat': cat, 'thumb': f'assets/gallery/{cat}/{stem}-t.webp', 'title': t, 'caption': cap, 'alt': t})
    for c in data['cats']:
        for p in c['photos']:
            p.pop('file', None)
    json.dump(data, open(os.path.join(OUT, 'gallery.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('gallery.json:', sum(len(c['photos']) for c in data['cats']), 'photos,', len(data['rope']), 'on the rope')


def contact(key, photos):
    """Numbered contact sheets (work/gallery-sheets/<key>-N.jpg) to review faces and pick the rope."""
    outd = os.path.join(os.path.dirname(SITE), 'work', 'gallery-sheets'); os.makedirs(outd, exist_ok=True)
    T, cols = 200, 8
    for s in range(0, len(photos), 48):
        chunk = photos[s:s + 48]; rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * T, rows * (T + 16)), 'white'); dr = ImageDraw.Draw(sheet)
        for i, p in enumerate(chunk):
            im = Image.open(os.path.join(SITE, p['thumb'])); im.thumbnail((T, T))
            x, y = (i % cols) * T, (i // cols) * (T + 16)
            sheet.paste(im, (x + (T - im.width) // 2, y + (T - im.height) // 2)); dr.text((x + 3, y + T + 2), p['file'][:30], fill='black')
        sheet.save(os.path.join(outd, f'{key}-{s // 48 + 1}.jpg'), quality=78)


if __name__ == '__main__':
    main('--sheets' in sys.argv)
