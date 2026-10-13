import React, {useEffect, useState} from 'react';
import {AbsoluteFill, CanvasImage, Composition, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio, Video} from '@remotion/media';

const useFonts = () => {
  const [handle] = useState(() => delayRender('Load Chinese fonts'));
  useEffect(() => {
    Promise.all([
      new FontFace('GallerySerif', `url(${staticFile('serif-cn.otf')})`).load(),
      new FontFace('GallerySans', `url(${staticFile('sans-cn.otf')})`).load(),
    ]).then((fonts) => {
      fonts.forEach((font) => document.fonts.add(font));
      continueRender(handle);
    });
  }, [handle]);
};

export const ArtworkCard: React.FC = () => {
  useFonts();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: '#102529', color: '#f1e8cf', fontFamily: 'GallerySans', overflow: 'hidden'}}>
      <CanvasImage src={staticFile('source.png')} premountFor={fps} style={{position:'absolute',left:42,top:55,width:838,height:600,objectFit:'contain'}} />
      <div style={{position:'absolute',left:900,top:68,width:1,height:574,backgroundColor:'#d7bb70',opacity:0.28}} />
      <div style={{position:'absolute',left:924,top:78,width:309,opacity:interpolate(frame,[0,0.8*fps],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),translate:interpolate(frame,[0,0.8*fps],['0px 12px','0px 0px'],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>
        <div style={{fontSize:14,letterSpacing:2,color:'#d7bb70'}}>VINCENT VAN GOGH</div>
        <div style={{fontFamily:'GallerySerif',fontSize:39,lineHeight:1.45,marginTop:10}}>文森特·梵高</div>
        <div style={{fontSize:21,color:'#c1c9bf',marginTop:8}}>1853—1890 · 荷兰画家</div>
      </div>
      <div style={{position:'absolute',left:924,top:229,width:309,height:1,backgroundColor:'#d7bb70',opacity:0.42}} />
      <div style={{position:'absolute',left:924,top:252,width:309,opacity:interpolate(frame,[0.35*fps,1.15*fps],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>
        <div style={{fontFamily:'GallerySerif',fontSize:34,lineHeight:1.45}}>罗讷河上的星夜</div>
        <div style={{fontSize:21,color:'#d7bb70',marginTop:14}}>1888年9月 · 法国阿尔勒</div>
      </div>
      <div style={{position:'absolute',left:924,top:361,width:309,fontSize:24,lineHeight:1.8,color:'#e4ddc9',opacity:interpolate(frame,[0.75*fps,1.55*fps],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>
        他在阿尔勒描绘夜晚的罗讷河，以深蓝天空与金色灯光倒影，表现夜色的宁静。
      </div>
      <div style={{position:'absolute',left:924,top:598,width:309,color:'#c1c9bf',fontSize:20,lineHeight:1.7,opacity:interpolate(frame,[1.1*fps,1.8*fps],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>
        <div>布面油画</div><div>巴黎奥赛博物馆藏</div>
      </div>
      <div style={{position:'absolute',left:42,bottom:26,fontSize:16,letterSpacing:1.7,color:'#c1c9bf'}}>STARRY NIGHT OVER THE RHÔNE · 1888</div>
      <div style={{position:'absolute',left:924,bottom:26,fontSize:16,color:'#c1c9bf'}}>资料来源：奥赛博物馆</div>
    </AbsoluteFill>
  );
};

export const RhoneFilm: React.FC = () => {
  const {fps} = useVideoConfig();
  return <AbsoluteFill style={{backgroundColor:'#102529'}}>
    <Sequence durationInFrames={18*fps} premountFor={fps} name="三维穿行">
      <Video src={staticFile('flythrough.mp4')} muted premountFor={fps} style={{width:'100%',height:'100%'}} />
    </Sequence>
    <Sequence from={18*fps} durationInFrames={8*fps} premountFor={fps} name="原画与创作简介"><ArtworkCard /></Sequence>
    <Audio src={staticFile('ambience.m4a')} premountFor={fps} />
  </AbsoluteFill>;
};

export const GalleryCompositions: React.FC = () => <>
  <Composition id="RhoneFilm" component={RhoneFilm} durationInFrames={780} fps={30} width={1280} height={720} />
  <Composition id="ArtworkCard" component={ArtworkCard} durationInFrames={240} fps={30} width={1280} height={720} />
</>;
