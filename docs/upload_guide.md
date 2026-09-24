# Uploading the Week 2 increment

The package is designed to be added beside your existing `week1` folder. It does not replace Week 1 or the repository's root README.

## Browser workflow

1. Extract the ZIP archive. The resulting folder should be named `week2` and contain `README.md`, `data`, `docs`, `evidence`, `images`, and `scripts`.
2. Open the root of your existing GitHub repository. Select **Add file → Upload files**.
3. Drag the complete **week2 folder** into the upload area. Confirm that the listed paths start with `week2/` and that the nested files are present. Do not upload the ZIP as a substitute for its contents.
4. Use the commit message `docs(week2): add sourced OSINT collection and evidence`, then complete **Commit changes**.
5. Open `week2/README.md` on GitHub. Check the source figures, tables, Mermaid map, and dataset links.

The GitHub browser upload workflow is described in the [official documentation](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository), accessed 2026-09-24. This guide is an instruction, not evidence that the upload has occurred.

The original figures load from external source URLs and require network access. Local binaries are not required for the initial online report. Optional preservation instructions are in [images/README.md](../images/README.md).

## Git workflow

Copy `week2` into the local clone, then run these commands from the repository root:

```bash
python week2/scripts/validate_dataset.py
git status
git add week2/
git diff --cached --stat
git commit -m "docs(week2): add sourced OSINT collection and evidence"
git push
```

Review the files before committing. Keep later corrections as genuine later commits; do not manufacture a past weekly history.

## Before the defense

Open the report once while online, review the four case boundaries and the observable types, and practice the [7-minute-30-second plan](defense.md). The sources' screenshots and experiments belong to their authors, so describe them that way. Actual GitHub history and oral defense must be supplied by the group.
