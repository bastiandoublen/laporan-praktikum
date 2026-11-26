"""Susun laporan praktikum .docx dari template laporan lama + isi (content.json) + screenshot.

Pakai:
  python -I build_report.py <template.docx> <content.json> <screenshot_dir> <out.docx> <tmp_dir>

Template = laporan praktikum lama dengan struktur: sampul (LAPORAN PRAKTIKUM / Disusun Oleh / NIM),
KATA PENGANTAR, DAFTAR ISI (field TOC), LEMBAR ASISTENSI, "Modul 1 ..." (Heading 1), DAFTAR PUSTAKA (Heading 1).
Isi modul lama dibuang dan diganti isi dari content.json (format: SKILL.md bagian content.json).
Aturan tampilan: references/format-rules.md.
"""
import sys, copy, re, os, json
import docx
from docx.shared import Cm
from docx.oxml.ns import qn
from lxml import etree
from PIL import Image

TPL, CONTENT, SS, OUT, TMP = sys.argv[1:6]
C = json.load(open(CONTENT, encoding='utf-8'))
os.makedirs(TMP, exist_ok=True)
d = docx.Document(TPL)
body = d.element.body
els = list(body.iterchildren())
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
XS = '{http://www.w3.org/XML/1998/namespace}space'
KODE_DIR = C['kode_dir']

def P(el): return docx.text.paragraph.Paragraph(el, d)
def is_p(el): return el.tag == qn('w:p')
def text(el): return P(el).text.strip() if is_p(el) else ''
def style(el): return P(el).style.name if is_p(el) else ''
def has_num(el): return el.find('.//' + qn('w:numPr')) is not None
def has_img(el): return el.find('.//' + qn('w:drawing')) is not None
def has_sect(el): return el.find('.//' + qn('w:sectPr')) is not None
def find(pred, start=0, stop=None):
    for i in range(start, len(els) if stop is None else stop):
        if pred(els[i]): return i
    raise SystemExit('Template tidak sesuai: penanda tidak ditemukan (lihat SKILL.md bagian Template).')

# ---------- penanda template ----------
I_COVER = find(lambda e: text(e).upper() == 'LAPORAN PRAKTIKUM')
I_MATKUL = find(lambda e: text(e) != '', I_COVER + 1)
I_OLEH = find(lambda e: text(e).lower().startswith('disusun oleh'))
I_NAMA = find(lambda e: text(e) != '', I_OLEH + 1)
I_NIM = find(lambda e: text(e).upper().startswith('NIM') or re.fullmatch(r'[\d ]{6,}', text(e)) is not None, I_NAMA + 1)
I_KP = find(lambda e: style(e).startswith('Heading 1') and text(e).upper() == 'KATA PENGANTAR')
I_KP_TXT = find(lambda e: len(text(e)) > 80, I_KP + 1)
I_DATE = find(lambda e: re.match(r'^\w[\w ]*,\s', text(e)) is not None and len(text(e)) < 60, I_KP_TXT + 1)
I_SIGN = I_DATE + 1
I_SIGN_NAME = find(lambda e: text(e) != '', I_SIGN + 1)
I_ASIS = find(lambda e: style(e).startswith('Heading 1') and 'ASISTENSI' in text(e).upper())
I_MOD = find(lambda e: style(e).startswith('Heading 1') and text(e).lower().startswith('modul'))
I_DP = find(lambda e: style(e).startswith('Heading 1') and 'PUSTAKA' in text(e).upper(), I_MOD + 1)
I_ASIS_IMG = next((i for i in range(I_ASIS + 1, I_MOD) if has_img(els[i])), None)

# ---------- prototipe paragraf dari isi modul lama ----------
def proto(i):
    el = copy.deepcopy(els[i])
    for c in list(el):
        if c.tag != qn('w:pPr'): el.remove(c)
    return el
def ppr_of(el):
    ppr = el.find(qn('w:pPr'))
    if ppr is None:
        ppr = etree.Element(qn('w:pPr')); el.insert(0, ppr)
    return ppr
def ppr_add(el, tag):
    ppr = ppr_of(el)
    if ppr.find(qn(tag)) is not None: return ppr.find(qn(tag))
    new = etree.Element(qn(tag)); sty = ppr.find(qn('w:pStyle'))
    if sty is not None: sty.addnext(new)
    else: ppr.insert(0, new)
    return new
def ppr_del(el, *tags):
    for t in tags:
        x = ppr_of(el).find(qn(t))
        if x is not None: ppr_of(el).remove(x)
def set_ind(el, **kw):
    ppr = ppr_of(el); ind = ppr.find(qn('w:ind'))
    if ind is None: ind = etree.SubElement(ppr, qn('w:ind'))
    ind.attrib.clear()
    for k, v in kw.items(): ind.set(qn('w:' + k), str(v))
def set_jc(el, v):
    ppr_add(el, 'w:jc').set(qn('w:val'), v)

i_h2 = find(lambda e: style(e).startswith('Heading 2'), I_MOD, I_DP)
P_H1, P_H2 = proto(I_MOD), proto(i_h2)
P_BODY = proto(find(lambda e: style(e) == 'Normal' and text(e) and not has_sect(e), i_h2, I_DP))
P_LIST = proto(find(lambda e: style(e) == 'List Paragraph' and has_num(e), I_MOD, I_DP))
P_IMG = proto(find(has_img, I_MOD, I_DP))
for pr in (P_BODY, P_IMG, P_LIST):   # bersihkan sisa format template
    ppr_del(pr, 'w:keepNext', 'w:keepLines', 'w:pageBreakBefore')
for pr in (P_BODY, P_IMG):
    ppr_del(pr, 'w:numPr')
for pr in (P_BODY, P_IMG, P_LIST):
    ppr_add(pr, 'w:keepLines')       # paragraf tidak terbelah di dua halaman
set_ind(P_BODY, left=360, firstLine=360)
P_PB = copy.deepcopy(P_BODY)
etree.SubElement(etree.SubElement(P_PB, qn('w:r')), qn('w:br')).set(qn('w:type'), 'page')

# ---------- daftar isi: jarak "A." ke judul = 360 (sama dengan heading), nomor halaman sejajar TOC 1 ----------
def style_el(name):
    try: return d.styles[name].element
    except KeyError: return None
toc1, toc2 = style_el('toc 1'), style_el('toc 2')
right_pos = None
if toc1 is not None:
    t = toc1.find('.//' + qn('w:tab') + f'[@{qn("w:val")}="right"]')
    if t is not None: right_pos = t.get(qn('w:pos'))
if toc2 is not None:
    ind = toc2.find('.//' + qn('w:ind'))
    left2 = int(ind.get(qn('w:left'), '0')) if ind is not None else 0
    for t in toc2.findall('.//' + qn('w:tab')):
        if t.get(qn('w:val')) == 'left': t.set(qn('w:pos'), str(left2 + 360))
        if t.get(qn('w:val')) == 'right' and right_pos: t.set(qn('w:pos'), right_pos)

# judul bagian A.–E. tebal lewat style (bukan format langsung) agar entri daftar isi tidak ikut tebal
h2s = d.styles['Heading 2'].element
h2r = h2s.find(qn('w:rPr'))
if h2r is None: h2r = etree.SubElement(h2s, qn('w:rPr'))
if h2r.find(qn('w:b')) is None: h2r.insert(0, etree.Element(qn('w:b')))

# ---------- numbering ----------
numbering = d.part.numbering_part.element
h2_num = d.styles['Heading 2'].element.find('.//' + qn('w:numId'))
if h2_num is None: raise SystemExit('Style Heading 2 template tidak punya penomoran A., B., C.')
ABS_H2 = next(n for n in numbering.findall(qn('w:num'))
              if n.get(qn('w:numId')) == h2_num.get(qn('w:val'))).find(qn('w:abstractNumId')).get(qn('w:val'))
# Tingkat daftar: 1.  ->  a.  ->  1)  ->  a)   ; penanda tiap tingkat tepat di bawah teks tingkat atasnya
LEVELS = [('decimal', '%1.'), ('lowerLetter', '%2.'), ('decimal', '%3)'), ('lowerLetter', '%4)')]
def text_left(depth): return 720 + 360 * depth          # posisi teks item pada kedalaman depth
lv = ''.join(f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="{f}"/><w:lvlText w:val="{t}"/>'
             f'<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="{text_left(i)}" w:hanging="360"/></w:pPr></w:lvl>'
             for i, (f, t) in enumerate(LEVELS))
ABS_LIST = 900
numbering.find(qn('w:num')).addprevious(etree.fromstring(
    f'<w:abstractNum xmlns:w="{W}" w:abstractNumId="{ABS_LIST}"><w:multiLevelType w:val="multilevel"/>{lv}</w:abstractNum>'))
next_id = [max(int(n.get(qn('w:numId'))) for n in numbering.findall(qn('w:num'))) + 1]
def new_num(abs_id):
    nid = next_id[0]; next_id[0] += 1
    numbering.append(etree.fromstring(
        f'<w:num xmlns:w="{W}" w:numId="{nid}"><w:abstractNumId w:val="{abs_id}"/>'
        + ''.join(f'<w:lvlOverride w:ilvl="{l}"><w:startOverride w:val="1"/></w:lvlOverride>' for l in range(4))
        + '</w:num>'))
    return nid
def set_num(el, nid, lvl):
    ppr_del(el, 'w:numPr', 'w:ind')
    np_ = ppr_add(el, 'w:numPr')
    etree.SubElement(np_, qn('w:ilvl')).set(qn('w:val'), str(lvl))
    etree.SubElement(np_, qn('w:numId')).set(qn('w:val'), str(nid))

# ---------- penyusun paragraf ----------
out = []
CITE = re.compile(r'\[\d+(?:\s*[,-]\s*\d+)*\]')     # [1], [2, 3] = kutipan, bukan isian
def parts_of(s):
    """'[...]' (selain kutipan angka) di-highlight kuning: isian yang harus diisi mahasiswa."""
    return [(x, x.startswith('[') and x.endswith(']') and not CITE.fullmatch(x))
            for x in re.split(r'(\[[^\]]+\])', s) if x]
ZW = '​'   # titik potong tak terlihat
def breakable(s):
    """Kata yang disambung '/' (Programming/OOP) dianggap satu kata panjang -> baris rata kiri-kanan meregang.
    Beri titik potong setelah '/'. Nama ber-underscore TIDAK dipotong (daftar_ / peminjaman jelek); kalau barisnya
    meregang, ubah susunan kalimatnya (cek dengan check_stretch.py)."""
    return re.sub(r'/(?=\S)', '/' + ZW, s)

def para(protoel, s, bold=False):
    if 'http' not in s:
        s = breakable(s)
    el = copy.deepcopy(protoel)
    for txt, hl in parts_of(s):
        r = etree.SubElement(el, qn('w:r'))
        if hl or bold:
            rpr = etree.SubElement(r, qn('w:rPr'))
            if bold: etree.SubElement(rpr, qn('w:b'))
            if hl: etree.SubElement(rpr, qn('w:highlight')).set(qn('w:val'), 'yellow')
        t = etree.SubElement(r, qn('w:t')); t.text = txt; t.set(XS, 'preserve')
    out.append(el); return el
def h2(s, nid):
    el = para(P_H2, s); set_num(el, nid, 0)
    set_ind(el, left=360, hanging=360)   # huruf A. mentok kiri, teks heading di 360
def teks(s, left, first=True):
    """Paragraf isi. Kalimat pendek (label "File: ...", link) tanpa menjorok baris pertama."""
    el = para(P_BODY, s)
    if len(s) >= 100 and first: set_ind(el, left=left, firstLine=360)
    else: set_ind(el, left=left)
    if 'http' in s or s.startswith('[link'):   # URL panjang tak bisa dipotong: rata kiri, spasi tidak meregang
        set_jc(el, 'left')
    return el
def item(s, nid, lvl):
    el = para(P_LIST, s); set_num(el, nid, lvl)
    ppr_add(el, 'w:keepNext')            # label selalu satu halaman dengan isi di bawahnya
    set_jc(el, 'left')                   # butir pendek berisi nama_method: rata kiri agar tidak meregang
    return el

# ---------- gambar ----------
G = C.get('screenshot_geometry', {})
X0, CROP_W = G.get('x0', 430), G.get('crop_width', 1300)   # area maksimal; sisi kanan kosong dipangkas
MIN_W = G.get('min_width', 700)                             # potongan sempit tidak diperbesar berlebihan
HEAD_Y = G.get('code_header_y', (44, 110))                 # tab + breadcrumb editor
LINE1_Y, LINE_H = G.get('first_line_center', 120), G.get('line_height', 23.75)
PER_PAGE = G.get('lines_per_page', 36)                      # sama dengan -PerPage di shot.ps1
OUT_Y = G.get('out_y', (88, 993))
SPLIT_AT = C.get('split_code_lines', 19)
IMG_CM = C.get('image_width_cm', 10.0)
cnt = [0]

def is_bg(px): return max(px) < 48 and max(px) - min(px) < 12
def last_content_y(im, start=0):
    w, h = im.size; pix = im.load(); last = 0
    for y in range(start, h, 2):
        if last and y - last > 120: break       # jeda kosong panjang = konten selesai (abaikan tooltip)
        if any(not is_bg(pix[x, y]) for x in range(0, w, 2)): last = y
    return last

def stem_of(path):
    """modul1/nomor_2/2025XXXXX_dosen.py -> m1_nomor_2_dosen (sama dengan penamaan saat screenshot)."""
    parts = path.replace('\\', '/').split('/')
    base = re.sub(r'^\d+_', '', os.path.splitext(parts[-1])[0])
    return '_'.join([re.sub(r'^modul', 'm', parts[0])] + parts[1:-1] + [base])
def shots(path, kind):
    stem = stem_of(path)
    fs = sorted((f for f in os.listdir(SS) if re.fullmatch(re.escape(stem) + f'_{kind}(\\d+)\\.png', f)),
                key=lambda f: int(re.search(r'(\d+)\.png$', f).group(1)))
    if not fs: raise SystemExit(f'Screenshot {stem}_{kind}*.png tidak ada di {SS}')
    return [Image.open(os.path.join(SS, f)).convert('RGB') for f in fs]

def trim_right(im, skip_top=0):
    """Pangkas ruang kosong kanan (min MIN_W px): huruf tetap terbaca karena gambar selalu IMG_CM lebarnya."""
    w, h = im.size; pix = im.load()
    mx = max((x for y in range(skip_top, h, 2) for x in range(w - 1, 0, -2) if not is_bg(pix[x, y])), default=0)
    return im.crop((0, 0, min(w, max(mx + 40, MIN_W)), h))

def place(im, left, skip_top=0, trim=True):
    if trim: im = trim_right(im, skip_top)
    cnt[0] += 1
    p = os.path.join(TMP, f'img{cnt[0]:03d}.png'); im.save(p)
    if out and not has_img(out[-1]): ppr_add(out[-1], 'w:keepNext')   # label/teks pengantar ikut gambar
    el = copy.deepcopy(P_IMG); out.append(el)
    ppr_del(el, 'w:jc'); set_ind(el, left=left)
    run = P(el).add_run(); run.add_picture(p, width=Cm(IMG_CM))
    # garis tepi digambar separuh di luar gambar: tanpa ruang efek (0,5 pt tiap sisi) separuh garis atas/kanan
    # terpotong baris teks sehingga sisi itu tampak tipis/abu-abu
    ee = run._r.find('.//' + qn('wp:effectExtent'))
    if ee is None:   # python-docx tidak membuatnya; urutan skema: tepat sesudah wp:extent
        ee = etree.SubElement(run._r.find('.//' + qn('wp:inline')), qn('wp:effectExtent'))
        run._r.find('.//' + qn('wp:extent')).addnext(ee)
    for k in 'ltrb': ee.set(k, '6350')
    run._r.find('.//' + qn('pic:spPr')).append(etree.fromstring(    # border 1 pt "Black, Text 1" (tersorot di menu Word)
        '<a:ln xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="12700">'
        '<a:solidFill><a:schemeClr val="tx1"/></a:solidFill></a:ln>'))

def line_y(r): return LINE1_Y + r * LINE_H
def code_lines(path, a, b):
    """Potong baris a..b (1-based) dari screenshot halaman kode; lintas halaman disambung."""
    pages, pieces, n = shots(path, 'code'), [], a
    while n <= b:
        k = (n - 1) // PER_PAGE; top = k * PER_PAGE + 1
        end = min(b, top + PER_PAGE)               # satu halaman menampilkan PER_PAGE+1 baris
        y0, y1 = int(line_y(n - top) - LINE_H / 2), int(line_y(end - top) + LINE_H / 2)
        pieces.append(pages[k].crop((X0, y0, X0 + CROP_W, y1))); n = end + 1
    im = Image.new('RGB', (CROP_W, sum(p.size[1] for p in pieces)))
    y = 0
    for p in pieces: im.paste(p, (0, y)); y += p.size[1]
    return im

def resolve(path, spec, key):
    """dari/sampai: nomor baris (int) atau teks/regex baris pertama yang cocok."""
    v = spec.get(key)
    if v is None or isinstance(v, int): return v
    lines = open(os.path.join(KODE_DIR, path), encoding='utf-8').read().split('\n')
    start = (spec['_a'] if key == 'sampai' else 1)
    for i in range(start - 1, len(lines)):
        if re.search(v, lines[i]): return i + 1
    raise SystemExit(f'Pola {key}={v!r} tidak ditemukan di {path}')

def kode(spec, left):
    path = spec['kode']
    nlines = len(open(os.path.join(KODE_DIR, path), encoding='utf-8').read().rstrip('\n').split('\n'))
    a = resolve(path, spec, 'dari')
    if a is None:   # seluruh file: header tab ikut; file panjang dipecah jadi potongan seimbang ±SPLIT_AT baris
        pages = shots(path, 'code')
        head = pages[0].crop((X0, HEAD_Y[0], X0 + CROP_W, HEAD_Y[1]))
        parts = 1 if not SPLIT_AT or nlines <= SPLIT_AT + 6 else -(-nlines // SPLIT_AT)
        size = -(-nlines // parts)
        for s in range(1, nlines + 1, size):
            im = code_lines(path, s, min(nlines, s + size - 1))
            skip = 0
            if s == 1:
                full = Image.new('RGB', (CROP_W, head.size[1] + im.size[1]))
                full.paste(head, (0, 0)); full.paste(im, (0, head.size[1])); im = full
                skip = head.size[1]   # lebar diukur dari kode, bukan deretan tab
            place(im, left, skip)
        return
    spec['_a'] = a
    b = resolve(path, spec, 'sampai') or a
    place(code_lines(path, a, b), left)

def output(spec, left):
    for pg in shots(spec['output'], 'out'):
        im = pg.crop((X0, OUT_Y[0], X0 + CROP_W, OUT_Y[1]))
        place(im.crop((0, 0, CROP_W, min(im.size[1], last_content_y(im) + 16))), left)

def blocks(items, nid, depth):
    """Blok isi: item (bernomor, punya 'isi'), teks, kode, output. depth = kedalaman item berikutnya."""
    left = text_left(depth - 1) if depth > 0 else 360
    for b in items:
        if 'item' in b:
            item(b['item'], nid, depth)
            blocks(b.get('isi', []), nid, depth + 1)
        elif 'teks' in b:
            teks(b['teks'], left)
        elif 'kode' in b:
            kode(b, left)
        elif 'output' in b:
            output(b, left)
        elif 'gambar' in b:   # gambar utuh dari folder screenshot (mis. jendela GUI dari gui_shot.py)
            # daftar nama = disusun berdampingan dalam satu gambar 10 cm (jendela kecil/dialog tidak jadi raksasa)
            names = b['gambar'] if isinstance(b['gambar'], list) else [b['gambar']]
            ims = [Image.open(os.path.join(SS, n)).convert('RGB') for n in names]
            gap = 24
            im = Image.new('RGB', (sum(i.size[0] for i in ims) + gap * (len(ims) - 1), max(i.size[1] for i in ims)), 'white')
            x = 0
            for i in ims: im.paste(i, (x, 0)); x += i.size[0] + gap
            place(im, left, trim=False)
        else:
            raise SystemExit(f'Blok tidak dikenal: {b}')

# ---------- isi modul ----------
ID = C['identitas']
for mi, m in enumerate(C['modul']):
    if mi: out.append(copy.deepcopy(P_PB))
    para(P_H1, m['judul'])
    hn = new_num(ABS_H2)
    h2('Tujuan', hn)
    n = new_num(ABS_LIST)
    for t in m['tujuan']: item(t, n, 0)
    h2('Alat dan Bahan', hn)
    n = new_num(ABS_LIST)
    for t in m.get('alat', C['alat']): item(t, n, 0)
    h2('Landasan Teori', hn)
    n = new_num(ABS_LIST)
    for sub in m['teori']:
        item(sub['judul'], n, 0)
        for t in sub['paragraf']: teks(t, text_left(0))
    h2('Kegiatan Praktikum', hn)
    teks(C['kegiatan'].format(judul=m['judul'], mata_kuliah=ID['mata_kuliah'], **m.get('kegiatan_isi', {})), 360)
    blocks(m['praktik'], new_num(ABS_LIST), 0)
    if m.get('tugas'):
        h2('Tugas', hn)
        if m['tugas'].get('pengantar'): teks(m['tugas']['pengantar'], 360, first=False)
        blocks(m['tugas']['isi'], new_num(ABS_LIST), 0)
out.append(copy.deepcopy(P_PB))

# ---------- ganti isi lama ----------
dp = els[I_DP]
for el in out: dp.addprevious(el)
for el in els[I_MOD:I_DP]: body.remove(el)
for el in els[I_DP + 1:]:
    if el.tag != qn('w:sectPr'): body.remove(el)   # bibliografi lama (field CITATION) dibuang
last = dp
APA = C.get('gaya_pustaka', 'apa') == 'apa'
for i, r in enumerate(C['referensi'], 1):
    # rata kiri-kanan (Ctrl+J) + menggantung 1,27 cm (Ctrl+T). APA: tanpa nomor, urut abjad (diurutkan di content).
    # *teks* = miring (judul buku / nama jurnal & volume). DOI/URL diberi titik potong agar baris tidak meregang.
    el = copy.deepcopy(P_BODY); set_ind(el, left=720, hanging=720); set_jc(el, 'both')
    s = r if APA else f'[{i}]\t{r}'
    for k, chunk in enumerate(re.split(r'\*([^*]+)\*', s)):
        if not chunk: continue
        rr = etree.SubElement(el, qn('w:r'))
        if k % 2: etree.SubElement(etree.SubElement(rr, qn('w:rPr')), qn('w:i'))
        t = etree.SubElement(rr, qn('w:t')); t.text = re.sub(r'([/.])(?=\w)', r'\1' + ZW, chunk) if 'http' in chunk or 'doi' in chunk else breakable(chunk)
        t.set(XS, 'preserve')
    last.addnext(el); last = el

# ---------- sampul, kata pengantar, lembar asistensi ----------
def set_text(el, s):
    runs = el.findall(qn('w:r'))
    for x in runs[1:] + el.findall(qn('w:hyperlink')): el.remove(x)
    r = runs[0]
    for c in list(r):
        if c.tag != qn('w:rPr'): r.remove(c)
    t = etree.SubElement(r, qn('w:t')); t.text = s; t.set(XS, 'preserve')

set_text(els[I_MATKUL], ID['mata_kuliah'])
set_text(els[I_NAMA], ID['nama'])
set_text(els[I_NIM], f"NIM : {ID['nim']}")
set_text(els[I_KP_TXT], C['kata_pengantar'])
set_text(els[I_DATE], ID['kota_tanggal'])
set_text(els[I_SIGN_NAME], ID['nama'])
for r in els[I_SIGN].findall(qn('w:r')): els[I_SIGN].remove(r)   # tanda tangan pemilik template
for i in (I_DATE, I_SIGN_NAME):   # tanggal & nama rata tengah seperti baris tanda tangan
    old = els[i].find(qn('w:pPr'))
    if old is not None: els[i].remove(old)
    sp = els[I_SIGN].find(qn('w:pPr'))
    if sp is not None: els[i].insert(0, copy.deepcopy(sp))
for i in range(I_KP + 1, I_KP_TXT):   # baris kosong di bawah judul KATA PENGANTAR
    if not text(els[i]) and not has_img(els[i]) and not has_sect(els[i]): body.remove(els[i])
if I_ASIS_IMG is not None:   # kartu kendali pemilik template -> penanda kuning
    e = els[I_ASIS_IMG]
    for r in e.findall(qn('w:r')): e.remove(r)
    r = etree.SubElement(e, qn('w:r'))
    etree.SubElement(etree.SubElement(r, qn('w:rPr')), qn('w:highlight')).set(qn('w:val'), 'yellow')
    t = etree.SubElement(r, qn('w:t')); t.text = '[Tempel foto kartu kendali praktikum di sini]'

# ---------- sembunyikan garis merah/biru cek ejaan & tata bahasa Word di seluruh dokumen ----------
st = d.settings.element
for tag in ('w:hideGrammaticalErrors', 'w:hideSpellingErrors'):
    if st.find(qn(tag)) is None:
        st.insert(0, etree.Element(qn(tag)))   # urutan skema: elemen ini berada di awal w:settings

# ---------- buang gambar yatim & metadata ----------
used = set(re.findall(r'r:(?:embed|id|link)="([^"]+)"', etree.tostring(d.element).decode()))
for rid, rel in list(d.part.rels.items()):
    if rel.reltype.endswith('/image') and rid not in used: del d.part.rels[rid]
d.core_properties.author = ID['nama']
d.core_properties.last_modified_by = ID['nama']
d.core_properties.title = f"Laporan Praktikum {ID['mata_kuliah']}"
d.save(OUT)
print('saved', OUT, 'gambar', cnt[0])
