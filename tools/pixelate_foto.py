#!/usr/bin/env python3
"""
Ubah foto wajah jadi potret pixel art untuk popup profil Fairy Quest.

Butuh: Python 3 + Pillow  ->  pip install pillow

Contoh:
  python pixelate_foto.py foto_teman1.jpg --name friend1
  python pixelate_foto.py foto_teman2.jpg --name friend2 --grid 40 --colors 12
  python pixelate_foto.py foto_teman3.jpg --name friend3 --crop 120,60,400,400
  python pixelate_foto.py foto.jpg --name friend1 --zoom 1.3 --shift-y -0.15

Hasil: folder "hasil_pixel/portrait_<name>_<ukuran>.png" (kotak, tanpa transparansi)
"""
import argparse, os, sys
from PIL import Image, ImageEnhance, ImageOps


def square_crop(im, zoom=1.0, shift_x=0.0, shift_y=0.0, box=None):
    w, h = im.size
    if box:
        x, y, cw, ch = box
        s = min(cw, ch)
        return im.crop((x, y, x + s, y + s))
    side = min(w, h) / max(zoom, 1.0)
    cx = w / 2 + shift_x * (w - side) / 2
    cy = h / 2 + shift_y * (h - side) / 2          # shift-y negatif = geser ke atas
    x0 = min(max(cx - side / 2, 0), w - side)
    y0 = min(max(cy - side / 2, 0), h - side)
    return im.crop((int(x0), int(y0), int(x0 + side), int(y0 + side)))


def pixelate(path, out_dir, name, grid, size, colors, zoom, sx, sy, box, contrast, saturation):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = square_crop(im, zoom, sx, sy, box)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(saturation)
    small = im.resize((grid, grid), Image.BOX)                       # rata-rata per blok
    small = small.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    scale = max(1, size // grid)
    out = small.resize((grid * scale, grid * scale), Image.NEAREST)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"portrait_{name}_{out.width}.png")
    out.save(out_path)
    return out_path, small.size, out.size


def main():
    ap = argparse.ArgumentParser(description="Foto wajah -> potret pixel art")
    ap.add_argument("foto", help="path foto (jpg/png)")
    ap.add_argument("--name", default=None, help="nama file hasil, mis. friend1 (default: nama foto)")
    ap.add_argument("--out", default="hasil_pixel", help="folder hasil")
    ap.add_argument("--grid", type=int, default=32, help="jumlah 'kotak' pixel per sisi (kecil = lebih kasar). default 32")
    ap.add_argument("--size", type=int, default=64, help="ukuran gambar akhir (px), kelipatan --grid. default 64 (pas untuk bingkai 76px)")
    ap.add_argument("--colors", type=int, default=16, help="jumlah warna palet. default 16")
    ap.add_argument("--zoom", type=float, default=1.0, help="perbesar area wajah (>=1). default 1.0")
    ap.add_argument("--shift-x", type=float, default=0.0, help="geser crop, -1 (kiri) .. 1 (kanan)")
    ap.add_argument("--shift-y", type=float, default=-0.1, help="geser crop, -1 (atas) .. 1 (bawah). default -0.1")
    ap.add_argument("--crop", default=None, help="crop manual 'x,y,lebar,tinggi' (piksel foto asli)")
    ap.add_argument("--contrast", type=float, default=1.1)
    ap.add_argument("--saturation", type=float, default=1.15)
    a = ap.parse_args()

    if not os.path.isfile(a.foto):
        sys.exit(f"File tidak ditemukan: {a.foto}")
    name = a.name or os.path.splitext(os.path.basename(a.foto))[0]
    box = tuple(int(v) for v in a.crop.split(",")) if a.crop else None
    p, g, s = pixelate(a.foto, a.out, name, a.grid, a.size, a.colors, a.zoom, a.shift_x, a.shift_y, box, a.contrast, a.saturation)
    print(f"OK -> {p}  (grid {g[0]}x{g[1]}, ukuran akhir {s[0]}x{s[1]})")


if __name__ == "__main__":
    main()
