"""Verify technical output; visual art and geography still require manual inspection."""
from pathlib import Path
import argparse,json,subprocess
from fractions import Fraction
from PIL import Image
def main():
 p=argparse.ArgumentParser();p.add_argument('video',type=Path);p.add_argument('--duration',type=float,required=True);p.add_argument('--width',type=int,required=True);p.add_argument('--height',type=int,required=True);p.add_argument('--fps',type=int,default=30);p.add_argument('--source-dir',type=Path);p.add_argument('--source-frames',type=int);p.add_argument('--report',type=Path);a=p.parse_args()
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(a.video)]))
 v=next(x for x in meta['streams'] if x['codec_type']=='video');audio=[x for x in meta['streams'] if x['codec_type']=='audio']
 assert (v['width'],v['height'])==(a.width,a.height),'Resolution mismatch'
 assert Fraction(v['avg_frame_rate'])==a.fps,'Frame rate mismatch'
 expected=round(a.duration*a.fps);assert int(v['nb_read_frames'])==expected,'Frame count mismatch'
 assert abs(float(v['duration'])-a.duration)<1/a.fps+.01,'Video duration mismatch'
 assert audio and abs(float(audio[0]['duration'])-a.duration)<.10,'Audio absent or duration mismatch'
 subprocess.run(['ffmpeg','-v','error','-i',str(a.video),'-f','null','-'],check=True)
 if a.source_dir:
  frames=sorted(a.source_dir.glob('*.jpg'))
  if a.source_frames is not None:assert len(frames)==a.source_frames,'Source frame count mismatch'
  for f in frames:
   with Image.open(f) as im:assert im.size==(a.width,a.height);im.verify()
 result={'file':a.video.name,'duration':a.duration,'width':a.width,'height':a.height,'fps':a.fps,'frames':expected,'audio_duration':float(audio[0]['duration']),'full_decode':'passed','visual_review':'required separately'}
 if a.report:a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
