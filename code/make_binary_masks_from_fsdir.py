import os

def make_binary_masks_from_fsdir(freesurfer_subject_folder, freesurfer_environment_path, fsl_environment_path, output_path, threshold_brain=50, threshold_white=50):
    
    # Load white matter, brain and rawavg 
    brain_mask = os.path.join(freesurfer_subject_folder, 'mri', 'brainmask.mgz')    
    white_matter_segment = os.path.join(freesurfer_subject_folder, 'mri', 'wm.seg.mgz')
    raw_avg = os.path.join(freesurfer_subject_folder, 'mri', 'rawavg.mgz')
    
    # Convert them to nifti
    converted_brain_destination = os.path.join(output_path, 'convertedBrain.nii.gz')
    converted_white_destination = os.path.join(output_path, 'convertedWhite.nii.gz')    
    converted_raw_avg_destination = os.path.join(output_path, 'convertedRawavg.nii.gz')    
    convert_brain = '%s %s %s' % (os.path.join(freesurfer_environment_path, 'mri_convert'),
                                  brain_mask, converted_brain_destination)
    convert_white = '%s %s %s' % (os.path.join(freesurfer_environment_path, 'mri_convert'),
                                  white_matter_segment, converted_white_destination)
    convert_raw = '%s %s %s' % (os.path.join(freesurfer_environment_path, 'mri_convert'),
                                raw_avg, converted_raw_avg_destination)   
    os.system(convert_brain + ';' + convert_white + ';' + convert_raw)
    
    # Register white and brain to rawavg
    registered_brain_destination = os.path.join(output_path, 'brainRegistered.nii.gz')
    registered_white_destination = os.path.join(output_path, 'whiteRegistered.nii.gz')
    registration_command_brain = '%s -in %s -ref %s -dof 6 -out %s -v' % (os.path.join(fsl_environment_path, 'flirt'), 
                                                                       converted_brain_destination, 
                                                                       converted_raw_avg_destination, registered_brain_destination)
    registration_command_brain = '%s -in %s -ref %s -dof 6 -out %s -v' % (os.path.join(fsl_environment_path, 'flirt'), 
                                                                       converted_white_destination, 
                                                                       converted_raw_avg_destination, registered_white_destination)
    os.system(registration_command_brain + ';' + registration_command_white)
    
    # Binarize the masks 
    binary_brain_mask = os.path.join(output_path, 'binaryBrainMask.nii.gz')
    binary_white_mask = os.path.join(output_path, 'binaryWhiteMask.nii.gz')
    binarize_brain_command = '%s %s -thr %s -bin %s' % (os.path.join(fsl_environment_path, 'fslmaths'),
                                                        registered_brain_destination, threshold_brain,
                                                        binary_brain_mask)
    binarize_white_command = '%s %s -thr %s -bin %s' % (os.path.join(fsl_environment_path, 'fslmaths'),
                                                        registered_white_destination, threshold_white,
                                                        binary_white_mask)    
    os.system(binarize_brain_command + ';' + binarize_white_command)
    
    return (binary_brain_mask, binary_white_mask)