% process_t2_epg.m
% Loops over patient folders, converts DICOM scans to NIfTI using dicomto4d,
% then runs DECAES T2 mapping on each scan.
% Author: Charles Brammell
%
% Expected data directory structure:
%   data_dir/
%     Patient1/
%       scan1/   (contains *.dcm files)
%       scan2/   (contains *.dcm files)
%     Patient2/
%       scan1/
%       scan2/

%% --- Parameters (edit these) ---
data_dir     = 'data';          % root folder containing patient subfolders
output_dir   = 'output';        % where results will be saved
settings_file = 'settings.txt'; % DECAES settings file

% read settings.txt into a cell array of argument strings
settings_args = strtrim(splitlines(fileread(settings_file)))';
settings_args = settings_args(~cellfun('isempty', settings_args));

%% --- Process each patient ---
patients = dir(data_dir);
patients = patients([patients.isdir] & ~startsWith({patients.name}, '.'));

for p = 1:length(patients)
    patient_name = patients(p).name;
    patient_path = fullfile(data_dir, patient_name);
    fprintf('Processing patient: %s\n', patient_name);

    % find the two scan subfolders
    scans = dir(patient_path);
    scans = scans([scans.isdir] & ~startsWith({scans.name}, '.'));

    for s = 1:length(scans)
        scan_name = scans(s).name;
        scan_path = fullfile(patient_path, scan_name);
        fprintf('  Scan: %s\n', scan_name);

        % output paths for this scan
        scan_out_dir = fullfile(output_dir, patient_name, scan_name);
        if ~exist(scan_out_dir, 'dir')
            mkdir(scan_out_dir);
        end
        nii_path = fullfile(scan_out_dir, 'image');

        % convert DICOMs to .mat and .nii.gz using dicomto4d
        dicomto4d(scan_path, nii_path);

        % run DECAES T2 mapping on the NIfTI file using settings from settings.txt
        decaes([nii_path '.nii.gz'], settings_args{:}, '--output', scan_out_dir);

        fprintf('  Done -> %s\n', scan_out_dir);
    end
end

fprintf('All patients processed.\n');
