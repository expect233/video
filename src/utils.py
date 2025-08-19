import os, re, json, subprocess, pathlib, hashlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]

def slugify(path: str) -> str:
    name = pathlib.Path(path).stem
    name = re.sub(r'[^a-zA-Z0-9\-_]+', '-', name).strip('-').lower()
    if not name:
        name = hashlib.md5(path.encode('utf-8')).hexdigest()[:8]
    return name

def ensure_dir(p: pathlib.Path):
    p.mkdir(parents=True, exist_ok=True)

def run(cmd: list):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)

def ffprobe_duration(path: str) -> float | None:
    try:
        out = subprocess.check_output([
            "ffprobe","-v","error","-select_streams","v:0","-show_entries",
            "format=duration","-of","json", path
        ]).decode()
        j = json.loads(out)
        return float(j.get("format",{}).get("duration",0.0))
    except Exception:
        return None

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
