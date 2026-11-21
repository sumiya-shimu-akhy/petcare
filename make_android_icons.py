import os
from PIL import Image, ImageDraw

BASE = os.path.join('android', 'app', 'src', 'main', 'res')
SIZES = {'mipmap-mdpi': 48, 'mipmap-hdpi': 72, 'mipmap-xhdpi': 96,
         'mipmap-xxhdpi': 144, 'mipmap-xxxhdpi': 192}


def draw_icon(size):
    img = Image.new('RGB', (size, size), '#4f46e5')
    d = ImageDraw.Draw(img)
    pad = 0.12
    s = size * (1 - 2 * pad)
    o = size * pad

    def box(cx, cy, rx, ry):
        return (o + (cx - rx) * s, o + (cy - ry) * s, o + (cx + rx) * s, o + (cy + ry) * s)

    d.ellipse(box(0.5, 0.64, 0.24, 0.19), fill='white')
    for cx, cy in [(0.22, 0.42), (0.40, 0.25), (0.60, 0.25), (0.78, 0.42)]:
        d.ellipse(box(cx, cy, 0.09, 0.12), fill='white')
    return img


for folder, size in SIZES.items():
    out = os.path.join(BASE, folder)
    os.makedirs(out, exist_ok=True)
    draw_icon(size).save(os.path.join(out, 'ic_launcher.png'))
print('Android icons created')