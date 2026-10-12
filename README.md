# 短视频自动化工厂

用于沉淀可复用的视频制作 Skill。

## 已收录技能

| Skill | 用途 |
| --- | --- |
| [paint-world-flythrough](skills/paint-world-flythrough/) | 根据名画或插画，规划沉浸式穿行视频，生成关键帧、运镜提示词和三维制作简报 |

## 名画沉浸式穿行

工作流：参考证据分析 → 三维 / AI / 2.5D 路线选择 → 空间约束 → 终点倒推关键帧 → 逐段运镜 → 接续与验收。

- 区分视频直接展示、制作推断和复现设计。
- 提供中文及英文运镜提示词。
- 包含《星月夜》参考案例的按秒解析。
- 适配只支持首帧的图生视频工具，不假设所有工具都支持尾帧。
- 创建的是制作方案；实际出片需要相应的视频生成或三维制作能力。

## 安装与调用

下载 `skills/paint-world-flythrough/` 整个目录，保持其中 `SKILL.md`、`agents/`、`references/` 和 `scripts/` 的相对位置。

将目录放入本机 Codex 的技能目录。通常为 `~/.codex/skills/paint-world-flythrough/`；设置了 `CODEX_HOME` 时，使用其下的 `skills/paint-world-flythrough/`。Windows 常见位置是 `C:\Users\<用户名>\.codex\skills\paint-world-flythrough\`。

在重新加载技能后的会话中调用：

```text
用 $paint-world-flythrough 将这幅画制作成约20秒的沉浸式穿行视频方案。
先判断适合三维还是AI图生视频，给我关键帧、逐段运镜提示词和接续验收表。
我只有首帧图生视频工具，请按这个能力设计。
```

## 参考抽帧脚本

脚本依赖 Python 标准库，以及已加入 PATH 的 FFmpeg 和 FFprobe。无需 Whisper 或语音模型。

```text
python skills/paint-world-flythrough/scripts/prepare_video_evidence.py reference.mp4 evidence --times 0,5.5,11,13.2,18.6,18.9
```

输出目录必须为空。脚本保留源视频，只输出按源时间采样的图片和 `index.json`。

## 验证

已通过 Skill 结构校验、30.333 秒参考视频的实际抽帧，以及“夜间咖啡馆 / 9:16 / 单首帧工具”场景的独立试用。提示词尚未以付费视频生成进行效果验收。
