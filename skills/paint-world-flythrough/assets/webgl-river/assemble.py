from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;F=P/'frames';movie=P/'rhone_complete_30s.mp4';body=P/'remotion/public/full-flythrough.mp4'
assert {p.name for p in F.glob('*.jpg')}=={f'{i:04d}.jpg' for i in range(660)}
def ff(args):
 out=Path(args[-1]);tmp=out.with_name(out.stem+'.encoding'+out.suffix)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-y',*args[:-1],str(tmp)],check=True)
 tmp.replace(out)
ff(['-framerate','30','-start_number','0','-i',str(F/'%04d.jpg'),'-frames:v','660','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(body)])
ff(['-i',str(body),'-i',str(P/'artwork-card-1080.mp4'),'-i',str(P/'remotion/public/ambience.m4a'),'-filter_complex_threads','2','-filter_complex','[0:v]setsar=1[v0];[1:v]setsar=1[v1];[v0][v1]concat=n=2:v=1:a=0[v]','-map','[v]','-map','2:a:0','-t','30','-frames:v','900','-r','30','-c:v','libx264','-crf','18','-preset','medium','-c:a','copy','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)])
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]));v=next(x for x in meta['streams'] if x['codec_type']=='video');a=next(x for x in meta['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',900)
assert abs(float(v['duration'])-30)<.04 and abs(float(a['duration'])-30)<.08
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
for p in F.glob('*.jpg'):
 with Image.open(p) as im:assert im.size==(1920,1080);im.verify()
qa=P/'final-qa';qa.mkdir(exist_ok=True);times=[0,3.5,6.3,9.3,12,14.8,17.4,21.95,22.1,23.9,26,29.5];sheet=Image.new('RGB',(1280,615),'#102529');draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 p=qa/f'{i:02d}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(movie),'-frames:v','1','-update','1',str(p)],check=True)
 with Image.open(p) as im:sheet.paste(im.resize((320,180)),((i%4)*320,(i//4)*205))
 draw.text(((i%4)*320+10,(i//4)*205+185),f'{t}s',fill='#f1e8cf')
sheet.save(qa/'contact.jpg',quality=95)
results={'file':movie.name,'duration_seconds':30,'width':1920,'height':1080,'fps':30,'frames':900,'native_3d_frames':660,'native_3d_seconds':22,'artist_card_seconds':8,'interpolation':False,'video_upscale':False,'full_decode':'passed','source_frames':'all 660 JPEGs passed','audio_duration_seconds':float(a['duration']),'inspection_times':times}
(P/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False),flush=True)
