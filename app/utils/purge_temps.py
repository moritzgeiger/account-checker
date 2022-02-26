import os
import glob
# from utils.gcs_hook import GCSConnector
import logging
import shutil


def purge_temps(debug=False):
    """Removes temporary files and zip directories from temp/ and final/ folder"""
    if debug:
        # don't rempve temp files
        pass
    else:
        folders = ['temp/']
        for folder in folders:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path) and 'gitkeep' not in file_path:
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    logging.warning('Failed to delete %s. Reason: %s' % (file_path, e))

