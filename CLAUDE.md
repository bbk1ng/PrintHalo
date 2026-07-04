# Project Instructions

Instructions for Claude Code (and other agents) working in this repo. Keep this
file current — it is loaded into context every session.

## What this is

<!-- Replace this section with a one-paragraph description of the project:
     what it does, the stack, and where the entry points are. -->

A project scaffolded from `repo-template`, wired for agent-orch.

## Workflow

This repo follows [WORKFLOW-ORCHESTRATION.md](WORKFLOW-ORCHESTRATION.md):

1. **Plan first** — for any non-trivial task (3+ steps), write the plan to
   `tasks/todo.md` with checkable items before touching code.
2. **One concern per change** — small, reviewable diffs.
3. **Verify before done** — run `python3 -m unittest discover -s tests`; never mark a
   task complete without a passing test.
4. **Capture lessons** — after any correction, add a rule to `tasks/lessons.md`.

## Conventions

- Tests are stdlib `unittest` — no test framework dependency. Run:
  `python3 -m unittest discover -s tests`.
- Source lives in `src/`, tests mirror it in `tests/`.
- Orchestrated changes go through `orch task "<change>"`; config in `.orch/orch.yml`.

## Guardrails

- Make the smallest change that solves the problem. Find root causes, no
  temporary patches.
- Don't add a dependency for what a few lines of stdlib can do.
- Confirm before destructive or irreversible actions.

<!-- orch:begin (managed by `orch init --link`; edits here are overwritten) -->
## orch
This repo uses agent-orch. See `.orch/ORCH.md` for usage; config in `.orch/orch.yml`.
@.orch/ORCH.md
<!-- orch:end -->
