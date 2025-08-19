# video-insight-pipeline

> **目的**：把影片處理成可分析的**文字與截圖**輸出，方便在 ChatGPT 這邊讀取檔案後，幫你做**摘要、時間軸、HackMD 講義**等高階分析。  
> **輸出**：`outputs/<slug>/` 內包含：`transcript.srt`、`keyframes/*.jpg`、`ocr/*.txt`、`summary.json`、`notes.md`。

## 快速開始（本機）
1. 安裝系統工具：`ffmpeg`、`tesseract-ocr`  
   - macOS：`brew install ffmpeg tesseract`
   - Ubuntu：`sudo apt-get update && sudo apt-get install -y ffmpeg tesseract-ocr`
2. Python 3.10+ & 依賴：
   ```bash
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. 放一支影片於 `videos/`（建議用 Git LFS；或僅在本機放檔），執行：
   ```bash
   python src/transcribe.py videos/lecture.mp4 --model small --lang zh --out outputs/lecture/transcript.srt
   python src/keyframes.py videos/lecture.mp4 --out outputs/lecture/keyframes
   python src/ocr.py outputs/lecture/keyframes --out outputs/lecture/ocr
   python src/summarize.py outputs/lecture --out outputs/lecture
   ```

## GitHub Actions（雲端自動化）
專案已附 `.github/workflows/process-video.yml`：
- 觸發方式：
  - **workflow_dispatch**：手動輸入 `video_path`（repo 內路徑，如 `videos/lecture.mp4`）。
  - **push**：當 `videos/**` 有變更時自動跑。
- Runner 會：安裝 `ffmpeg`、`tesseract` → 安裝 Python 依賴 → 執行四個步驟 → **把 `outputs/` commit 回 repo**。

> **建議**：影片體積大請用 **Git LFS** 或放雲端，只把**輸出**回寫到 repo。

## 產出檔案說明
- `transcript.srt`：Whisper 逐字稿（含時間碼）。
- `keyframes/*.jpg`：關鍵畫面截圖（內容變化大處）。
- `ocr/*.txt`：每張截圖的文字辨識結果（Tesseract）。
- `summary.json`：關鍵詞、章節摘要（rule-based，之後可替換你自訂的 summarizer）。
- `notes.md`：HackMD 友善筆記（可直接貼到 HackMD）。

## 自訂
- Whisper 模型用 `--model` 指定（`tiny`、`base`、`small`、`medium`、`large-v3`）。CPU 環境建議 `small`。
- 想改 keyframe 靈敏度，調 `--threshold`（0~255 差異強度）。
- 想接你自己的 LLM/總結服務，編輯 `src/summarize.py` 裡的 `build_summary()`。

## 結果交付給 ChatGPT
完成後，把 `outputs/<slug>/`（特別是 `transcript.srt`、`summary.json`、`notes.md`、`keyframes/`）提供給我，我就能在這裡把它**升級**成高品質講義與分析。
