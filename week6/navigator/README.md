# ATT&CK Navigator layer

`week6_execution_layer.json` selects **T1059.006 — Python** as an emulated laboratory procedure. It is not a detection coverage layer. The file does not import ATLAS IDs into an Enterprise matrix.

Open [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/), choose **Open Existing Layer**, then **Upload from local**, and select this JSON file. Read the technique comment before taking a screenshot. Interface labels may differ across versions.

The JSON uses [layer format 4.5](https://github.com/mitre-attack/attack-navigator/blob/master/layers/spec/v4.5/layerformat.md). It was checked structurally during packaging; no successful browser import or rendered Navigator screenshot is claimed.

T1048.003 is deliberately not highlighted: the local dummy-data transfer is a related analogy, not evidence of complete non-C2 exfiltration. See `docs/mitre_mapping.md`.
