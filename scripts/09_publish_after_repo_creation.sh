#!/usr/bin/env bash
# Only after the OWNER has created an empty PUBLIC GitHub repository at the URL below.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
REMOTE='https://github.com/engasm89/RDK-X5-EdgeVision-Ignite-2026.git'
command -v git >/dev/null || { echo 'git required' >&2; exit 1; }
if [[ ! -d .git ]]; then
  git init -b main
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "$REMOTE"
elif [[ "$(git remote get-url origin)" != "$REMOTE" ]]; then
  echo 'Existing origin does not match expected repo; refusing to overwrite remote.' >&2; exit 2
fi
if [[ -n "$(git status --porcelain)" ]]; then
  git add .
  git commit -m 'Prepare RDK X5 EdgeVision Stage 1 challenge package'
fi
git push -u origin HEAD:main
printf 'Verify public repository and README: https://github.com/engasm89/RDK-X5-EdgeVision-Ignite-2026\n'
