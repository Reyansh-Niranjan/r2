# Antigravity CLI (`agy`) Tool Mapping

Skills speak in actions ("dispatch a subagent", "create a todo", "read a file"). On the Antigravity CLI (`agy`) these resolve to the tools below.

| Action skills request | Antigravity CLI equivalent |
|----------------------|----------------------|
| Dispatch a subagent (`Subagent (general-purpose):` template) | `invoke_subagent` with a built-in `TypeName` — `self` for full-capability work, `research` for read-only |
| Task tracking ("create a todo", "mark complete") | `update_steps` — Antigravity's native live TODO checklist tool directly in the conversation UI. (Use `update_focus` alongside for phase status). **Not** `manage_task`, which manages background processes. |

## Task tracking

Antigravity provides the native **TODO / Task List tool (`update_steps`)** to display and manage a live interactive checklist in the conversation UI.

- Use `update_steps` at the start of any multi-step task (3+ steps) to publish the ordered checklist.
- Keep task items short (2-6 words), action-oriented, and imperative (e.g. "Run test suite", "Update config").
- Update the list live as each step starts (`in_progress`) and completes (`done`).
- Use `update_focus` in parallel to communicate high-level phase activity.
- **NEVER** write task lists, checklists, or checkpoint state to `TASKS.md`, `tasks.md`, or markdown task artifact files on disk. Task tracking lives strictly in the conversation UI via `update_steps`.
