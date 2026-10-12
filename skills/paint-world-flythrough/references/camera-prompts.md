# 可复制提示词与三维简报

以下均为复现设计，不是作者原始提示词。先代入当前画作、地标、首尾状态与空间约束，再提交制作工具。首尾帧、负面提示、seed必须确认工具支持；seed不能保证空间一致。

## 全局提示：星月夜示例

以参考《星月夜》的钴蓝夜空、暖黄色光点、旋转云带和厚涂笔触建立可穿行的画中村庄。固定同一座细长尖顶教堂、同一组村屋、同一段远山与同一棵深色前景树。每个物体表面都像油画颜料绘制，近镜仍可见笔触。为道路、教堂侧面和树枝补全合理空间，延续已有形状。保持蓝色环境光与暖黄窗光。不要改为写实摄影，不改变教堂身份，不添加现代城市、游客、镜头界面或文字。

迁移到其他作品：替换作品名、色板、笔触、主体地标与光照；不要强加教堂和星空。

## 关键帧：先终点，再起点

### K4 全景匹配帧

以上传原画为构图参照。深色高树在前景左侧，教堂与村屋在下方，远山横向延伸，旋涡夜空与黄色光点占据上方。保持同一建筑身份与色板，相机已退到足够远的位置。不要让新增桥梁或大树挡住核心识别线索。此图是动画收尾锚点；最终用干净原画完成精确收尾。

### K3 高处村庄帧

在同一场景中，相机位于屋顶上方，教堂偏画面中部，村庄延伸至远山。深色树干可从画面边缘靠近，为后续外退提供前景。保留教堂轮廓、山脉方向和天空旋涡位置关系。相机可自然继续退向K4。

### K2 教堂接近帧

相机来到同一条村街出口，暖黄窗光在两侧，前方同一座教堂清晰可见。屋顶、墙面和地面保持厚涂笔触。视线略向上，街道保持连续，不换村庄。

### K1 入口帧

相机位于夜晚村庄入口，窄路向教堂方向延伸，两侧低墙与深色植被，远处暖黄窗光，高处同一旋涡夜空。低位广角，建立真实空间纵深，不把原画放在前方当平面幕布。

## AI分段运镜

### S1 约0-5秒：前移

从给定首帧出发，低位相机沿道路平稳向前，逐步进入村庄街道。两侧墙与房屋掠过，同一座远处教堂变大。近景移动快、远景移动慢。蓝色油画夜景与暖黄窗光保持不变。只做连续前移，不跳到另一条街，不产生人物。结束时匹配K2的街口与教堂距离。

### S2 约5-10秒：升高、轻侧绕

沿用上一段尾帧的教堂与村屋。相机逐渐升至教堂屋顶附近并轻微侧绕，显露同一建筑侧面。保持尖顶、建筑比例、远山与夜空背景方向。不要大角度环绕，不替换建筑；结束于K3的屋顶视角。

### S3 约10-15秒：外退、前景遮挡

从同一高处村庄视角缓慢外退。固定教堂、屋顶和山脉；一根深色前景树干从边缘掠过，短暂遮挡后离开。相机方向连续，树干不凭空出现。可在最大遮挡处接续片段。结束时显露较宽的村庄与夜空。

### S4 约15-20秒：拉远、减速

继续后退并逐渐减速，前景高树、下方村庄、远山与旋涡天空形成接近原画的布局。工具支持时以K4约束尾帧。最后保持稳定，不突然变成写实照片。不要要求模型强行变成精确原画；后期以干净原图衔接。

## 英文运镜短版

S1: A low camera moves steadily forward along the painted village street toward the same church. Clear foreground parallax, stable architecture, cobalt-blue night and warm windows. Preserve oil-paint brushwork. End at the supplied street-exit frame.

S2: The camera rises gently beside the same church and makes a small side arc. Preserve the steeple silhouette, building identity, mountains and painted sky. Reveal a coherent side view. No geometry morphing or sudden orbit.

S3: The camera retreats from the village. A nearby dark painted tree crosses the lens, briefly occluding it before revealing the same village. Continuous camera direction and stable landmark positions. No teleportation.

S4: Continue pulling back and ease to a stop. Compose the foreground cypress, village, distant hills and swirling sky to resemble the supplied painting. Keep the same style and landmarks. Hold a stable final frame for the edit to the original artwork.

## 负面约束

建筑轮廓漂移、复制教堂、屋顶融化、树木凭空生长、天空突然换色、瞬移、局部写实、现代车辆、文字、水印、二维码、突然换场景。工具没有负面提示字段时，只将最重要的2-3条变为正向约束加入主提示。

## 三维路线简报

以原画为风格和最终构图参照建立三维场景。先列地标ID与位置表，建立体块，再在最终相机中校验构图；不要先堆细节。

将前景树枝、村庄和教堂、远山、天空设为不同深度层。需要侧绕的建筑使用有侧面与背面的实体几何；远山可用低模或背景卡，天空可用绘画纹理穹顶。新增街道、地形明确标为创作补全。

统一墙、瓦、地面、植物的绘画纹理，采用蓝色环境光与柔和暖黄窗光。近景测试笔触尺度，避免纹理拉伸。天空投射方式要检查是否出现不自然的贴屏移动。

创建连续相机路径：低位沿街进入 → 教堂附近平滑升高侧绕 → 屋顶外退 → 前景树遮挡 → 拉远减速。逐段预览，不穿墙或穿树干。最后匹配原画地标布局；无法精确匹配时明确切到原画，不宣称无缝变形。

交付布局、地标清单、相机路径、预览与正式渲染。先做短段验证，再决定最终分辨率。简报可以指导代理，不能自动替代建模、贴图、渲染工作。

## 失败后的首要调整

| 失败 | 首要调整 |
| --- | --- |
| 绕行时尖顶融化 | 减少绕行角度，固定同一教堂首尾帧 |
| 延长越来越偏 | 用已验证关键帧重新锚定 |
| 近镜笔触消失 | 先修正关键帧材质，再重做运镜 |
| 最后硬变原画 | 先做接近全景的K4，再后期接原图 |
| 叠化出现双重尖顶 | 匹配地标位置与尺度，缩短叠化或明确切换 |
| 天空或山脉变化 | 统一空间约束与参考体系，不能只锁色板 |
