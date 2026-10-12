---
name: pr-stacks
description: Turn a repo's open PRs into stacks and substacks, write a living merge runbook for the human operator (coach), and keep the next substacks rebased and fast-forwardable while coach executes. Use when asked to plan, sequence, prepare, or babysit a batch of PRs for deployment, or when coach reports a step done ("refresh", "next", "step 4 done").
---

# pr-stacks

**Coach** is the human who merges and does the manual steps. Coach often did not author or review the PRs, so every step must stand on its own. **You** discover, order, document, and rebase. You never merge, close, approve, or run a deploy step.

Arguments (`$ARGUMENTS`, all optional): `owner/repo` (default: the cwd remote), a filter (`label:x`, `author:y`, `base:z`), and free text from coach such as "step 4 done".

## Terms

| Term | Meaning |
|---|---|
| Stack | PRs whose `origin/main..head` commit sets nest by patch-id: A ⊂ B ⊂ C. C is the stack head. A lone PR is a stack of one. |
| Covered | PRs GitHub auto-closes as merged when a head lands, because their head SHA is a literal ancestor of it. Patch-id equivalence finds stacks; only identical SHAs auto-close. |
| Manual step | Anything coach does besides merge: RUN a command or migration, WAIT for it, CHECK a result, TOGGLE a setting, CONFIRM something the PR text leaves unclear. The gap inside a widen/tighten (expand/contract) pair is always one. |
| Substack | The PRs of one stack between two manual steps. Its head is what coach merges. |
| READY | Head is a descendant of `origin/main`, CI green, no changes-requested review. Fast-forwardable now. |
| BEHIND | Not a descendant, but `git merge-tree` is clean. You can rebase it. |
| CONFLICTS | `git merge-tree` reports conflicts. Needs judgment. |
| PARKED | Draft, WIP/do-not-merge label, red CI, or changes requested. Not yours to fix. |
| FROZEN | The PR(s) of the step coach is executing right now. Never touch. |

## Each run

Runs are re-entrant. Redo steps 1–4 from live state every time, then do one unit of step 5.

### 1. Discover

```sh
gh pr list -R $REPO --state open --limit 200 \
  --json number,title,body,url,isDraft,labels,author,createdAt,headRefName,headRefOid,baseRefName,reviewDecision,mergeable,statusCheckRollup > prs.json
git fetch origin main '+refs/pull/*/head:refs/remotes/pr/*'
# per PR N:
git rev-list --reverse origin/main..pr/N                                    # its commits
git rev-list origin/main..pr/N | while read c; do git diff-tree -p "$c" | git patch-id --stable; done
git merge-base --is-ancestor origin/main pr/N                               # READY-shaped?
git merge-tree --write-tree origin/main pr/N >/dev/null                     # exit 0 clean, 1 conflicts (git ≥ 2.38)
```

Also pull each PR's conversation: `gh pr view N --comments` and `gh api repos/$REPO/pulls/N/comments`. Without `gh`, use the GitHub MCP tools for the same data.

### 2. Classify

- **Stacks.** A sits under B when patchids(A) ⊆ patchids(B). Chain them. Mark each edge *literal* (A's head is an ancestor of B's head) or *logical* (patch-id only; must be re-pointed in step 5 before B can close A).
- **Diamonds** (B covers independent A1 and A2) are fine; note them. Identical commit sets are duplicates; flag for coach.
- **Ghosts.** All of a PR's patch-ids are already in main but its head is not reachable. It will never auto-close. Emit a CLOSE step for coach with the evidence.
- **Manual steps.** Read titles, bodies, comments, review threads, and the changed-file list. Triggers: checklist items, and words like migration, backfill, run, flag, toggle, env, secret, widen/expand, tighten/contract, before/after merge, pause, verify. Paths like `migrations/`, `db/`, `*.sql`, `config/`, `.env*`, `infra/`. Each hit becomes a step with the source quoted and linked. Unsure whether a step is real? Emit CONFIRM. Never guess a step away.
- **Widen/tighten.** Two PRs in one stack where the later removes or constrains what the earlier added. The gap is a WAIT plus a CHECK, and the two are separate substacks.

### 3. Order

Sort substacks by this key, ascending, and recompute every run:

1. readiness tier: READY, BEHIND, CONFLICTS, PARKED
2. has a manual step: yes first (coach is the bottleneck, and a WAIT is time you spend rebasing)
3. more commits first
4. older stack first

Then schedule **steps, not stacks**. A WAIT blocks only its own stack, so the steps during a wait come from the next READY substack of another stack, and the waiting stack resumes after its CHECK passes. Pin every MERGE to a head SHA.

### 4. Write or update the runbook

One living document, updated in place: keep coach's checkmarks, append to its changelog. Default home is a GitHub issue titled `Deploy runbook <date>` in the repo, mirrored to a local file. Template below.

### 5. Prep (one unit per run)

Target: the first substack in order that is BEHIND and not FROZEN.

1. In a throwaway worktree, rebase the **stack head** branch onto `origin/main`. Only heads get rebased; lower PRs get re-pointed.
2. Prove nothing but SHAs changed: `git range-diff $(git merge-base <old-head> origin/main)..<old-head> origin/main..<new-head>`. Every row must be `=`. A `!` row is a conflict resolution: keep it minimal, quote the hunk in a PR comment, and mark that MERGE step "re-review needed".
3. Push with lease: `git push --force-with-lease=<branch>:<old-sha> origin <new-sha>:refs/heads/<branch>` for the head branch, then for each covered PR to the commit in the new history that carries its last patch-id. Every lower head is now a literal ancestor again.
4. Comment once on the head PR: rebased onto main `<sha>`, range-diff clean (or the hunks). Wait for CI. Promote to READY in the runbook and log old→new SHAs.
5. Preview the following substack in a scratch worktree on top of `origin/main` plus the current READY head. Write expected conflicts into the runbook. Never push a preview.

When coach reports a step done: fetch, confirm every covered PR shows MERGED, and emit a CLOSE step for any that did not.

CONFLICTS substacks: attempt the rebase. A mechanical resolution (adjacent lines, import order, a lockfile regenerated with the repo's tool) is a `!` row above. Anything else: stop, write the conflicting files and your proposed resolution into the Parked section, and ask the author on the PR.

## Guardrails

- Never merge, approve, close, or run a deploy or migration. Coach does those.
- The set of patch-ids in a PR's `origin/main..head` never changes by your hand. No squash, fixup, reorder, drop, or add. Rebase stack heads onto `origin/main` only, never onto another open PR. The reviewed chain stays the reviewed chain.
- Never force-push without `--force-with-lease`, and never a FROZEN branch.
- A conflict resolution that changes behavior is never silent: range-diff hunk on the PR, "re-review needed" in the runbook.
- Manual steps come from PR text and diffs only. No outside research. A page trail you cannot source reads "not in PR; ask @author", not a guess.
- An unresolved question in a PR thread is listed on its MERGE step. If a later PR or comment answers it, link the answer. Do not answer it yourself.
- The runbook is updated, never regenerated. Changelog every SHA you moved.
- Coach merges by fast-forward push or merge commit, never squash or "rebase and merge". Both mint new SHAs and orphan the covered PRs.

## Runbook template

```markdown
# Deploy runbook — <repo> — <date>
main at `<sha>` as of <time>. States: READY / BEHIND / CONFLICTS / PARKED. ⚑ = manual step.
Agent updates this in place; coach ticks boxes. Current step: 1 (its PRs are FROZEN).

## Stacks
| # | Stack (bottom → head)   | Substacks                        | Commits | State | Oldest     | ⚑   |
|---|-------------------------|----------------------------------|---------|-------|------------|-----|
| 1 | #1227 → #1230 → #1234   | [#1227 #1230] ⚑ migrate [#1234]  | 7       | READY | 2026-09-30 | yes |
| 2 | #1301                   | [#1301] ⚑ flag                   | 2       | READY | 2026-10-02 | yes |
| 3 | #1402 → #1410           | [#1402 #1410]                    | 5       | CONFLICTS | 2026-10-01 | no |

## Steps
- [ ] **1. MERGE #1230** `feat/foo-widen` head `a1b2c3d` — covers #1227
  - What: #1227 adds the `foo_v2` column (nullable). #1230 dual-writes to it. Approved by @r1, @r2.
  - Precondition: `git fetch origin && git merge-base --is-ancestor origin/main a1b2c3d` — if false, stop; agent re-preps.
  - Command: `git push origin a1b2c3d:refs/heads/main`
    Protected main: `gh pr merge 1230 --merge --match-head-commit a1b2c3d`
  - Verify: `gh pr view 1227 --json state` → MERGED. CI on main green.
  - Open questions: #1230 "do we backfill before tighten?" — answered in #1234 by @x: "yes, see step 6" (link).
    #1230 "keep the old column a week?" — UNRESOLVED; ask @author.
  - Rollback: `git revert --no-edit <main-before>..a1b2c3d`
- [ ] **2. ⚑ RUN** — from #1230 body: "<quoted instruction>" (link). Command: `<verbatim from PR>`
- [ ] **3. ⚑ WAIT** until <condition quoted from PR>. Meanwhile do steps 4–5.
- [ ] **4. MERGE #1301** `feat/refurb-flag` head `<sha>` — covers nothing. ...
- [ ] **5. ⚑ TOGGLE** Settings > Deploy Settings > Feature Flags > "foo refurbishing" → Off (from #1301 comment, link). Not in PR: who owns the flag; ask @author.
- [ ] **6. ⚑ CHECK** <how to confirm step 3's migration finished, quoted from PR>.
- [ ] **7. MERGE #1234** `feat/foo-tighten` head `<sha>` — re-review needed: conflict resolved in `db/schema.rb`, see PR comment (link).

## Parked
- Stack 3 (#1402 → #1410): CONFLICTS in `api/routes.ts` against main `<sha>`. Proposed resolution in PR comment (link). Needs @author.
- #1388: draft.

## Changelog
- <time> rebased #1234 head `e4f5…` → `9a8b…`; re-pointed #1230 `b2c3…` → `7d6e…`; range-diff clean; CI pending.
```

## Command crib for coach

- Fast-forward merge: `git fetch origin && git push origin <sha>:refs/heads/main`
- Protected main: `gh pr merge <n> --merge --match-head-commit <sha>` (never `--squash`, never `--rebase`)
- Did it cover? `gh pr view <m> --json state,mergedAt`
