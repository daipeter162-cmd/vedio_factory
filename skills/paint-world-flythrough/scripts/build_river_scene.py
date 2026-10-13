"""A real 3D river-night blueprint, not automatic reconstruction of any painting.
Blender 4.0+: blender -b -t 4 --python build_river_scene.py -- --source painting.png
  --atlas paint_atlas.png --output scene.blend --preview-dir qa --width 1280
New sides and geographic layout are authored approximations. Images are packed.
"""
import argparse, math, random, sys
from pathlib import Path
import bpy
from mathutils import Vector

args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser()
p.add_argument('--source',required=True)
p.add_argument('--atlas',required=True)
p.add_argument('--output',required=True)
p.add_argument('--preview-dir')
p.add_argument('--width',type=int,default=1280)
a=p.parse_args(args)
random.seed(41)
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'
s.eevee.taa_render_samples=8
s.eevee.use_soft_shadows=False
s.eevee.use_gtao=True
s.eevee.gtao_distance=3
s.eevee.gtao_factor=1.15
s.eevee.use_bloom=True
s.eevee.bloom_intensity=.10
s.eevee.bloom_threshold=1.4
s.render.resolution_x=a.width
s.render.resolution_y=round(a.width*9/16)
s.render.resolution_percentage=100
s.render.fps=30
s.frame_start=1
s.frame_end=540
s.render.image_settings.file_format='PNG'
s.render.film_transparent=False
s.view_settings.view_transform='Standard'
s.view_settings.look='Medium High Contrast'
s.view_settings.exposure=0
s.view_settings.gamma=1
s.world=bpy.data.worlds.new('Blue night ambient')
s.world.use_nodes=True
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.11,.17,.23,1)
s.world.node_tree.nodes['Background'].inputs[1].default_value=.65
atlas=bpy.data.images.load(str(Path(a.atlas).resolve()))
original=bpy.data.images.load(str(Path(a.source).resolve()))

def solid(name,color,energy=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
 bs.inputs['Roughness'].default_value=.9
 bs.inputs['Emission Color'].default_value=(*color,1)
 bs.inputs['Emission Strength'].default_value=energy
 return m

def paint(name,tile,scale=1,emission=.3):
 m=solid(name,(.2,.3,.3));n=m.node_tree.nodes;l=m.node_tree.links;bs=n.get('Principled BSDF')
 uv=n.new('ShaderNodeTexCoord')
 mul=n.new('ShaderNodeVectorMath');mul.operation='SCALE';mul.inputs[3].default_value=scale
 half=n.new('ShaderNodeVectorMath');half.operation='SCALE';half.inputs[3].default_value=.5
 frac=n.new('ShaderNodeVectorMath');frac.operation='FRACTION'
 double=n.new('ShaderNodeVectorMath');double.operation='SCALE';double.inputs[3].default_value=2
 sub=n.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=(1,1,1)
 ab=n.new('ShaderNodeVectorMath');ab.operation='ABSOLUTE'
 inv=n.new('ShaderNodeVectorMath');inv.operation='SUBTRACT';inv.inputs[0].default_value=(1,1,1)
 shrink=n.new('ShaderNodeVectorMath');shrink.operation='SCALE';shrink.inputs[3].default_value=.475
 add=n.new('ShaderNodeVectorMath');add.operation='ADD'
 offsets=[(.012,.512,0),(.512,.512,0),(.012,.012,0),(.512,.012,0)]
 add.inputs[1].default_value=offsets[tile]
 tex=n.new('ShaderNodeTexImage');tex.image=atlas;tex.interpolation='Linear'
 for out,inp in [(uv.outputs['UV'],mul.inputs[0]),(mul.outputs[0],half.inputs[0]),(half.outputs[0],frac.inputs[0]),(frac.outputs[0],double.inputs[0]),(double.outputs[0],sub.inputs[0]),(sub.outputs[0],ab.inputs[0]),(ab.outputs[0],inv.inputs[1]),(inv.outputs[0],shrink.inputs[0]),(shrink.outputs[0],add.inputs[0]),(add.outputs[0],tex.inputs[0]),(tex.outputs['Color'],bs.inputs['Base Color']),(tex.outputs['Color'],bs.inputs['Emission Color'])]:l.new(out,inp)
 bs.inputs['Emission Strength'].default_value=emission
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.25;bump.inputs['Distance'].default_value=.04
 l.new(tex.outputs['Color'],bump.inputs['Height']);l.new(bump.outputs[0],bs.inputs['Normal'])
 return m

water=paint('River • impasto blue',0,1,.50)
wood=paint('Boat • dark painted wood',1,1,.28)
bank=paint('Shore • ochre olive paint',2,1,.35)
wall=paint('City • slate painted walls',3,.7,.40)
roof=paint('Roofs • dark painted wood',1,.65,.25)
yellow=solid('Golden lamp paint',(.72,.55,.20),1.8)
dark=solid('Dark brush outlines',(.022,.038,.034),.15)
stroke_mats=[solid('Wave brush %02d'%i,c,.65) for i,c in enumerate([(.08,.15,.17),(.09,.20,.23),(.15,.27,.29),(.23,.31,.29),(.36,.38,.23),(.50,.49,.22),(.68,.58,.24),(.83,.68,.29)])]

def mesh(name,verts,faces,material,uvscale=1):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(name,me);s.collection.objects.link(o)
 if material:me.materials.append(material)
 layer=me.uv_layers.new(name='Paint UV')
 for poly in me.polygons:
  axis=max(range(3),key=lambda k:abs(poly.normal[k]))
  axes=[i for i in range(3) if i!=axis]
  for li in poly.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co
   layer.data[li].uv=(v[axes[0]]*uvscale,v[axes[1]]*uvscale)
 return o

def box(name,pos,size,mat,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.name=name;o.scale=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(mat)
 if bevel:
  mod=o.modifiers.new('Soft painted edge','BEVEL');mod.width=bevel;mod.segments=2
  o.data.use_auto_smooth=True
  o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o

def line(name,points,radius,mat):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=1
 sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for v,co in zip(sp.points,points):v.co=(*co,1)
 ob=bpy.data.objects.new(name,cu);s.collection.objects.link(ob);ob.data.materials.append(mat);return ob

# Spatial layout: near shore y<0, boats near y=0, river, far city y=52.
mesh('River surface',[(-120,-80,0),(120,-80,0),(120,150,0),(-120,150,0)],[(0,1,2,3)],water,.14)
shore_verts=[(-65,-65,.11),(65,-65,.11),(50,-7,.11),(19,-2,.11),(7,1,.11),(3,-1,.11),(-3,-6,.11),(-24,-12,.11),(-65,-9,.11)]
mesh('Near riverbank',shore_verts,[tuple(range(len(shore_verts)))],bank,.18)
line('Riverbank painted lip',[(-65,-9,.19),(-24,-12,.19),(-3,-6,.19),(3,-1,.19),(7,1,.19),(19,-2,.19),(50,-7,.19)],.075,wood)
mesh('Distant quay',[(-100,49,.25),(100,49,.25),(100,72,.25),(-100,72,.25)],[(0,1,2,3)],bank,.1)
box('Far stone embankment',(0,49,.5),(160,.6,.65),wall)

# Foreground boats are complete hulls with sides, transoms, decks, seats and rigging.
def boat(name,x,y,angle,length=5.1,width=1.35,mastheight=5.6):
 root=bpy.data.objects.new(name,None);s.collection.objects.link(root);root.location=(x,y,.06);root.rotation_euler.z=angle
 outline=[(0,-length/2),(.37*width,-.32*length),(.5*width,.10*length),(.40*width,.38*length),(0,length/2),(-.40*width,.38*length),(-.5*width,.10*length),(-.37*width,-.32*length)]
 verts=[(u*.67,v*.92,.15) for u,v in outline]+[(u,v,.64) for u,v in outline]
 faces=[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]+[tuple(range(8))]
 objects=[]
 objects.append(mesh(name+' hull',verts,faces,wood,1.2))
 objects.append(mesh(name+' inside deck',[(u*.80,v*.94,.48) for u,v in outline],[tuple(range(8))],bank,.75))
 objects.append(line(name+' rim',[(u,v,.65) for u,v in outline]+[(outline[0][0],outline[0][1],.65)],.04,bank))
 for yy in [-1.3,-.3,.8,1.5]:objects.append(box(name+' cross seat',(0,yy,.69),(width*.73,.18,.10),wood,.02))
 objects.append(line(name+' mast',[(0,.20,.50),(0,.20,mastheight)],.052,wood))
 objects.append(line(name+' ochre mast stroke',[(.026,.17,.8),(.026,.17,mastheight-.1)],.012,bank))
 for pt in [(-width*.40,-length*.35,.63),(width*.40,-length*.35,.63),(0,length*.40,.65)]:objects.append(line(name+' stay',[pt,(0,.20,mastheight-.2)],.010,dark))
 objects.append(line(name+' furled sail',[(0,.2,mastheight-.2),(.22,.21,mastheight*.55),(.18,.25,1.0)],.085,wall))
 for side in [-1,1]:objects.append(line(name+' hull brush rail',[(side*u,v,.37) for u,v in [(width*.23,-length*.35),(width*.38,0),(width*.27,length*.32)]],.022,bank))
 for o in objects:o.parent=root
 return root

boat('L1 main moored boat',-1,0,math.radians(-20))
boat('L2 secondary boat',-4.2,1.2,math.radians(-37),4.5,1.15,3.9)
line('Mooring rope',[(-.5,-1.6,.7),(2,-2,.17),(3,-1,.17)],.018,bank)

# City buildings have side faces; position variation prevents a flat postcard strip.
for i in range(63):
 x=-75+i*2.4;y=52+random.uniform(0,6);w=random.uniform(1.7,3.0);h=random.uniform(1.7,4.2);d=random.uniform(2.4,5)
 box('L3 city house %02d'%i,(x,y,h/2+.35),(w,d,h),wall,.07)
 vs=[(-w/2,-d/2,0),(w/2,-d/2,0),(-w/2,d/2,0),(w/2,d/2,0),(0,-d/2,.9),(0,d/2,.9)]
 ro=mesh('Roof %02d'%i,vs,[(0,1,4),(2,5,3),(0,4,5,2),(1,3,5,4)],roof,.6);ro.location=(x,y,h+.35)
 for row in range(max(1,int(h/1.1))):
  for col in range(2):
   if random.random()<.65:box('Warm window',(x+(col-.5)*w*.40,y-d/2-.02,.85+row*1.05),(.22,.035,.39),yellow)
 if i%3==0:box('Quayside gas lamp',(x,48.55,1.4),(.09,.09,2.7),dark);box('Lamp flame',(x,48.55,2.9),(.25,.25,.30),yellow,.03)

# Tall landmark on the left, inspired by the source skyline rather than exact architecture.
box('L4 distant clock tower',(-40,53,4.7),(2.7,3.4,8.8),wall,.08)
for x in [-41,-39]:box('Tower dark slit',(x,51.27,6.9),(.23,.04,1),dark)
bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=2.1,radius2=0,depth=3.6,location=(-40,53,10.7),rotation=(0,0,math.pi/4));bpy.context.object.name='Tower painted spire';bpy.context.object.data.materials.append(roof)

# Brush ribbons lie in 3D on the water; perspectives and occlusion change with the camera.
verts=[];faces=[];indices=[]
def ribbon(x,y,length,width,angle,mi,z=.022):
 start=len(verts)
 ux,uy=math.cos(angle),math.sin(angle);vx,vy=-uy,ux
 for k in range(5):
  t=k/4;center=(t-.5)*length;wig=.07*math.sin(t*math.pi*2+0.7)
  half=width*(.55+.45*math.sin(math.pi*t))/2
  for sign in [-1,1]:verts.append((x+ux*center+vx*(wig+sign*half),y+uy*center+vy*(wig+sign*half),z+.005*math.sin(t*math.pi)))
 for k in range(4):faces.append((start+k*2,start+k*2+1,start+k*2+3,start+k*2+2));indices.append(mi)

for i in range(8500):
 x=random.uniform(-85,85);y=random.uniform(-22,60)
 ribbon(x,y,random.uniform(.22,1.2),random.uniform(.025,.10),random.uniform(-.13,.13),random.choices(range(5),weights=[5,5,4,2,1])[0])
for j,xx in enumerate([-55,-42,-29,-18,-7,5,17,29,41,55,67]):
 for k in range(180):
  y=random.uniform(-16,48);x=xx+1.7*math.sin(y*.12+j)+random.gauss(0,1.1)
  ribbon(x,y,random.uniform(.12,.70),random.uniform(.035,.16),random.uniform(-.2,.2),random.choice([4,5,6,7]),.039)
waves=mesh('L5 river brush marks and golden reflections',verts,faces,None,.1)
for m in stroke_mats:waves.data.materials.append(m)
for poly,mi in zip(waves.data.polygons,indices):poly.material_index=mi
waves.location.z=0;waves.keyframe_insert('location',frame=1)
waves.location.z=.015;waves.keyframe_insert('location',frame=270)
waves.location.z=0;waves.keyframe_insert('location',frame=540)
for m in stroke_mats[4:]:
 bs=m.node_tree.nodes.get('Principled BSDF');drv=bs.inputs['Emission Strength'].driver_add('default_value').driver;drv.expression='0.7+0.10*sin(frame/23)'

# Sky is an immense curved world backdrop, with UV sampling only the source sky.
skyverts=[];skyfaces=[];N=144
for i in range(N+1):
 ang=math.radians(-180+360*i/N)
 for z in [-3,122]:skyverts.append((180*math.sin(ang),180*math.cos(ang),z))
for i in range(N):skyfaces.append((i*2,i*2+1,i*2+3,i*2+2))
sky=mesh('L6 painted starry sky cylinder',skyverts,skyfaces,None)
skymat=bpy.data.materials.new('Original sky • world anchored');skymat.use_nodes=True;n=skymat.node_tree.nodes;n.clear();l=skymat.node_tree.links
tex=n.new('ShaderNodeTexImage');tex.image=original;tex.extension='EXTEND'
em=n.new('ShaderNodeEmission');em.inputs[1].default_value=.78;out=n.new('ShaderNodeOutputMaterial');l.new(tex.outputs['Color'],em.inputs[0]);l.new(em.outputs[0],out.inputs[0]);sky.data.materials.append(skymat)
for poly in sky.data.polygons:
 for li in poly.loop_indices:
  vi=sky.data.loops[li].vertex_index;ang=-180+360*(vi//2)/N
  u=(ang+100)/200 if abs(ang)<=100 else (.5*(-100-ang)/80 if ang<-100 else 1-.5*(ang-100)/80)
  sky.data.uv_layers.active.data[li].uv=(u,.670+(vi%2)*.330)

# Two people on shore are spatial figures, not a cutout from the painting.
for j,(x,y) in enumerate([(5.8,-5.3),(6.6,-5.2)]):
 coat=wood if j==0 else bank
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.15,location=(x,y,1.67));head=bpy.context.object;head.name='L7 shore figure head';head.data.materials.append(bank)
 bpy.ops.mesh.primitive_cone_add(vertices=10,radius1=.30,radius2=.16,depth=.95,location=(x,y,.99));bpy.context.object.data.materials.append(coat)
 for dx in [-.10,.10]:line('Figure leg',[(x+dx,y,.60),(x+dx*.9,y-.03,.17)],.075,wood)
 line('Figure shoulder',[(x-.25,y,1.30),(x+.25,y,1.30)],.10,coat)
box('Foreground shore mooring bollard',(3.0,-1.0,.36),(.24,.24,.5),wood,.04)

def area(name,pos,power,color,size):
 data=bpy.data.lights.new(name,'AREA');data.energy=power;data.color=color;data.shape='DISK';data.size=size
 ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(Vector((0,0,0))-ob.location).to_track_quat('-Z','Y').to_euler()
area('Soft blue night fill',(-10,-10,25),2100,(.40,.64,.85),25)
area('Warm reflected shore light',(7,-5,9),650,(1,.83,.48),14)

bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Continuous flythrough camera';s.camera=cam;cam.data.lens=29;cam.data.clip_end=500
controls=[(0,(5,-12,1.8),(-1,1,2.1)),(3.5,(3.6,-5.2,2.0),(-1,1,2.2)),(6.5,(3.4,1.5,2.8),(-1,0,2.1)),(9.5,(-4.8,3.5,4.3),(-1,0,1.9)),(13,(-8,-8,7.8),(-1,17,3.5)),(18,(5,-26,13),(0,27,7.5))]
def sample(sec,column):
 idx=next((i for i in range(len(controls)-1) if sec<=controls[i+1][0]),len(controls)-2)
 t=(sec-controls[idx][0])/(controls[idx+1][0]-controls[idx][0]);t=max(0,min(1,t))
 p0=Vector(controls[max(0,idx-1)][column]);p1=Vector(controls[idx][column]);p2=Vector(controls[idx+1][column]);p3=Vector(controls[min(len(controls)-1,idx+2)][column])
 return .5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)
for fr in range(1,541):
 sec=(fr-1)/30;cam.location=sample(sec,1);target=sample(sec,2);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 cam.keyframe_insert('location',frame=fr);cam.keyframe_insert('rotation_euler',frame=fr)
for curve in cam.animation_data.action.fcurves:
 for kp in curve.keyframe_points:kp.interpolation='LINEAR'
s['route']='Real 3D reconstruction; unobserved geometry is an authored approximation.'
s['landmarks']='L1 main boat; L2 second boat; L3 city; L4 left tower; L5 reflections; L6 source sky; L7 couple.'
bpy.ops.file.pack_all()
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.output).resolve()))
if a.preview_dir:
 outdir=Path(a.preview_dir);outdir.mkdir(parents=True,exist_ok=True)
 for fr in [1,106,196,286,391,540]:
  s.frame_set(fr);s.render.filepath=str(outdir/f'{fr:04d}.png');bpy.ops.render.render(write_still=True)
print('SCENE_READY',len(s.objects),'objects',flush=True)
