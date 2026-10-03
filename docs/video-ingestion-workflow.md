# 视频与图文案例整理流程

本仓库采用“文字优先、按需解析”的策略：已有完整图文笔记时不重复解析整段视频；只有笔记缺失、上下文冲突或需要核对关键时间点时，才增加截图抽查或全文提取。

## 1. 目录边界

- MediaCrawler 原始视频、截图和平台缓存保留在本地采集目录；
- `private-vault/source-index/media-index.json` 只保存本地媒体的路径、大小、修改时间、哈希和类型；
- 去身份化后的观点、时间戳、限制和行动建议才可以整理进公开 `knowledge/`；
- 不把本地绝对路径、账号隐私、聊天原文、未授权视频或私人案例提交到 GitHub。

## 2. 建立媒体索引

在仓库根目录运行：

```powershell
python tools/index_media.py <MEDIA_ROOT> --output private-vault/source-index/media-index.json
```

`<MEDIA_ROOT>` 替换为本机 MediaCrawler 数据目录。索引只处理 mp4、mov、mkv、mp3 和 wav，并为每个文件计算 SHA-256，方便去重和确认文件是否变化。

## 3. 选择提取模式

使用 `tools.extraction_plan.choose_extraction_mode` 的规则：

| 现有材料 | 模式 | 处理方式 |
|---|---|---|
| 笔记完整、无截图冲突 | `notes_only` | 只整理文字笔记 |
| 笔记完整、有关键截图 | `notes_plus_images` | 文字为主，核对截图 |
| 笔记不完整或材料有冲突 | `notes_plus_spotcheck` | 只抽查冲突时间点 |
| 没有可用文字 | `full_video` | 配置本地 ASR/OCR 后再提取 |

当前仓库不会假装已经完成全文提取。没有配置本地 ASR/OCR 时，`full_video` 会明确报错，而不是生成看似完整的虚假字幕。

## 4. 将图文笔记转成视频卡片

笔记建议使用标题、时间戳和以下栏目：`观点`、`话术`、`对方反应`、`回应`、`限制`。然后运行：

```powershell
python tools/normalize_video_notes.py `
  --source <NOTE_FILE> `
  --output <VIDEO_CARD_JSON> `
  --platform douyin `
  --author <AUTHOR> `
  --mode notes_only
```

完整笔记包含截图时，将模式改为 `notes_plus_images`。输出字段遵循 `knowledge-schema/video-card.schema.json`，包括来源、主题、时间戳文字、主张、话术、反应、回应和限制。

## 5. 进入知识库前的人工核验

1. 把可观察内容和博主解释分开；
2. 为每个主张保留原链接、发布时间和时间戳；
3. 将经验建议标记为案例材料，不写成研究定律；
4. 对涉及彩礼、性、财务、暴力或医疗的内容，补充可靠研究或官方资料；
5. 去除姓名、账号、联系方式、面部截图和与决策无关的私密细节；
6. 只把可复用的结构、话术、反应分支和停止条件写入公开指南。

## 6. 自动生成案例草稿

可以先把字幕、OCR 或图文笔记整理为带标签的文本：

```text
[事实] 对方提出了住房条件
[观点] 先确认预算再谈金额
[推测] 对方可能担心诚意
[未知] 房产登记和借款性质
```

然后运行：

```powershell
python tools/case_pipeline.py note.txt draft.json --platform douyin
```

工具会生成事实/观点/推测/未知分类、内容指纹、隐私标记和路由结果。出现本地绝对路径、手机号或邮箱时自动路由到 `private_review`，不会直接进入公开案例库。工具只生成草稿，来源、授权、事实和脱敏仍需人工复核。

## 7. 失败处理

- 图文笔记与截图冲突：保留冲突记录，改用 `notes_plus_spotcheck`，不要自行补全；
- 视频无字幕且没有本地 ASR/OCR：保留来源和待处理状态，不把摘要写成事实；
- 链接失效或无法确认作者：降为低证据案例，不能单独支撑决策；
- 资料含私人案例：只写入 `private-vault/`，不进入提交或公开视频卡片。

