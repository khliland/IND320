#!/usr/bin/env bash
# Rebuilds the book locally (executing notebooks - requires Docker/API to be
# running) and pushes the resulting MyST execution cache to the
# refs/cache/execution-cache ref, so CI can reuse pre-executed outputs without
# needing local infrastructure. A custom ref (not refs/heads) is used so the
# cache doesn't show up as a branch or trigger GitHub's PR nudges.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE_REF="refs/cache/execution-cache"
WORKTREE_DIR="$(mktemp -d)"

cd "$REPO_ROOT/D2Dbook"
echo "Building book (this executes notebooks)..."
uv run --project "$REPO_ROOT" jupyter-book build --html

cd "$REPO_ROOT"

if git fetch origin "$CACHE_REF:$CACHE_REF" 2>/dev/null; then
  git worktree add --detach "$WORKTREE_DIR" "$CACHE_REF"
else
  git worktree add --detach "$WORKTREE_DIR"
  (cd "$WORKTREE_DIR" && git checkout --orphan cache-tmp && git rm -rf --quiet . >/dev/null 2>&1 || true)
fi

rm -rf "$WORKTREE_DIR/execute" "$WORKTREE_DIR/jupyter_execute"
cp -r "$REPO_ROOT/D2Dbook/_build/execute" "$WORKTREE_DIR/execute"
cp -r "$REPO_ROOT/D2Dbook/_build/jupyter_execute" "$WORKTREE_DIR/jupyter_execute"

cd "$WORKTREE_DIR"
git add -A
if git diff --cached --quiet; then
  echo "No changes to the execution cache."
else
  git commit -m "Update execution cache"
  git push origin "HEAD:$CACHE_REF"
  echo "Pushed updated execution cache to $CACHE_REF."
fi


cd "$REPO_ROOT"
git worktree remove "$WORKTREE_DIR" --force
