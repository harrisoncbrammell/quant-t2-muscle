# run_t2_pipeline.py
# Converts a folder of multi-echo DICOMs into a T2 map using DECAES.
#
# Usage:
#   run_t2_pipeline("path/to/dicoms", "path/to/output")

from .src.dicomto4dnii import dicomto4dnii
from .src.process_nii_decaes import process_nii_decaes


def run_t2_pipeline(dicom_dir, output_dir):
    nii_path, _ = dicomto4dnii(dicom_dir, output_dir)
    process_nii_decaes(nii_path, output_dir)
