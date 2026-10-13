"""Report executables and libraries without reading credentials."""
import argparse,importlib.util,json,shutil,platform,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--blender-wrapper',default=os.environ.get('PAINT_WORLD_BLENDER'))
a=p.parse_args();wrapper=str(Path(a.blender_wrapper).resolve()) if a.blender_wrapper and Path(a.blender_wrapper).is_file() else None
print(json.dumps({'platform':platform.system(),'executables':{x:shutil.which(x) for x in ['blender','ffmpeg','ffprobe','apt-get','node']},'portable_blender_wrapper':wrapper,'python':{x:bool(importlib.util.find_spec(x)) for x in ['numpy','PIL','bpy']}},ensure_ascii=False,indent=2))
