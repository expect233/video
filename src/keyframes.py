import argparse, pathlib, cv2
from utils import ensure_dir

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", help="影片檔")
    ap.add_argument("--out", required=True, help="輸出資料夾（將存 JPG）")
    ap.add_argument("--step", type=int, default=12, help="抽幀間隔（每 N 幀檢查一次）")
    ap.add_argument("--threshold", type=float, default=28.0, help="畫面差異門檻（越小越敏感）")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out)
    ensure_dir(out_dir)

    cap = cv2.VideoCapture(args.video)
    last = None
    idx = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % args.step != 0:
            idx += 1
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        if last is None:
            last = gray
            cv2.imwrite((out_dir / f"{idx:06d}.jpg").as_posix(), frame)
            saved += 1
        else:
            diff = cv2.absdiff(gray, last)
            score = diff.mean()
            if score > args.threshold:
                cv2.imwrite((out_dir / f"{idx:06d}.jpg").as_posix(), frame)
                last = gray
                saved += 1
        idx += 1
    cap.release()
    print(f"Saved keyframes: {saved} -> {out_dir}")

if __name__ == "__main__":
    main()
