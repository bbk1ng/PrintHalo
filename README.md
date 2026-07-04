# repo-template

Self-bootstrapping project template wired for [agent-orch](https://github.com/bbk1ng/agent-orch).
Clone it, rename, and start shipping — the orchestration workflow, task tracking,
and a passing test are already in place.

## Layout

```
.
├── .orch/orch.yml          # agent-orch config (author/reviewer rotation, test gate, merge policy)
├── src/                    # source code (example.py is a placeholder — replace it)
├── tests/                  # stdlib unittest suite (no test deps)
├── tasks/
│   ├── todo.md             # active plan, checkable items
│   └── lessons.md          # corrections captured into rules
├── docs/                   # design notes, architecture
├── CLAUDE.md               # instructions for Claude Code / agents in this repo
├── WORKFLOW-ORCHESTRATION.md  # how work flows through plan → build → verify → merge
└── pyproject.toml          # project metadata
```

## Quick start

One command bootstraps a fresh project — clones the template, detaches its git
history, ensures agent-orch is installed + initialised, runs the test gate, and
leaves a clean repo with one commit:

```bash
curl -fsSL https://raw.githubusercontent.com/bbk1ng/repo-template/main/install.sh | bash -s myproject
# or, from a local clone:
./install.sh myproject
```

Then:

```bash
cd myproject
python3 -m unittest discover -s tests   # run the test gate
orch task "describe the change"          # author + cross-audit + test-gate + merge
```

`install.sh` removes itself from the new repo. Override the source repo or orch
package via the `TEMPLATE_REPO` / `ORCH_PKG` env vars.

## The orch loop

`orch task "<change>"` spins up an author agent on its own branch, a reviewer
agent cross-audits, the test gate (`python3 -m unittest discover -s tests`) must pass,
then it merges to `main`. Config lives in `.orch/orch.yml`. See
[agent-orch](https://github.com/bbk1ng/agent-orch) for the full command set.

## Conventions

- **Plan first** — non-trivial work starts in `tasks/todo.md`.
- **Verify before done** — never mark complete without a passing test.
- **Capture lessons** — after any correction, add a rule to `tasks/lessons.md`.

See [WORKFLOW-ORCHESTRATION.md](WORKFLOW-ORCHESTRATION.md) for the full workflow.
