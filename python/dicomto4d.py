# Loads a folder of 3D DICOM files and stacks them into a 4D array
# Saves output as both a .mat and .nii.gz file
# Author: Charles Brammell
#
# Usage:
#   dicomto4d("path/to/dicoms", "output")
#   -> saves output.mat and output.nii.gz
#
#   dicomto4d("path/to/dicoms", "output", order=[2, 0, 1])
#   -> reorders files before stacking

import re
import numpy as np
import pydicom
import scipy.io
import nibabel as nib
from pathlib import Path


def dicomto4d(path, output_path, order=None):
    # sort .dcm files numerically by filename
    path = Path(path)
    output_path = Path(output_path)
    files = sorted(path.glob("*.dcm"), key=lambda f: int(re.search(r"\d+", f.stem).group()))

    # reorder files if a custom order is provided
    if order is not None:
        files = [files[i] for i in order]

    # build 4D array: (x, y, z, num_files)
    first = pydicom.dcmread(files[0]).pixel_array.astype(float)
    data = np.zeros((*first.shape, len(files)))

    for i, f in enumerate(files):
        data[..., i] = pydicom.dcmread(f).pixel_array.astype(float)

    # save as .mat and .nii.gz
    scipy.io.savemat(output_path.with_suffix(".mat"), {"data": data})
    nib.save(nib.Nifti1Image(data, affine=np.eye(4)), output_path.with_suffix(".nii.gz"))
