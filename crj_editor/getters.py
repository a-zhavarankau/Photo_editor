import os
from typing import Tuple
from PIL import Image
from editors import change_size_format_pretty


def create_out_folder(in_folder: str) -> str:
    """Create output folder named as initial folder + '_edited'
       to save edited files
    """
    out_folder = in_folder + "_edited"
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    return out_folder


def get_folder_size(folder_path: str) -> int:
    folder_size = 0
    for path, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(path, file)
            folder_size += os.path.getsize(file_path)
    return folder_size


def get_folder_info(folder_path: str) -> dict[str: list | int]:
    all_entities = os.scandir(folder_path)
    all_entities_list = list(all_entities)
    all_entities_amount = len(all_entities_list)
    folder_size = get_folder_size(folder_path)
    return {"all_entities_list": all_entities_list,
            "all_entities_amount": all_entities_amount,
            "folder_size": folder_size}


def get_name_ext(img: Image) -> Tuple[str, str]:
    """ Get file name and extension.
    """
    spl_name = img.filename.split("/")[-1]
    img_name, img_ext = os.path.splitext(spl_name)[0], os.path.splitext(spl_name)[1].lstrip(".")
    return img_name, img_ext


def get_img_data(img: Image, folder: str) -> Tuple[str | Tuple[int, int]]:
    """ Return tuple of image data for some functions and reports.
        Parameter 'folder' takes value of input or output folder regarding
        with its purpose.
    """
    name, ext = get_name_ext(img)
    res, format_, mode = img.size, img.format, img.mode
    file_path = os.path.join(folder, f'{name}.{ext}')
    size = change_size_format_pretty(os.path.getsize(file_path))

    in_img_data = name, ext, res, size, format_, mode
    return in_img_data
