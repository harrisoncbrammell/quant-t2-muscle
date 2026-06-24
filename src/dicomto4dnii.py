# dicomto4dnii.py
# Converts a folder of multi-echo DICOM files into a single 4D NIfTI + JSON sidecar.
# The fourth dimension of the NIfTI is echo time, as expected by DECAES.
#
# Requires: pip install dcm2niix
#
# Usage:
#   dicomto4dnii(dicom_dir, output_dir)             -> saves echo_time_series.nii.gz and echo_time_series.json
#   dicomto4dnii(dicom_dir, output_dir, "t2scan")   -> saves t2scan.nii.gz and t2scan.json
#
# Arguments:
#   dicom_dir  : folder containing one DICOM per echo time
#   output_dir : folder where output files will be saved
#   filename   : base name for output files, default "output" (no extension)

import subprocess
from pathlib import Path


def dicomto4dnii(dicom_dir, output_dir, filename="echo_time_series"):
    dicom_dir = Path(dicom_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            "dcm2niix",
            "-m", "y",            # merge all echoes into a single 4D NIfTI
            "-z", "y",            # compress output as .nii.gz
            "-f", filename,       # base output filename (no extension)
            "-o", str(output_dir),
            str(dicom_dir),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"dcm2niix failed:\n{result.stderr}")

    nii_path = output_dir / f"{filename}.nii.gz"
    json_path = output_dir / f"{filename}.json"

    if not nii_path.exists():
        raise FileNotFoundError(
            f"Expected output not found: {nii_path}\n"
            f"dcm2niix output:\n{result.stdout}"
        )

    print(f"Saved: {nii_path}")
    if json_path.exists():
        print(f"Saved: {json_path}")

    return nii_path, json_path
