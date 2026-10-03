# Install relationship-adviser

The repository is public. It contains shared rules, verified sources, playbooks, and sanitized public examples. Personal profiles, private cases, raw media, and media indexes remain under `private-vault/` and are ignored by Git.

## Generic installation

Clone the complete repository so the root SKILL.md, core/, and knowledge/ stay together:

    git clone https://github.com/Now-Bebrave/relationship-adviser.git relationship-adviser

Load relationship-adviser/SKILL.md in the agent. Do not copy only an adapter file without the repository because its shared files are relative paths.

## Codex

    $target = Join-Path $HOME '.codex\skills\relationship-adviser'
    git clone https://github.com/Now-Bebrave/relationship-adviser.git $target

Restart Codex or refresh its skills list, then invoke relationship-adviser.

## Claude Code and compatible Agents skills

    $target = Join-Path $HOME '.agents\skills\relationship-adviser'
    git clone https://github.com/Now-Bebrave/relationship-adviser.git $target

If the installation uses Claude Code's private directory instead:

    $target = Join-Path $HOME '.claude\skills\relationship-adviser'
    git clone https://github.com/Now-Bebrave/relationship-adviser.git $target

## WorkBuddy mobile

If the mobile app supports importing a GitHub skill, import:

    https://github.com/Now-Bebrave/relationship-adviser

Choose the root entry SKILL.md and name it relationship-adviser. If the app only accepts an instruction message, paste the contents of the root SKILL.md and keep the GitHub URL as the knowledge source. The mobile app may not support local filesystem paths or automatic Git updates; this depends on the installed WorkBuddy version.

For a shorter mobile prompt, use `adapters/workbuddy/MOBILE_PROMPT.md`. Voice input uses the app's own speech recognition when available; the repository does not upload audio or bundle a cloud speech provider.

### 注册和显式调用

1. 打开 WorkBuddy 的 **Skills 管理**；
2. 选择从 GitHub/仓库导入，填写 `https://github.com/Now-Bebrave/relationship-adviser`；
3. 入口选择根目录 `SKILL.md`；
4. 名称保持 `relationship-adviser`；
5. 安装或更新完成后，在新对话输入：

```text
/relationship-adviser
```

也可以一行调用：

```text
/relationship-adviser 我跟对象因为结婚城市和父母照护发生分歧，请给明确结论、步骤、话术、反应分支和停止条件。
```

如果输入 `/` 后没有显示该命令，先刷新 Skills 列表或重新导入仓库。若当前手机版只支持自然语言触发，使用：

```text
使用 relationship-adviser 分析：这里写你的问题
```

这两种调用方式加载的是同一个根 `SKILL.md`，不会改变知识库内容。

## Update

For cloned installations:

    cd relationship-adviser
    git pull --ff-only

For a skills-directory installation:

    cd (Join-Path $HOME '.codex\skills\relationship-adviser')
    git pull --ff-only

Replace .codex\skills with .agents\skills or .claude\skills for the other targets. Mobile imports need the app's update action or a re-import if automatic update is unavailable.

## Public case boundary

`examples/cases/` contains sanitized, public-facing case cards. Do not add names, contact details, screenshots with identifiers, private chat logs, raw video, or copied personal stories. Put those materials in `private-vault/` instead.
