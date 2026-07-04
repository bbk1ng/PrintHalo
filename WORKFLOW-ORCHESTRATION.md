# Workflow Orchestration

How work flows through this repo: **plan → build → verify → merge**.

## 1. Plan first
- Enter plan mode for any non-trivial task (3+ steps or an architectural decision).
- Write the plan to `tasks/todo.md` with checkable items before touching code.
- If something goes sideways, stop and re-plan — don't keep pushing.

## 2. Build small
- One concern per change. Small, reviewable diffs.
- Use subagents for research, exploration, and parallel analysis to keep the
  main context clean. One focused task per subagent.
- Make the smallest change that works. Find root causes, not temporary patches.

## 3. Verify before done
- Never mark a task complete without proving it works.
- Run the test gate: `python3 -m unittest discover -s tests`.
- Ask: "Would a staff engineer approve this?"

## 4. Merge via orch
- `orch task "<change>"` runs the full loop: an author agent writes on its own
  branch, a reviewer agent cross-audits, the test gate must pass, then it merges
  to `main`. Config: `.orch/orch.yml`.
- For an existing PR: `orch pr <number> [--merge]`.

## 5. Capture lessons
- After any correction, add the pattern as a rule to `tasks/lessons.md`.
- Review `tasks/lessons.md` at the start of a session.

---

## Task management

1. **Plan** — write `tasks/todo.md` with checkable items.
2. **Track** — mark items complete as you go.
3. **Explain** — high-level summary at each step.
4. **Document** — add a review section to `tasks/todo.md` when done.
5. **Capture** — update `tasks/lessons.md` after corrections.

## Core principles

- **Simplicity first** — every change as simple as possible; minimal blast radius.
- **No laziness** — root-cause fixes, senior-developer standards.
- **Minimal impact** — touch only what's necessary; avoid introducing bugs.
