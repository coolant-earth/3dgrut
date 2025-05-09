#!/usr/bin/env python3
"""
fast_downscale.py

python fast_downscale.py /workspace/GreenTrees/Plot123/images 2
"""

import sys, os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor as TPE
from functools import partial
from PIL import Image, ImageOps
from tqdm import tqdm
import multiprocessing as mp

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}

def _downscale_one(dst_dir: Path, factor: int, img_path: Path) -> None:
    with Image.open(img_path) as im:
        im = ImageOps.exif_transpose(im)           # honour orientation
        w, h = im.size
        im_ds = im.resize((w // factor, h // factor), Image.Resampling.LANCZOS)
        im_ds.save(dst_dir / img_path.name, quality=95, subsampling=0)

def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("Usage: fast_downscale.py <image_folder> <factor:int>")
    src = Path(sys.argv[1]).expanduser().resolve()
    if not src.is_dir():
        sys.exit(f"❌  {src} is not a directory")
    factor = int(sys.argv[2])
    if factor < 1:
        sys.exit("❌  factor must be ≥1")

    if factor == 1:
        print("Factor is 1; nothing to do."); return

    dst = src.parent / f"{src.name}_{factor}"
    dst.mkdir(exist_ok=True)

    images = [p for p in src.iterdir() if p.suffix.lower() in IMAGE_EXTS]
    if not images:
        sys.exit("❌  No supported images found")

    worker = partial(_downscale_one, dst, factor)
    n_threads = min(len(images), mp.cpu_count() * 2)   # I/O + CPU mix

    with TPE(max_workers=n_threads) as pool:
        list(tqdm(pool.map(worker, images),
                  total=len(images),
                  desc=f"Resizing x{factor} → {dst.name}",
                  unit="img"))

    print(f"✅  Done. {len(images)} images written to {dst}")

if __name__ == "__main__":
    main()