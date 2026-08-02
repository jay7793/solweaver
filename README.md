# Solweaver

[![Validate](https://github.com/jay7793/solweaver/actions/workflows/validate.yml/badge.svg)](https://github.com/jay7793/solweaver/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Solweaver gives Codex a small software team without giving up control. GPT-5.6
Sol stays in charge while implementation work is woven across GPT-5.6 Terra
and GPT-5.6 Luna according to scope, risk, and coupling.

> Community project. Not an official OpenAI project.

## Why use it?

- **One clear lead:** Sol owns the plan, assignments, integration, and final
  answer.
- **Better model fit:** Terra handles judgment-heavy implementation; Luna
  handles narrow, repeatable, high-throughput work.
- **Safe parallelism:** workers run together only when their file ownership is
  disjoint.
- **Evidence before “done”:** the parent reviews worker changes and runs
  appropriate verification.
- **No surprise publishing:** deployment, production changes, commits, pushes,
  and pull requests still require user authorization.

## How it works

| Role | Runtime | Best fit |
| --- | --- | --- |
| Orchestrator | `gpt-5.6-sol` / `max` | Planning, decomposition, ownership, integration, review, and delivery |
| Default worker | `gpt-5.6-terra` / `max` | Coupled, ambiguous, multi-file, architecture-sensitive, and general implementation |
| Bounded worker | `gpt-5.6-luna` / `max` | Narrow, mechanical, repetitive, high-throughput, or independent file clusters |

The parent remains on the critical path. Workers receive bounded ownership and
cannot silently take over orchestration. Terra and Luna run in parallel only
when their write scopes are disjoint.

```text
User goal
   │
   ▼
Sol max ── plan, delegate, integrate, verify
   ├── Terra max ── coupled or judgment-heavy implementation
   └── Luna max  ── narrow or high-throughput implementation
   │
   ▼
Sol max ── review the integrated result and report evidence
```

## Included

- `skills/solweaver/`: the Codex skill and UI metadata
- `agents/terra-worker.toml`: Terra worker definition at `max`
- `agents/luna-worker.toml`: Luna worker definition at `max`
- `examples/config.toml`: parent runtime and concurrency example
- `examples/AGENTS.md`: minimal global routing policy
- `scripts/install.py`: dependency-free local installer
- `scripts/validate.py`: repository validation used by CI

## Before you install

- Use a Codex runtime and account where `gpt-5.6-sol`, `gpt-5.6-terra`, and
  `gpt-5.6-luna` are available.
- The installer needs Python 3.9 or newer.
- The validation script needs Python 3.11 or newer.
- The included workers use reasoning effort `max`, which prioritizes capability
  over token usage.

## Install

Clone the repository and run the safe installer:

```bash
git clone https://github.com/jay7793/solweaver.git
cd solweaver
python3 scripts/install.py
```

The installer copies the skill and both worker definitions into
`$CODEX_HOME`, or `~/.codex` when `CODEX_HOME` is unset. It refuses to overwrite
existing files.

Then merge, rather than blindly replace, the relevant settings from:

- `examples/config.toml` into `~/.codex/config.toml`
- `examples/AGENTS.md` into `~/.codex/AGENTS.md`

Restart Codex or open a new task after installation so the new skill, agents,
model, and reasoning settings are loaded.

## Use

Invoke the skill explicitly:

```text
$solweaver

Goal: implement the feature and verify it end to end.
```

With the example global policy installed, software-development prompts starting
with `Goal:` or `/goal`, and explicit requests such as `use software team`, can
load the skill automatically.

## Validate

Validation requires Python 3.11 or newer.

Run:

```bash
python3 scripts/validate.py
```

The validation checks the skill frontmatter, folder/name consistency, UI
metadata, both worker TOML definitions, model assignments, reasoning effort,
and example configuration.

## Safety boundaries

- The skill does not change the active model by itself.
- It does not authorize deployment, production mutation, pushing, merging, or
  pull-request creation.
- It preserves unrelated working-tree changes and requires explicit ownership
  for every writing agent.
- High-risk auth, money, tenant, data-integrity, or production paths remain on
  the Terra/parent route and should receive an independent security review.

## License

MIT
