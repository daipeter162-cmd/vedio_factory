import React from 'react';
import {AbsoluteFill,Composition,Sequence,useVideoConfig,staticFile} from 'remotion';
import {Audio,Video} from '@remotion/media';
import {ArtworkCard} from './ArtworkCard';
const FullFilm:React.FC=()=>{const {fps}=useVideoConfig();return <AbsoluteFill style={{background:'#102529'}}>
 <Sequence durationInFrames={22*fps} premountFor={fps} name="完整三维穿行"><Video src={staticFile('full-flythrough.mp4')} muted style={{width:'100%',height:'100%'}}/></Sequence>
 <Sequence from={22*fps} durationInFrames={8*fps} premountFor={fps} name="原图和梵高创作简介"><AbsoluteFill><div style={{position:'absolute',width:1280,height:720,transform:'scale(1.5)',transformOrigin:'0 0'}}><ArtworkCard/></div></AbsoluteFill></Sequence>
 <Audio src={staticFile('ambience.m4a')}/>
 </AbsoluteFill>;};
const Card:React.FC=()=> <AbsoluteFill><div style={{position:'absolute',width:1280,height:720,transform:'scale(1.5)',transformOrigin:'0 0'}}><ArtworkCard/></div></AbsoluteFill>;
export const Root:React.FC=()=> <><Composition id="RhoneComplete" component={FullFilm} durationInFrames={900} fps={30} width={1920} height={1080}/><Composition id="ArtworkCard" component={Card} durationInFrames={240} fps={30} width={1920} height={1080}/></>;
