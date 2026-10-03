# Codex、Claude Code 与 WorkBuddy 同步

## 单一来源

本机唯一资料源是：

```text
D:\WorkFiles\adviser
```

Codex 和 Claude Code 的 `relationship-adviser` 安装目录应指向这个目录，而不是各自保存一份副本。WorkBuddy 手机版无法读取电脑目录，因此以 GitHub `main` 为公共资料源：

```text
https://github.com/Now-Bebrave/relationship-adviser
```

## 调用方式

| 平台 | 调用 |
|---|---|
| Codex | `$relationship-adviser` |
| Claude Code | `/relationship-adviser` |
| WorkBuddy | `/relationship-adviser` |

## 补充资料后的同步

1. 资料只写入仓库根目录的 `knowledge/`、`core/`、`visuals/` 或本地 `private-vault/`；
2. 运行测试和校验；
3. 将公开资料推送到 GitHub；
4. Codex 和 Claude Code 无需复制文件，重新开启对话即可读取本地新内容；
5. WorkBuddy 打开 Skills 管理，选择更新；没有更新按钮时重新导入仓库；
6. 检查 Skill 名称为 `relationship-adviser`，版本见 `adapters/manifest.json`。

## 一致性检查

```powershell
python tools/check_install_sync.py `
  D:\WorkFiles\adviser `
  C:\Users\30239\.codex\skills\relationship-adviser `
  C:\Users\30239\.claude\skills\relationship-adviser
```

输出 `all installations match canonical source` 表示 Codex 和 Claude 使用同一套公开资料。

## 隐私限制

公共 GitHub 只同步公开研究、指南、模板和脱敏案例。`private-vault/`、原始视频、私人聊天和决策日志留在本机。WorkBuddy 若需要某个私人案例，应在当次对话中由用户主动提供必要且脱敏的信息。

