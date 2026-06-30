#!/usr/bin/env bash
# save-specialist — stage, commit, and push specialist folders to GitHub
#
# Usage:
#   save-specialist              → commits all new/modified specialists
#   save-specialist <name>       → commits one specific specialist
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

# ── helpers ──────────────────────────────────────────────────────────────────

die()  { echo "Error: $*" >&2; exit 1; }
info() { echo "  $*"; }

# Returns 0 (true) if no files in the dir are tracked by git yet
is_new() {
  [[ $(git ls-files "specialists/$1" | wc -l) -eq 0 ]]
}

# Collect specialist dirs that have uncommitted changes
detect_changed() {
  {
    # Untracked new dirs
    git ls-files --others --exclude-standard specialists/ 2>/dev/null \
      | grep -oP 'specialists/\K[^/]+' || true

    # Modified tracked files
    git diff --name-only HEAD -- specialists/ 2>/dev/null \
      | grep -oP 'specialists/\K[^/]+' || true

    # Already-staged files (if user ran git add manually)
    git diff --cached --name-only -- specialists/ 2>/dev/null \
      | grep -oP 'specialists/\K[^/]+' || true
  } | sort -u
}

# ── guards ────────────────────────────────────────────────────────────────────

git rev-parse --git-dir &>/dev/null || die "not a git repository"

# ── resolve target specialist(s) ─────────────────────────────────────────────

if [[ $# -gt 0 ]]; then
  TARGET="$1"
  [[ -d "specialists/$TARGET" ]] || die "specialists/$TARGET does not exist"
  NAMES=("$TARGET")
else
  mapfile -t NAMES < <(detect_changed)
  if [[ ${#NAMES[@]} -eq 0 ]]; then
    echo "Nothing to commit — no new or modified specialists found."
    exit 0
  fi
fi

# ── validate each specialist has the required files ───────────────────────────

echo ""
echo "Validating specialists..."
for name in "${NAMES[@]}"; do
  dir="specialists/$name"
  [[ -f "$dir/persona.md"    ]] || die "$dir/persona.md is missing — create it before committing"
  [[ -f "$dir/reference.md"  ]] || die "$dir/reference.md is missing — create it before committing"
  if is_new "$name"; then
    info "+ new      $name"
  else
    info "✎ updated  $name"
  fi
done

# ── confirmation ─────────────────────────────────────────────────────────────

echo ""
read -r -p "Commit and push these specialists? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

# ── stage ────────────────────────────────────────────────────────────────────

echo ""
for name in "${NAMES[@]}"; do
  git add "specialists/$name"
  info "staged  specialists/$name"
done

# ── build commit message ──────────────────────────────────────────────────────

if [[ ${#NAMES[@]} -eq 1 ]]; then
  name="${NAMES[0]}"
  if is_new "$name"; then
    verb="add"
    type="feat"
  else
    verb="update"
    type="docs"
  fi
  MSG="${type}(specialists): ${verb} ${name} specialist"
else
  joined=$(IFS=', '; echo "${NAMES[*]}")
  MSG="feat(specialists): add/update ${joined}"
fi

# ── commit ────────────────────────────────────────────────────────────────────

git commit -m "$(cat <<EOF
$MSG

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"

# ── push ─────────────────────────────────────────────────────────────────────

echo ""
echo "Pushing to origin/main..."
git push origin main

echo ""
echo "Done. Specialist(s) saved to GitHub."
