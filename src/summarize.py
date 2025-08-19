import argparse, pathlib, json, re, srt, jieba, collections
from utils import ensure_dir, now_iso

def load_srt(srt_path):
    with open(srt_path, encoding="utf-8") as f:
        subs = list(srt.parse(f.read()))
    return subs

def top_keywords(text, k=20):
    words = [w for w in jieba.cut(text) if re.match(r"[\u4e00-\u9fa5a-zA-Z0-9]{2,}", w)]
    cnt = collections.Counter(words)
    return [w for w,_ in cnt.most_common(k)]

def build_summary(out_dir: pathlib.Path):
    srt_path = out_dir / "transcript.srt"
    subs = load_srt(srt_path)
    full_text = " ".join([s.content for s in subs])

    chapters = []
    sec_per_ch = 300
    chap = {"start": 0, "end": 0, "bullets": []}
    acc = []
    for s in subs:
        t = int(s.start.total_seconds())
        if t // sec_per_ch != chap["end"] // sec_per_ch and acc:
            chap["end"] = t
            chap["bullets"] = acc[:5]
            chapters.append(chap)
            chap = {"start": t, "end": t, "bullets": []}
            acc = []
        acc.append(s.content[:50])
        chap["end"] = int(s.end.total_seconds())
    if acc:
        chap["bullets"] = acc[:5]
        chapters.append(chap)

    kw = top_keywords(full_text, 20)

    summary = {
        "generated_at": now_iso(),
        "keywords": kw,
        "chapters": chapters[:12],
    }
    return summary

def write_notes(out_dir: pathlib.Path, summary: dict):
    srt_rel = "transcript.srt"
    keyword_lines = "\n- ".join(summary['keywords'][:7])
    header = "# 影片講義筆記（自動草稿）\n\n"
    meta = "> 產出時間：" + summary['generated_at'] + "\n\n[TOC]\n\n"
    notes = header + meta + "## 速讀重點（自動產生）\n- " + keyword_lines + "\n\n## 章節時間軸（每 ~5 分鐘）\n"
    for i, ch in enumerate(summary["chapters"], 1):
        def mmss(s): return f"{s//60:02d}:{s%60:02d}"
        notes += f"\n### ⏱ {mmss(ch['start'])} – {mmss(ch['end'])}\n"
        for b in ch["bullets"]:
            notes += f"- {b}\n"
    notes += (\
        "\n---\n\n" +\
        "## 逐字稿（SRT）\n> ./" + srt_rel + "\n\n" +\
        "## 關鍵畫面\n> ./keyframes/ 內 JPG 檔案（可挑 5–10 張插入）\n\n" +\
        "## OCR（畫面文字）\n> ./ocr/ 內每張圖片的 .txt\n\n" +\
        "---\n\n" +\
        "## 後續建議\n- 手動挑選 5–10 張關鍵截圖，插入到對應章節下。\n- 若要更精準的摘要，可替換 src/summarize.py 的 build_summary() 實作。\n"\
    )
    (out_dir / "notes.md").write_text(notes, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_root", help="包含 transcript.srt 的資料夾")
    ap.add_argument("--out", help="輸出資料夾（預設同 out_root）")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out or args.out_root)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = build_summary(out_dir)
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_notes(out_dir, summary)
    print("Summary & notes ->", out_dir)

if __name__ == "__main__":
    main()
