#!/usr/bin/env python3
# Cut5 video splitter - cuts video into 5s segments
# Requires ffmpeg installed and in PATH

import argparse, subprocess
from pathlib import Path

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr

def slice_video(inp, out_dir, secs):
    inp = Path(inp)
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)
    ext = inp.suffix or ".mp4"
    template = str(out_dir / f"part_%04d{ext}")

    cmd = ["ffmpeg","-y","-i",str(inp),"-c","copy","-map","0","-f","segment",
           "-segment_time",str(secs),"-reset_timestamps","1",template]
    rc,out = run(cmd)
    if rc==0: return True

    template = str(out_dir / "part_%04d.mp4")
    cmd = ["ffmpeg","-y","-i",str(inp),
           "-c:v","libx264","-preset","fast","-crf","23",
           "-c:a","aac","-b:a","128k",
           "-map","0","-f","segment","-segment_time",str(secs),
           "-reset_timestamps","1",template]
    rc,out = run(cmd)
    return rc==0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", default="output_parts")
    ap.add_argument("--seconds","-s", type=int, default=5)
    args=ap.parse_args()
    ok = slice_video(args.input, args.out, args.seconds)
    print("Done" if ok else "Error")

if __name__=="__main__":
    main()
