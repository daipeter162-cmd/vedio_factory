"""Copy the tested river-specific template into a fresh project. Does not generate assets."""
from pathlib import Path
import argparse,shutil,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--source',type=Path);p.add_argument('--materials',type=Path);a=p.parse_args()
 out=a.output.resolve()
 if out.exists():p.error('Output already exists; choose a fresh directory to preserve previous work.')
 names=['facades.png','surfaces.png','boat-planks.png','painted-sky.png','painted-surface.png','foliage.png']
 if a.materials:
  missing=[n for n in names if not (a.materials/n).is_file()]
  if missing:p.error('Missing materials: '+', '.join(missing))
  with Image.open(a.materials/'foliage.png') as im:
   if im.mode!='RGBA' or im.getextrema()[-1][0]!=0:p.error('foliage.png needs a genuine transparent alpha background.')
 if a.source and not a.source.is_file():p.error('Source image does not exist.')
 shutil.copytree(ROOT/'assets/webgl-river',out)
 if a.source:
  with Image.open(a.source) as im:im.convert('RGB').save(out/'remotion/public/source.png')
 if a.materials:
  for n in names:shutil.copy2(a.materials/n,out/'assets'/n)
 report={'project':str(out),'template':'river-specific authored reconstruction','missing_inputs':([n for n in names if not (out/'assets'/n).exists()]+([] if a.source else ['remotion/public/source.png'])),'next':'Verify/replace artwork biography and adapt geometry before rendering.'}
 (out/'project-inputs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
