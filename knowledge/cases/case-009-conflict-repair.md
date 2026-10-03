# 案例 009：道歉后反复出现同一伤害

- `case_id`: case-009-conflict-repair
- `source`: synthetic_training_template；用于测试修复是否具有行为证据
- `topic`: 冲突与修复
- `evidence_level`: L3
- `privacy`: 已脱敏；无真实对话原文

## Context

伴侣在争吵时辱骂，事后道歉并承诺改变，但一周后再次发生。受伤的一方不确定应继续观察、设置边界还是退出。

## Facts and unknowns

- 已知：伤害行为重复，口头道歉没有带来稳定变化。
- 未知：是否存在暴力、威胁、物质使用、主动求助和安全退出条件。

## Decision rule and actions

1. 记录触发、行为、后果、道歉和下一次发生时间。
2. 提出一个可观察的 7 天修复协议，例如暂停争吵、禁止辱骂、主动求助。
3. 以行为兑现而非情绪强度判断是否继续，不承担监督对方改变的全部责任。

## Likely reactions and responses

- “我都道歉了还要怎样”：回答“道歉是开始，是否继续取决于持续行为和安全。”

## Result and limits

`result`: unknown；训练模板不判断真实关系是否应继续。

## Stop conditions

暴力、威胁、跟踪、报复或拒绝任何边界时停止单独谈判并启动安全支持。

