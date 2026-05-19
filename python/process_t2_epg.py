# process_t2_epg.py
# Loops over patient folders, converts DICOM scans to NIfTI using dicomto4d,
# then runs DECAES T2 mapping on each scan using settings from settings.txt.
# Author: Charles Brammell
#
# Expected data directory structure:
#   data_dir/
#     Patient1/
#       scan1/   (contains *.dcm files)
#       scan2/   (contains *.dcm files)
#     Patient2/
#       scan1/
#       scan2/

from pathlib import Path
from dicomto4d import dicomto4d
import decaes_pyjulia as decaes

# --- Parameters (edit these) ---
data_dir      = Path("data")
output_dir    = Path("output")
settings_file = Path("settings.txt")

# read settings.txt into a list of argument strings
settings_args = [line.strip() for line in settings_file.read_text().splitlines() if line.strip()]

# initialize Julia and DECAES once before the loop
decaes.initialize()

# --- Process each patient ---
for patient_path in sorted(data_dir.iterdir()):
    if not patient_path.is_dir():
        continue
    print(f"Processing patient: {patient_path.name}")

    # find scan subfolders
    for scan_path in sorted(patient_path.iterdir()):
        if not scan_path.is_dir():
            continue
        print(f"  Scan: {scan_path.name}")

        # create output folder for this scan
        scan_out_dir = output_dir / patient_path.name / scan_path.name
        scan_out_dir.mkdir(parents=True, exist_ok=True)
        nii_path = scan_out_dir / "image"

        # convert DICOMs to .mat and .nii.gz
        dicomto4d(str(scan_path), str(nii_path))

        # run DECAES via Julia using settings from settings.txt
        decaes.DECAES.main([str(nii_path) + ".nii.gz"] + settings_args + ["--output", str(scan_out_dir)])

        print(f"  Done -> {scan_out_dir}")

print("All patients processed.")
