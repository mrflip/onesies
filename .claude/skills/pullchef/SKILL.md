---
name: pullchef
description: Pullchef groups a repo's open PRs into stacks and substacks, writes a living merge runbook for the human who merges them (coach), and keeps upcoming substacks rebased and purple-ready while coach works. Use when asked to plan, sequence, prepare, or babysit a batch of PRs for merging, when coach reports a step done ("refresh", "next", "step 4 done"), or on "pullchef".
---

# pullchef

**Coach** is the human who merges and does the manual steps. Coach often did not author or review the PRs, so every step must stand on its own. **Pullchef** (you) discovers, orders, documents, and rebases.

Pullchef has the duty and the right to push to any open PR branch in the repo. Every such push uses an explicit-SHA lease:

```sh
git push --force-with-lease=<branch>:<expected-sha> origin <new-sha>:refs/heads/<branch>
```

A bare `--force-with-lease` is not a lease. Pullchef never merges, approves, or closes a PR, and never runs a deploy step. Those are coach's.

Arguments (`$ARGUMENTS`, all optional): `owner/repo` (default: the cwd remote), a filter (`label:x`, `author:y`, `base:z`), and free text from coach such as "step 4 done" or a directive.

## Terms

| Term | Meaning |
|---|---|
| Stack | PRs whose `origin/main..head` commit sets nest by patch-id: #1230 (a) ⊂ #1234 (a b c) ⊂ #1239 (a…g). #1239 is the stack head. A lone PR is a stack of one. |
| Covered | PRs that turn purple when a head merges, because their head SHA is an ancestor of the merged head. Patch-id equivalence finds stacks; only identical SHAs turn purple. |
| Parallel | The same logical commit under two SHAs in two PRs of one stack. A substack holding a parallel commit is BEHIND until the lower branch is re-pointed. |
| Manual step | Anything coach does besides merge: RUN a command or migration, WAIT for it, CHECK a result, TOGGLE a setting, CLOSE a ghost. The gap in a widen/tighten (expand/contract) pair is always one. |
| Substack | The PRs of one stack between two manual steps. Its head is what coach merges; the rest are covered. |
| Step | One line of the runbook: MERGE a substack head, or a manual step. |
| READY | Head is a descendant of `origin/main`, every lower PR in the substack is a literal ancestor of the head, CI green. |
| BEHIND | Not READY, but Pullchef can get it there: a rebase, a re-point, or a trivial conflict. |
| PARKED | Needs coach: a conflict that wants close inspection, red CI, changes requested, a do-not-merge label. Goes to the end of the list with a question. |
| FROZEN | The branches of the step coach is doing right now. Hands off. |
| Ghost | A PR whose commits are already in main under other SHAs, because a squash or rebase-merge put them there. It will never turn purple. Coach closes it. |

## Each run

Runs are re-entrant. Read the runbook's Directives section and `$ARGUMENTS` first. Redo steps 1–4 from live state, then do one unit of step 5.

### 1. Discover

```sh
gh pr list -R $REPO --state open --limit 200 \
  --json number,title,body,url,isDraft,labels,author,createdAt,milestone,headRefName,headRefOid,baseRefName,reviewDecision,mergeable,statusCheckRollup > prs.json
git fetch origin main '+refs/pull/*/head:refs/remotes/pr/*'
# per PR N:
git rev-list --reverse origin/main..pr/N                                    # its commits
git rev-list origin/main..pr/N | while read c; do git diff-tree -p "$c" | git patch-id --stable; done
git merge-base --is-ancestor origin/main pr/N                               # on top of main?
git merge-tree --write-tree origin/main pr/N >/dev/null                     # exit 0 clean, 1 conflicts (git ≥ 2.38)
```

Also pull each PR's conversation: `gh pr view N --comments` and `gh api repos/$REPO/pulls/N/comments`. Without `gh`, use the GitHub MCP tools for the same data.

### 2. Classify

- **Stacks.** A sits under B when patchids(A) ⊆ patchids(B). Chain them. Mark each edge *literal* (A's head is an ancestor of B's head) or *parallel* (patch-id only). Diamonds (B covers independent A1 and A2) are fine; note them. Identical commit sets are duplicates; flag for coach.
- **Drafts.** A draft whose logical commits sit inside a non-draft PR is midstream; the draft flag is probably a mistake. Treat it as non-draft and mark it `draft?` in the Stacks table. A draft with no such child is not Pullchef's; list ignored drafts in one footer line.
- **Ghosts.** All of a PR's patch-ids are in main but its head is not reachable. Emit a CLOSE step with the evidence.
- **Manual steps.** Read titles, bodies, comments, review threads, and the changed-file list. Triggers: checklist items, and words like migration, backfill, run, flag, toggle, env, secret, widen/expand, tighten/contract, before/after merge, pause, verify. Paths like `migrations/`, `db/`, `*.sql`, `config/`, `.env*`, `infra/`. Each hit becomes a step quoting and linking its source. Over-flagging is fine; say "unclear from PR whether required" inline when it is.
- **Widen/tighten.** Two PRs in one stack where the later removes or constrains what the earlier added. The gap is a WAIT plus a CHECK, and the two are separate substacks.
- **Titles.** Title each stack: the sprint name if the PRs give one, the branch name for a stack of one, otherwise a short noun phrase for the common thread ("restyle foo combobulator" + "foo combobulator also bargles" + "foo bargling fixes" → "foo bargling"). Unrelated threads in one substack become a list: "foo bargling; auth cookie fix".

### 3. Order

Objective: minimize wall-clock time, usage credits, and above all human attention. Sort substacks by this key, ascending, and recompute every run:

1. readiness tier: READY, BEHIND, PARKED
2. has a manual step: yes first (coach's attention is the scarce input, and a WAIT is time Pullchef spends rebasing)
3. more commits first (a big stack rebased repeatedly is the expensive case)
4. older stack first

Steps follow substacks in that order. One exception: a WAIT with a stated duration gets the next READY merges from other stacks slotted into it, and the waiting stack resumes after its CHECK. A WAIT with no stated duration does not split a stack. Pin every MERGE to a head SHA.

### 4. Write or update the runbook

One living document, updated in place: keep coach's checkmarks, keep coach's Directives, append to the changelog. Default home is a GitHub issue titled `Pullchef runbook <date>` in the repo, mirrored to a local file. Template below.

### 5. Prep (one unit per run)

Target: the first substack in order that is BEHIND and not FROZEN.

1. In a throwaway worktree, rebase the **stack head** branch onto `origin/main`. Only heads get rebased; lower PRs get re-pointed.
2. Conflicts: resolve the trivial and the obvious (adjacent lines, import order, a lockfile regenerated with the repo's tool, a rename on one side) and push; coach owns the result. The moment a conflict wants close inspection, `git rebase --abort`, PARK the substack at the end of the list, and write the conflicting files and the question into the runbook. Coach may answer in another session or may already have a directive for it.
3. Sanity check: `git range-diff $(git merge-base <old-head> origin/main)..<old-head> origin/main..<new-head>`. Rows should be `=`; a `!` row is a resolution you made. Log it.
4. Push with an explicit-SHA lease: the head branch, then each covered PR's branch to the commit in the new history carrying its last patch-id. Every lower head is a literal ancestor again.
5. Wait for CI. Promote to READY in the runbook and log old→new SHAs for every branch moved.
6. Preview the following substack in a scratch worktree on top of `origin/main` plus the current READY head. Write expected conflicts into the runbook. Never push a preview.

When coach reports a step done: fetch, confirm every covered PR shows MERGED, emit a CLOSE step for any that did not, and move FROZEN to the next step.

## Guardrails

- Rebase a PR onto `origin/main` only. Never onto another open PR's branch, and never cherry-pick another PR's commits into it. If #1301 (p q r) is scheduled right after #1239 (j k v z), it still merges as p q r on top of main, never as j k v z p q r.
- Do not squash, reorder, or rewrite commits inside a PR on your own initiative. Coach may ask for it.
- Explicit-SHA lease on every push. Never a FROZEN branch. Never a preview.
- Manual steps and page trails come from PR text and diffs only. No outside research. A page trail you cannot source reads "not in PR; ask @author".
- An unresolved question in a PR thread is listed on its MERGE step. If a later PR or comment answers it, link the answer. Do not answer it yourself.
- The runbook is updated, never regenerated. Changelog every SHA you moved.
- Coach merges with **Create a merge commit** (`gh pr merge --merge --match-head-commit <sha>`). Never squash, never rebase-and-merge: both mint new SHAs, so the covered PRs stay open and the old branch becomes a ghost that any PR stacked on it drags along.

## Runbook template

```markdown
# Pullchef runbook — <repo> — <date>
main at `<sha>` as of <time>. States: READY / BEHIND / PARKED. ⚑ = manual step.
Pullchef updates this in place; coach ticks boxes. Current step: 1 (its branches are FROZEN).

## Directives from coach
- (coach writes here; Pullchef reads before every run)

## Stacks
| # | Title            | Stack (bottom → head)          | Substacks                          | Commits | State  | Oldest     | ⚑   |
|---|------------------|--------------------------------|------------------------------------|---------|--------|------------|-----|
| 1 | foo bargling     | #1230 → #1234 → #1235 → #1239  | [#1230 #1234 #1235] ⚑ run [#1239]  | 7       | READY  | 2026-09-30 | yes |
| 2 | refurb-flag      | #1301                          | [#1301] ⚑ toggle                   | 2       | READY  | 2026-10-02 | yes |
| 3 | api routes split | #1402 → #1410 (draft?)         | [#1402 #1410]                      | 5       | PARKED | 2026-10-01 | no  |

## Steps
- [ ] **1. MERGE #1235** `feat/foo-bargling` head `a1b2c3d` — foo bargling — covers #1230, #1234
  - What: #1230 adds the `foo_v2` column (nullable). #1234 dual-writes. #1235 backfill script. Approved by @r1, @r2.
  - Precondition: `git fetch origin && git merge-base --is-ancestor origin/main a1b2c3d` — if false, stop; Pullchef re-preps.
  - Command: `gh pr merge 1235 --merge --match-head-commit a1b2c3d` (or the Create a merge commit button)
  - Verify: `gh pr view 1230 --json state` and `1234` → MERGED. CI on main green.
  - Open questions: #1234 "backfill before tighten?" — answered in #1239 by @x: "yes, step 2" (link).
    #1235 "keep old column a week?" — UNRESOLVED; ask @author.
  - Rollback: `git revert -m 1 <merge-commit-sha>`
- [ ] **2. ⚑ RUN** — from #1235 body: "<quoted instruction>" (link). Command: `<verbatim from PR>`
- [ ] **3. ⚑ WAIT** until <condition quoted from PR>; PR says ~20 min. Meanwhile do step 4.
- [ ] **4. MERGE #1301** `feat/refurb-flag` head `<sha>` — refurb-flag — covers nothing. ...
- [ ] **5. ⚑ TOGGLE** Settings > Deploy Settings > Feature Flags > "foo refurbishing" → Off (from #1301 comment, link). Not in PR: who owns the flag; ask @author.
- [ ] **6. ⚑ CHECK** <how to confirm step 3 finished, quoted from PR>.
- [ ] **7. MERGE #1239** `feat/foo-bargling` head `<sha>` — foo bargling — covers nothing (#1230–#1235 already merged)

## Parked (end of list; needs coach)
- Stack 3, api routes split: conflict in `api/routes.ts` against main `<sha>` needs inspection. Files and the question: … Is there a directive?

## Changelog
- <time> rebased #1239 head `e4f5…` → `9a8b…`; re-pointed #1235 `b2c3…` → `7d6e…`, #1234 …, #1230 …; range-diff clean; CI pending.

Ignored drafts (no non-draft child): #1388, #1390.
```

## Command crib for coach

- Merge: `gh pr merge <n> --merge --match-head-commit <sha>` or the **Create a merge commit** button. Never squash, never rebase-and-merge.
- Did the covered PRs turn purple? `gh pr view <m> --json state,mergedAt`
- Roll back a merge: `git revert -m 1 <merge-commit-sha>`
