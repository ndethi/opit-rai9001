# Revert Instructions for Thesis Tags

## Available Tagged Versions

Run `git tag -l` to see all available tags:
- `v1.0-supervisor-submission` - Initial supervisor submission
- `v2.0-ready-for-review` - Ready for review version
- **`v2.1-supervisor-review-dec2025`** - Current: December 2025 supervisor review (Phase 1 complete)

## Quick Revert to This Version

If you need to revert to the December 2025 supervisor review version:

```bash
cd /home/ndethi/dev/opit-rai9001
git checkout v2.1-supervisor-review-dec2025
```

**Note**: This puts you in "detached HEAD" state (read-only). To make changes:

```bash
# Create a new branch from this tag
git checkout -b revision-from-dec2025-tag v2.1-supervisor-review-dec2025
```

## Revert Thesis Folder Only

If you only want to restore the thesis folder to this version:

```bash
cd /home/ndethi/dev/opit-rai9001
git checkout v2.1-supervisor-review-dec2025 -- docs/thesis/
git status  # See what changed
```

## Compare Current State with Tag

See what's different between current state and this tag:

```bash
git diff v2.1-supervisor-review-dec2025 docs/thesis/
```

## View Tag Details

```bash
git show v2.1-supervisor-review-dec2025
```

## Alternative: Use Backup Checkpoint

A filesystem backup also exists at:
```
docs/thesis-checkpoint-dec19-pre-annotator-revision/
```

To use this backup:
```bash
cd /home/ndethi/dev/opit-rai9001/docs
cp -r thesis/ thesis-backup-current/  # Save current state
rm -rf thesis/
cp -r thesis-checkpoint-dec19-pre-annotator-revision/ thesis/
```

## Push Tag to Remote (Optional)

If you want to push this tag to GitHub:

```bash
git push origin v2.1-supervisor-review-dec2025
```

Or push all tags:

```bash
git push origin --tags
```

---

**Tagged Commit**: cb581cc (current HEAD)  
**Created**: December 19, 2025  
**Purpose**: Supervisor review submission with Phase 1 revisions
