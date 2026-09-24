# Original source images

The main report displays **five authentic figures from the original publications**: three publisher/author screenshots, one published conceptual diagram, and one original two-panel empirical graph. No image was synthesized or redrawn for this increment.

## Current delivery

Images are embedded by their original HTTPS URLs in `../README.md`. They therefore display online without running code, subject to the original hosts and the viewer's network access. **The initial ZIP does not contain PNG binaries.** Direct image downloads were unavailable in the preparation environment, so no local-image checksum or download success is fabricated.

The [manifest](manifest.json) records provenance, original figure numbers, captions, and rights information. Caption numbers W2-1 through W2-5 are local report numbers; original publication figure numbers remain in every caption.

## Optional local preservation

Run from the repository root on a machine with internet access:

```bash
python week2/scripts/fetch_images.py --localize
```

The helper requests only the five exact image URLs in the manifest, validates the PNG signature and a conservative size limit, and records SHA-256 values for actual downloads. It rewrites remote image links to relative local links **only after every image is available**. It never requests the suspect repositories, IPs, domains, model files, or packages in the observable dataset.

Then rerun the local validator and commit the resulting images, receipt, and README change:

```bash
python week2/scripts/validate_dataset.py
git add week2/
git commit -m "docs(week2): preserve original source figures locally"
git push
```

Do not claim that this optional step was performed until it really succeeds. A successfully downloaded publisher-owned image still requires its original attribution and rights notice.
