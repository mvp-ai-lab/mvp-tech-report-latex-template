# Builds a vector "MVP Lab" wordmark: glyph outlines (from a Ghostscript-outlined PDF of plain black text) used as a
# clipping path, filled with an axial shading blue -> indigo -> pink. Standard path clipping, no text render modes.
import re, sys, zlib
src, out = sys.argv[1], sys.argv[2]
d = open(src, 'rb').read()
w, h = [float(x) for x in re.search(rb'/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]', d).groups()]
content = None
for m in re.finditer(rb'stream\r?\n(.*?)endstream', d, re.S):
    s = m.group(1)
    if b' m\n' in s:
        content = s.decode('latin-1')
assert content
lines = content.strip().split('\n')
assert lines[0].endswith(' cm'), lines[0]
cm = lines[0][2:]                      # "0.1 0 0 0.1 0 0 cm"
scale = float(cm.split()[0])
path = [l for l in lines[1:] if re.search(r' [mlc]$|^h$', l)]
ops = set(l.split()[-1] for l in lines[1:]) - {'m', 'l', 'c', 'h'}
assert ops <= {'g', 'i', 'f', 'Q'}, ops   # only color, flatness, fills, restore besides the path itself
blue, indigo, pink = [[int(c[i:i+2], 16) / 255 for i in (0, 2, 4)] for c in ('4361EE', '3F37C9', 'F72585')]
fmt = lambda v: ' '.join('%.4f' % x for x in v)
stream = ('q %s\n%s\nW n\n/Sh0 sh\nQ\n' % (cm, '\n'.join(path))).encode()
# Shading coordinates are in the scaled (cm) space: from x=0 to x=w/scale.
objs = [
    b'<< /Type /Catalog /Pages 2 0 R >>',
    b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    ('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.4f %.4f] /Resources << /Shading << /Sh0 5 0 R >> >> '
     '/Contents 4 0 R >>' % (w, h)).encode(),
    None,
    ('<< /ShadingType 2 /ColorSpace /DeviceRGB /Coords [0 0 %.4f 0] /Extend [true true] /Function '
     '<< /FunctionType 3 /Domain [0 1] /Bounds [0.5] /Encode [0 1 0 1] /Functions ['
     '<< /FunctionType 2 /Domain [0 1] /C0 [%s] /C1 [%s] /N 1 >> '
     '<< /FunctionType 2 /Domain [0 1] /C0 [%s] /C1 [%s] /N 1 >>] >> >>'
     % (w / scale, fmt(blue), fmt(indigo), fmt(indigo), fmt(pink))).encode(),
]
z = zlib.compress(stream, 9)
objs[3] = b'<< /Length %d /Filter /FlateDecode >>\nstream\n' % len(z) + z + b'\nendstream'
pdf = bytearray(b'%PDF-1.5\n%\xe2\xe3\xcf\xd3\n')
offs = []
for i, o in enumerate(objs, 1):
    offs.append(len(pdf)); pdf += b'%d 0 obj\n' % i + o + b'\nendobj\n'
x = len(pdf)
pdf += b'xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1) + b''.join(b'%010d 00000 n \n' % o for o in offs)
pdf += b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, x)
open(out, 'wb').write(pdf)
print('wrote', out, '%.3f x %.3f pt' % (w, h), len(pdf), 'bytes')
