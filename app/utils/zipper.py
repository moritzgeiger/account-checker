import os
import zipfile
import io


def zipper(
    zip_filename,
    debug=False,
    source_path=None,
    ):

    """Loads .html and .xlsx files from designated source path into zipfile.
    Returns:
        if debug:
            output zipfile name
        else:
            io.BytesIO file of zipfile
    """
    local_destinations = []
    for file in os.listdir(source_path):
        if any([x in file.lower() for x in ['.pdf', '.xlsx']]):
            local_destinations.append(file)

    if debug:
        s = f'final/{zip_filename}'
    else:
        s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in local_destinations:
        full_path = os.path.join(source_path, fpath)
        zf.write(full_path, fpath)

    zf.close()

    return s
