import argparse, pathlib, srt, datetime
from utils import ensure_dir, run
from faster_whisper import WhisperModel

def write_srt(segments, out_path):
    subs = []
    idx = 1
    for seg in segments:
        start = datetime.timedelta(seconds=seg.start)
        end = datetime.timedelta(seconds=seg.end)
        text = seg.text.strip()
        subs.append(srt.Subtitle(index=idx, start=start, end=end, content=text))
        idx += 1
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", help="影片路徑（本機）")
    ap.add_argument("--out", required=True, help="輸出 SRT 路徑，例如 outputs/<slug>/transcript.srt")
    ap.add_argument("--model", default="small", help="Whisper model size")
    ap.add_argument("--lang", default="auto", help="語言代碼，如 zh/en/jp，或 auto")
    args = ap.parse_args()

    out_path = pathlib.Path(args.out)
    ensure_dir(out_path.parent)

    tmp_wav = out_path.parent / "audio_16k.wav"
    run(["ffmpeg","-y","-i", args.video, "-ac","1","-ar","16000", tmp_wav.as_posix()])

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    language = None if args.lang == "auto" else args.lang
    segments, info = model.transcribe(tmp_wav.as_posix(), language=language, vad_filter=True)

    write_srt(segments, out_path.as_posix())

if __name__ == "__main__":
    main()
