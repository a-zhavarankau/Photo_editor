# import os
import pytest
from crop_bars_on_screenshots.crop_bars_on_screenshots import *

# @pytest.mark.xfail
def test_get_dest_folder():
    folder = "tests/Example_folder"
    expected_folder_name = f"{folder}_cropped"
    expected_folder_path = f"{os.getcwd()}/{folder}_cropped"
    # 1. Check if destination folder's name == expected
    assert get_dest_folder(folder) == expected_folder_name, \
        "Name of the created folder is incorrect"
    # 2. Check if destination folder is created indeed
    assert os.path.exists(expected_folder_path), "Folder does not exist"
    # 3. Check that there is no FileExistsError when creating existing folder
    try:
        get_dest_folder(folder)
    except FileExistsError:
        assert False, "Error occurs when creating existing folder"

    os.rmdir(get_dest_folder(folder))


# def test_get_file_name_and_ext():
#
#     assert get_file_name_and_ext("4.34.ggg.jpg") == ("4.34.ggg", "jpg")
