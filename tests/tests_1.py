# import os
import time
import pytest
from crop_bars_on_screenshots.crop_2 import *

# @pytest.mark.xfail
def test_get_dest_folder():
    init_folder = "tests/Example_folder"
    expected_folder_name = f"{init_folder}_edited"
    expected_folder_path = f"{os.getcwd()}/{init_folder}_edited"
    # 1. Check if destination folder's name = folderName_cropped
    assert create_dest_folder(init_folder) == expected_folder_name, "[TEST INFO] Name of the created folder is incorrect"
    # 2. Check if destination folder is created indeed
    assert os.path.exists(expected_folder_path), "[TEST INFO] Folder does not exist"
    # 3. Check that there is no FileExistsError when creating already existing folder
    try:
        create_dest_folder(init_folder)
    except FileExistsError:
        assert False, "[TEST INFO] Error occurs when creating already existing folder"
    os.rmdir(expected_folder_path)


def test_get_file_name_and_ext(fake_file):
    assert get_file_name_and_ext(fake_file['goodfile']) == ("goodname", "py")
    with pytest.raises(TypeError):
        get_file_name_and_ext(fake_file['badfile_1'])
        get_file_name_and_ext(fake_file['badfile_2'])
        get_file_name_and_ext(fake_file['badfile_3'])

def test_crop_image(example_screenshot):
    img = example_screenshot
    width_ex, height_ex = img.size
    width_cropped = width_ex
    height_cropped = height_ex - (170 + 210)
    img_cropped = crop_image(example_screenshot)

    assert width_cropped, height_cropped == img_cropped.size
