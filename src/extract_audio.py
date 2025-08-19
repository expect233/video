import argparse, pathlib
from utils import ensure_dir, run

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", help="影片路徑（本機）")
    ap.add_argument("--out_wav", default="tmp/audio.wav", help="輸出的 WAV 檔")
    ap.add_argument("--sr", type=int, default=16000, help="取樣率")
    args = ap.parse_args()

    out = pathlib.Path(args.out_wav)
    ensure_dir(out.parent)
    run(["ffmpeg","-y","-i", args.video, "-ac","1","-ar",str(args.sr), out.as_posix()])

if __name__ == "__main__":
    main()
