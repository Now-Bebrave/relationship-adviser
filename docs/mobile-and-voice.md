# 移动端与语音使用

## WorkBuddy 手机端

优先使用 GitHub Skill 导入：

```text
https://github.com/Now-Bebrave/relationship-adviser
```

入口选择根目录 `SKILL.md`。若当前 WorkBuddy 版本只能粘贴提示词，使用 `adapters/workbuddy/MOBILE_PROMPT.md`，并把仓库链接作为知识来源。

更新时使用应用内“更新/重新导入”。移动端无法访问电脑上的 `private-vault/`；不要通过公开仓库同步私人资料。

## 语音输入

平台已经提供语音转文字时，直接把转写交给 Skill。独立管线可以运行：

```bash
python tools/voice_bridge.py input.json request.json
```

输入示例：

```json
{"transcript":"对象希望我辞职去外地结婚","language":"zh-CN","confidence":0.91}
```

输出会标记需要复核的金额、日期、否定词和低置信度文本。工具不上传音频，也不自带 ASR。

## 语音回答

模型先生成完整文字回答，再运行：

```bash
python tools/voice_bridge.py answer.json tts-request.json --response
```

生成物是供应商中立的 TTS 请求，不会主动调用网络服务。平台有 TTS 时可读取 `spoken_text`；没有时显示文字版。

## 私人决策日志

只有用户明确要求保存时运行：

```bash
python tools/decision_log.py private-vault/decisions/history.jsonl decision.json --consent
```

日志保存在本地 `private-vault/`，受 `.gitignore` 排除。删除该 JSONL 中对应记录即可撤回长期保存。

## 本地设备同步

私人资料如需在个人设备间同步，使用端到端加密、用户控制的目录。可先生成不含文件正文的完整性清单：

```bash
python tools/private_sync_manifest.py private-vault private-vault/sync-manifest.json
```

同步工具、密钥和目标设备由用户管理；公开 GitHub 仓库不承担私人同步。

