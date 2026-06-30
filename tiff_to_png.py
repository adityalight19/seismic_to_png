from pathlib import Path
from PIL import Image, ImageSequence
import numpy as np

tiff_path = Path(r"E:\_desk\kg_bsr\test2.tiff")

output_dir = tiff_path.parent / f"{tiff_path.stem}_exported_png"
output_dir.mkdir(exist_ok=True)

with Image.open(tiff_path) as img:
    total_frames = getattr(img, "n_frames", 1)

    print("Input file:", tiff_path)
    print("Output folder:", output_dir)
    print("Mode:", img.mode)
    print("Size:", img.size)
    print("Frames:", total_frames)

    for i, frame in enumerate(ImageSequence.Iterator(img), start=1):
        arr = np.array(frame)

        if arr.ndim == 3:
            out_img = Image.fromarray(arr)
        else:

            if arr.dtype == np.uint16:
                out_img = Image.fromarray(arr, mode="I;16")
            else:

                arr = arr.astype(np.float32)

                low, high = np.percentile(arr, [0.5, 99.5])

                if high > low:
                    arr = (arr - low) / (high - low)
                else:
                    arr = arr * 0

                arr = np.clip(arr, 0, 1)
                arr_16 = (arr * 65535).astype(np.uint16)
                out_img = Image.fromarray(arr_16, mode="I;16")

        png_path = output_dir / f"{tiff_path.stem}_frame_{i:04d}.png"
        out_img.save(png_path, "PNG")

        print(f"Saved {i}/{total_frames}: {png_path}")