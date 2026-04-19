# sister-skill

> Bring back the little sister who sounds real, not obedient by default.

Turn chat logs, photos, social screenshots, and your descriptions into a runnable sister AI Skill.

Repository:
https://github.com/Wasdar456/sister-skill

---

## Installation

```bash
mkdir -p .claude/skills
git clone https://github.com/Wasdar456/sister-skill .claude/skills/create-sister
```

Global install:

```bash
git clone https://github.com/Wasdar456/sister-skill ~/.claude/skills/create-sister
```

Optional dependency:

```bash
pip3 install -r requirements.txt
```

---

## Usage

Run:

```text
/create-sister
```

Main commands:

| Command | Description |
|---------|-------------|
| `/create-sister` | Create a sister Skill |
| `/update-sister {slug}` | Append new material |
| `/list-sisters` | List all sister Skills |
| `/sister-rollback {slug} {version}` | Roll back |
| `/delete-sister {slug}` | Delete |

---

## Architecture

The generated Skill keeps a dual-track core:

1. Part A: Relationship Memory
2. Part B: Persona

The runtime output is driven by Persona first, then grounded by Memory.

Additionally, generated SKILL.md includes Part C (Attribute Tuning Console):

- Tsundere
- Bratty
- Brother-complex
- Kuudere
- Clingy

Each defaults to 20%, and the total must always be 100%.
