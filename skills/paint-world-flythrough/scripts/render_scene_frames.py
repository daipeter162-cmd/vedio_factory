"""Run inside Blender with a loaded .blend; render a resumable frame range.
blender -b scene.blend --python render_scene_frames.py -- --directory frames
  --start 1 --end 540 --step 1 --width 960 --samples 4
Each output filename retains its ORIGINAL scene frame (30fps blueprint).
"""
import argparse,sys,time
from pathlib import Path
import bpy
p=argparse.ArgumentParser();p.add_argument('--directory',required=True)
p.add_argument('--start',type=int,default=1);p.add_argument('--end',type=int,default=540)
p.add_argument('--step',type=int,default=1);p.add_argument('--width',type=int,default=960)
p.add_argument('--samples',type=int,default=4)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);s=bpy.context.scene
if a.step<1 or a.start>a.end:raise ValueError('Invalid frame range')
s.render.resolution_x=a.width;s.render.resolution_y=round(a.width*9/16)
s.render.resolution_percentage=100;s.eevee.taa_render_samples=a.samples
s.render.image_settings.file_format='PNG';s.render.image_settings.compression=15
root=Path(a.directory).resolve();root.mkdir(parents=True,exist_ok=True)
total=len(range(a.start,a.end+1,a.step));t=time.time()
for idx,frame in enumerate(range(a.start,a.end+1,a.step),1):
 path=root/f'{frame:04d}.png'
 if not path.exists():
  s.frame_set(frame);s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
 if idx%10==0 or idx==total:print(f'PROGRESS {idx}/{total} scene_frame={frame} elapsed={time.time()-t:.1f}',flush=True)
print('RENDER_COMPLETE',flush=True)
