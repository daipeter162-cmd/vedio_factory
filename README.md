# 短视频自动化工厂

可复用的视频制作技能与实际制作脚本。

## 名画沉浸式穿行

[paint-world-flythrough](skills/paint-world-flythrough/) 将绘画转成沉浸式穿行视频。区分参考观察、制作推断与复现设计，不声称恢复作者原提示词。

工作流：参考抽帧 → 能力检查与工具准备 → 三维或AI路线 → 固定地标 → 实体与绘画材质 → 连续相机路径 → 试渲与成片验收 → 原画收尾。

- 实体三维优先实现新侧面、绕行和遮挡；2.5D只作用户接受的预演。
- 含环境检查、隔离安装Blender、河岸场景蓝图、续渲和参考抽帧脚本。
- 河岸蓝图已在Blender 4.0.2实际渲染。它不是通用单图三维恢复器；其他作品需重建相应几何。
- 技能安装不提供外部视频模型权限，也不要求使用付费生成服务。

## 安装与调用

下载整个 `skills/paint-world-flythrough/` 目录到 Codex 技能目录，通常是 `~/.codex/skills/paint-world-flythrough/`。保持脚本和参考资料相对路径，重新加载技能后调用：

```text
用 $paint-world-flythrough 把这幅画制作成20秒的沉浸式穿行视频。
镜头要绕过主体看到侧面，再切回原画；缺工具自行准备。
```

## 本地三维制作

需Python、FFmpeg/FFprobe和经过单帧验证的Blender。Debian/Ubuntu可用便携安装脚本；安装权限和网络遵循运行环境。

```bash
python skills/paint-world-flythrough/scripts/check_capabilities.py
bash skills/paint-world-flythrough/scripts/install_blender.sh ./blender-runtime
./blender-runtime/blender -b -t 4 --python skills/paint-world-flythrough/scripts/build_river_scene.py -- \
  --source painting.png --atlas paint_atlas.png --output scene.blend --preview-dir qa --width 960
```

`paint_atlas.png` 是四格油画材质，按技能中的提示生成。场景文件打包素材。先检查侧面、遮挡与天空环绕，再正式续渲；原生尺寸、渲染帧率、补帧与放大应如实记录。参考原图未展示的空间均属创作补全。

## 参考抽帧

```bash
python skills/paint-world-flythrough/scripts/prepare_video_evidence.py reference.mp4 evidence --times 0,5.5,11,13.2,18.6,18.9
```

输出目录必须为空，源素材保持只读。含《星月夜》原参考的按秒分析、中文和英文运镜提示词。
