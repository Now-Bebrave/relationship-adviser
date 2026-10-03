# 项目长期约定（MEMORY）

## 插画能力池（图文并茂项目）

本项目"图文并茂"插画有**两套可选的插画 skill**，实际使用时按场景二选一：

### 1. ian-xiaohei-illustrations（小黑手绘，默认首选）
- 路径：`~/.workbuddy/skills/ian-xiaohei-illustrations/`
- 定位：中文正文配图，怪诞、极简、白板手绘草图感，黑色实心"小黑"IP（白点眼、细腿、空表情），纯白底 + 少量红/橙/蓝中文手写批注，16:9 横版，大量留白。
- 适用：表达"判断 / 流程 / 隐喻 / 状态 / 前后对比"等抽象概念的正文配图，需要清爽、克制、有人格化动作主体（小黑）时。
- 触发词：小黑、怪诞、手绘、正文配图、文章插图。

### 2. handdraw-style（280 种手绘风格库，按需调用）
- 路径：`~/.workbuddy/skills/handraw-style/`
- 定位：全库 280 种手绘风格（#001–#280）+ 36 种经典主题色（C-01–C-36）+ 122 种排版图型（SC/IG/SB）。默认智能推荐风格+主题色组合，支持图文/纯图双模式。
- 适用：需要指定某种具体艺术风格（如某作者风格、某画风）、海报、封面、IP 设计、风格融合、社媒卡片等，追求视觉丰富度与风格多样性时。
- 子入口：article-illustration-planner（文章配图规划）、poster-prompt-generator（海报）、article-cover-designer（封面）、style-fusion-prompter（风格融合）、ip-designer（IP 设计）、custom-asset-manager（图库管理）、knowledge-video-director（视频分镜）。
- 触发词：指定风格编号、海报、封面、公众号头图、IP 设计、风格融合。

### 选择原则（场景混用）
- 默认（无指定风格、要抽象概念配图）→ 用 ian-xiaohei-illustrations（小黑）。
- 用户指定某风格编号/要海报/封面/特定画风 → 用 handdraw-style。
- 生成工具统一用 ImageGen（消耗额度约 5-10 点/张，需先告知用户）。

### 关系/情感主题 · 首选风格与备选（已定稿）
关系观察手册等"成人关系 / 婚姻谈判 / 情感抉择"类主题，handdraw-style 的选定风格如下（用户已确认偏好朱德庸版）：

| 优先级 | 编号 | 风格 | 适合场景 |
|---|---|---|---|
| 首选 | FE-025 | 朱德庸 Minimal Adult Relationship Satire | 婚姻谈判、金钱博弈、对峙张力，冷峻一针见血 |
| 备选 | FA-015 | Brian Rea Soft Relationship Editorial Line Art | 温柔关系线稿，伤感/疗愈/细腻情绪 |
| 备选 | FA-031 | Marjane Satrapi 高对比黑白回忆录 | 回望上一段、复盘成长、自传疗愈叙事 |

- 以上三款均为强激活风格（模型原生理解，无需垫参考图）。
- 场景混用原则：同一份文档内可依段落情绪混搭——抽象隐喻/自嘲用小黑，谈判对峙用朱德庸，疗愈复盘用 Brian Rea 或 Satrapi。以适配更多场景为准，不强制统一单一画风。

### 交付规范
- 生成的图片存 `assets/<主题-slug>-illustrations/`，按 `01-xx.png` 顺序命名。
- HTML 报告中的插画用 base64 内嵌，保证单文件自包含可下载（脚本 `tools/inline_illustrations.py`）。
- 内嵌脚本模板：读取 html → 对每个 `src="assets/.../xx.png"` 替换为 `data:image/png;base64,...`。

## 其他
- 情感咨询档案存 `~/.workbuddy/skills/relationship-adviser/private-vault/profile/profile.yaml`（用户明确要求"记住"才写入；该目录已被 .gitignore 排除，不上传 GitHub）。
- 本工作区即 relationship-adviser skill 的开发仓库。
- 本项目后续会上传到 GitHub，本约定文档（.workbuddy/memory 内）不含敏感隐私，可随仓库提交。
