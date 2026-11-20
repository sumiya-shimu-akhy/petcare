import os
from PIL import Image, ImageDraw

OUT = os.path.join('accounts', 'static', 'accounts', 'icons')
os.makedirs(OUT, exist_ok=True)


def draw_icon(size, padding):
    img = Image.new('RGB', (size, size), '#4f46e5')
    d = ImageDraw.Draw(img)
    s = size * (1 - 2 * padding)
    o = size * padding

    def box(cx, cy, rx, ry):
        return (o + (cx - rx) * s, o + (cy - ry) * s, o + (cx + rx) * s, o + (cy + ry) * s)

    d.ellipse(box(0.5, 0.64, 0.24, 0.19), fill='white')
    for cx, cy in [(0.22, 0.42), (0.40, 0.25), (0.60, 0.25), (0.78, 0.42)]:
        d.ellipse(box(cx, cy, 0.09, 0.12), fill='white')
    return img


draw_icon(192, 0.08).save(os.path.join(OUT, 'icon-192.png'))
draw_icon(512, 0.08).save(os.path.join(OUT, 'icon-512.png'))
draw_icon(512, 0.22).save(os.path.join(OUT, 'icon-maskable-512.png'))
print('Icons created in', OUT)