"""Extract timestamped reference frames without altering the source video."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('video', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--times', default='0,3,6,9,12,15,18')
    a = p.parse_args()
    src = a.video.resolve(strict=True)
    out = a.output.resolve()
    if out == src or src in out.parents:
        p.error('Output must be a separate directory')
    if out.exists() and any(out.iterdir()):
        p.error('Output directory must be empty; use a new directory')
    for exe in ('ffprobe', 'ffmpeg'):
        if not shutil.which(exe):
            p.error(f'{exe} must be available on PATH')
    raw = subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(src)])
    meta = json.loads(raw)
    duration = float(meta['format']['duration'])
    try:
        times = [float(x.strip()) for x in a.times.split(',')]
    except ValueError:
        p.error('Times must be comma-separated numbers')
    if not times or any(t < 0 or t >= duration for t in times):
        p.error('Each requested time must be within the video duration')
    out.mkdir(parents=True, exist_ok=True)
    frames = []
    for i, t in enumerate(times):
        name = f'frame_{i:03d}_{t:.3f}s.jpg'
        target = out / name
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', str(t), '-i', str(src), '-frames:v', '1', '-q:v', '2', str(target)], check=True)
        if not target.is_file() or target.stat().st_size == 0:
            raise RuntimeError(f'No decoded frame at {t} seconds')
        frames.append({'requested_time_seconds': t, 'filename': name})
    index = {'source_name': src.name, 'duration_seconds': duration, 'streams': meta['streams'], 'frames': frames, 'time_note': 'Requested source seek times, rounded to frame-grid precision; no scene-boundary inference.'}
    (out / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'duration_seconds': duration, 'frame_count': len(frames), 'output': str(out)}, ensure_ascii=False))


if __name__ == '__main__':
    main()

