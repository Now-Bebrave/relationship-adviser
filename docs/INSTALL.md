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
