# process_nii_decaes.py
# Runs DECAES T2 mapping on a 4D NIfTI produced by dicomto4dnii.
# TE and T2Range are read automatically from the scan's JSON sidecar.
# All other settings are in settings.txt in the project root.
#
# Requires: pip install juliacall juliapkg
#
# Usage:
#   process_nii_decaes("scan.nii.gz", "output/patient1")

import json
from pathlib import Path
SETTINGS_FILE = Path(__file__).parent / "settings.txt"


def process_nii_decaes(nii_path, output_dir):
    from juliacall import Main as jl
    jl.seval("using DECAES")

    nii_path = Path(nii_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # read TE from the JSON sidecar produced by dicomto4dnii
    meta = json.loads(nii_path.with_suffix("").with_suffix(".json").read_text())
    te = meta["EchoTime"]
    if isinstance(te, list):
        te = te[0]  # equally spaced echoes, so first value is the echo spacing

    # load researcher-editable settings, skipping blank lines and comments
    settings_args = [
        line.strip() for line in SETTINGS_FILE.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]

    # TODO: add optional mask argument (--mask <path>) to skip background voxels and speed up processing
    # TODO: add --T2dist flag (or make it a parameter) to optionally output the full T2 distribution spectrum alongside the map
    jl.DECAES.main([
        str(nii_path),
        "--T2map",
        "--TE",     str(te),
        *settings_args,
        "--output", str(output_dir),
    ])
