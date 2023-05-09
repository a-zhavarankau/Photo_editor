import os
import time
import pytest
from crop_bars_on_screenshots.crop_2 import *


def test_create_dest_folder():
    init_folder = "Example_folder"
    expected_folder_name = f"{init_folder}_edited"
    expected_folder_path = f"{os.getcwd()}/{init_folder}_edited"
    # 1. Check if destination folder's name = folderName_edited
    assert create_dest_folder(init_folder) == expected_folder_name, "[TEST INFO] Name of the created folder is incorrect"
    # 2. Check if destination folder is created indeed
    assert os.path.exists(expected_folder_path), "[TEST INFO] Folder does not exist"
    # 3. Check that there is no FileExistsError when creating already existing folder
    try:
        create_dest_folder(init_folder)
    except FileExistsError:
        assert False, "[TEST INFO] Error occurs when creating already existing folder"
    os.rmdir(expected_folder_path)  # ???? >> Find out why it doesn't happen << ?????


