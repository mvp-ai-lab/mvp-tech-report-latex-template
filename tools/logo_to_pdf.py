"""Converts the MVP Lab logo (tools/mvplab_logo.svg, an SVG of filled circles) into a vector PDF with a transparent
background:  python3 tools/logo_to_pdf.py tools/mvplab_logo.svg template/mvplab_logo.pdf
Only <circle cx cy r fill [fill-opacity]> elements are supported, which is all the logo uses."""
import re
import sys
import zlib

src, out = sys.argv[1], sys.argv[2]
svg = open(src, encoding='utf-8').read()
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
x0, y0, w, h = vb
k = 0.5522847498  # Bezier control-point factor of a quarter circle

shapes = re.findall(r'<(\w+)([^>]*)/?>', svg)
others = {t for t, _ in shapes} - {'svg', 'circle'}
if others:
    sys.exit('unsupported SVG elements: %s' % ', '.join(sorted(others)))

gstates, ops = {}, []
for tag, attrs in shapes:
    if tag != 'circle':
        continue
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', attrs))
    cx, cy, r = float(a['cx']) - x0, h - (float(a['cy']) - y0), float(a['r'])  # PDF y axis points up
    col = a['fill'].lstrip('#')
    rgb = ' '.join('%.4f' % (int(col[i:i + 2], 16) / 255) for i in (0, 2, 4))
    op = a.get('fill-opacity')
    if op is not None and float(op) < 1:
        name = gstates.setdefault(op, 'GS%d' % len(gstates))
        ops.append('q /%s gs' % name)
    c = k * r
    ops.append('%s rg %.3f %.3f m %.3f %.3f %.3f %.3f %.3f %.3f c %.3f %.3f %.3f %.3f %.3f %.3f c '
               '%.3f %.3f %.3f %.3f %.3f %.3f c %.3f %.3f %.3f %.3f %.3f %.3f c f' % (
                   rgb, cx + r, cy,
                   cx + r, cy + c, cx + c, cy + r, cx, cy + r,
                   cx - c, cy + r, cx - r, cy + c, cx - r, cy,
                   cx - r, cy - c, cx - c, cy - r, cx, cy - r,
                   cx + c, cy - r, cx + r, cy - c, cx + r, cy))
    if op is not None and float(op) < 1:
        ops.append('Q')

stream = zlib.compress('\n'.join(ops).encode(), 9)
gs = ' '.join('/%s << /Type /ExtGState /ca %s >>' % (n, o) for o, n in gstates.items())
objs = [
    b'<< /Type /Catalog /Pages 2 0 R >>',
    b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    ('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %g %g] /Resources << /ExtGState << %s >> >> '
     '/Contents 4 0 R >>' % (w, h, gs)).encode(),
    b'<< /Length %d /Filter /FlateDecode >>\nstream\n' % len(stream) + stream + b'\nendstream',
]
pdf = bytearray(b'%PDF-1.5\n%\xe2\xe3\xcf\xd3\n')
offsets = []
for i, o in enumerate(objs, 1):
    offsets.append(len(pdf))
    pdf += b'%d 0 obj\n' % i + o + b'\nendobj\n'
xref = len(pdf)
pdf += b'xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1)
pdf += b''.join(b'%010d 00000 n \n' % o for o in offsets)
pdf += b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, xref)
open(out, 'wb').write(pdf)
print('wrote %s: %g x %g pt, %d circles, %d bytes' % (out, w, h, sum(t == 'circle' for t, _ in shapes), len(pdf)))
