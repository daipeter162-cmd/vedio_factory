# Three.js + Remotion 完整制作路线

## 使用条件与边界

使用浏览器渲染器来快速输出真实三维相机运动；使用Remotion编辑原图简介与后期。主场景也可继续使用Blender。两个框架不需要叠加才能补足美术，先完成几何与绘画表面。

`assets/webgl-river/` 是《罗讷河上的星夜》个案模板，原生1920×1080、30fps，默认22秒穿行+8秒作者卡。它包含实体河岸、两船、城市、教堂、码头建筑、树木和人物。其他画作必须替换场景、材质、相机与简介；不是通用单图三维恢复器，也不是参考作者工程。

## 初始化与素材

```bash
python scripts/init_webgl_project.py project --source painting.png --materials materials
cd project
npm ci
```

`materials` 中提供6个PNG：`facades.png`（四格正交立面）、`surfaces.png`（屋顶/石岸/地面/树皮）、`boat-planks.png`、`painted-sky.png`、`painted-surface.png`（河面底层）、`foliage.png`（真实透明Alpha枝叶）。原画转换为项目用PNG，源文件不改动。模板自带许可允许的字体与授权文本。

先读`art-direction.md`并根据当前原画生成材质。输入列表由`project-inputs.json`记录。缺素材时列出待生成项，不拿原画切层代替实体，也不调用未授权的付费模型。

## 模板改造

- 在`scene.mjs`修改地标、各面绘画贴图、根部承托与底部`controls`相机曲线。固定随机种子是可复现布局，不是图生视频身份保证。
- 原画与作者文本在`remotion/public/source.png`和`remotion/src/ArtworkCard.tsx`；核实画名、作者、年代、地点与馆藏，替换河岸案例事实。
- 默认总时长30秒已在场景、渲染、组片和Remotion注册中一致设置。改变时长或帧率时同步所有端点、帧数与音轨，不只改一个变量。

## 浏览器与试渲

提供系统Chrome路径：`PAINT_CHROME=/path/to/chrome`。渲染器也检查常见系统路径和项目Remotion下载的Chrome。无需读取登录账号或复用浏览器会话。

```bash
npm run qa
node render.mjs --start 0 --end 659 --width 1920
```

先看8个QA视角，再出片。默认使用SwiftShader软件WebGL以保持可复现；实际耗时先实测。不把用户电脑GPU规格当作当前云环境GPU性能。

`server.mjs`与Chromium在同一渲染进程范围启动，避免隔离环境的localhost跨进程不可达。并行任务只允许使用不重叠的帧区间、同一源版本与规格；受端口约束时串行执行。

## 必须保留的工程检查

- WebGL的`Shader Error`、`WebGLProgram`与`VALIDATE_STATUS`错误必须停止输出。MP4能解码不代表Shader正确，空河面仍是失败。
- 将传入GLSL的浮点常量显式序列化为`30.0`或`0.0`，不要生成`float + int`。水面与反光笔触统一世界坐标相位，计入几何位置偏移。
- 缓存指纹绑定场景、素材、依赖锁、渲染脚本、尺寸与固定帧数。代码、素材或规格改变时使用新的空`frames`目录。没有指纹的旧帧不能续渲；指纹不能代替实际画面验收。
- 导出先写临时MP4，编码成功再原子替换目标。发现`moov atom not found`时重导并完整验证，不能交付半写入文件。

## 后期与交付

在`remotion`安装依赖并导出作者卡；需要本机接口兼容时使用已有`loopback-env.cjs`，普通系统无需启用。

```bash
cd remotion
npm ci
npx remotion render ArtworkCard ../artwork-card-1080.mp4 --crf=18
cd ..
python make_audio.py
ffmpeg -y -i ambience.wav -c:a aac -b:a 192k remotion/public/ambience.m4a
python assemble.py
```

最终检查示例：

```bash
python scripts/verify_output.py project/rhone_complete_30s.mp4 --duration 30 --width 1920 --height 1080 --fps 30 --source-dir project/frames --source-frames 660 --report project/verification.json
```

交付完整MP4、可编辑场景/后期工程、实际材质与提示词、原生规格和验收记录。视频与大体积素材按单次制作保存；工作流仓库保存技能、代码、模板和说明。
