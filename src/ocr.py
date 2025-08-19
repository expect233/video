import argparse, pathlib, pytesseract
from PIL import Image
from utils import ensure_dir

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyframes_dir", help="keyframes 資料夾")
    ap.add_argument("--out", required=True, help="輸出 ocr 文字資料夾")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out)
    ensure_dir(out_dir)

    kdir = pathlib.Path(args.keyframes_dir)
    imgs = sorted([p for p in kdir.iterdir() if p.suffix.lower() in [".jpg",".png",".jpeg"]])
    for p in imgs:
        txt = pytesseract.image_to_string(Image.open(p), lang="chi_tra+eng")
        (out_dir / (p.stem + ".txt")).write_text(txt, encoding="utf-8")
    print(f"OCR done -> {out_dir}")

if __name__ == "__main__":
    main()
