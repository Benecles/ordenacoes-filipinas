# Notes for coding agents

Before changing anything in this repository, read the workshop's `CEO.md` (private repo `Benecles/ordenacoes-filipinas-workshop`), the newest entries in its `FLIGHT-LOG.md`, and its open GitHub Issues. They say who owns what, what is in progress and what must not be redone. The workshop's `archive/Relay Baton.md` is frozen history (coordination moved to Issues on 01/10); Codex's working rules live in `~/.codex/AGENTS.md`.

- Work that happens in Claude Code **cloud** sessions is mirrored in the private workshop repository (formerly `benecles/study-lab-private`; same home-relative paths as the owner's Mac, text only). Bring its newest entries into your picture before starting new work.
- Fixes may arrive on `claude/*` and `codex/*` branches before they reach `main`. Check open branches and PRs before publishing.
- After adding or changing any page, run `python3 tools/offline_build.py`; after hand-editing generated pages, run `python3 tools/polish.py capture` and then `python3 tools/polish.py check`.

## Checks on GitHub (CI-1, 05/10)

Every PR and every push to `main` runs `.github/workflows/checks.yml`: `tools/check_all.sh`, then a check that the committed tree already equals what `tools/offline_build.py` produces (manifest lists exactly the committed files; scripts injected; nothing left for sanitize/landscape/assetver to change).

- **Before merging, look at the PR's check** (`gh pr checks <n>`). Green: merge. Red: fix it on the branch first. The usual fix is to rebase on `main`, run `python3 tools/offline_build.py`, and commit.
- It is advisory (not a required check), so a red X won't stop `gh pr merge`. Don't merge red anyway: `main` is the live site.
- Breakscan and screenshots still need a browser and run locally, as before.
- **Work in your own checkout** (a clone or `git worktree` per agent), never in another agent's folder. Claim the issue (assign or comment) before starting, so two agents don't build the same thing.
