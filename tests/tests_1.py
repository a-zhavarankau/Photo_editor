# import os
import time
import pytest
from crop_bars_on_screenshots.crop_bars_on_screenshots import *

# @pytest.mark.xfail
def test_get_dest_folder():
    folder = "tests/Example_folder"
    expected_folder_name = f"{folder}_cropped"
    expected_folder_path = f"{os.getcwd()}/{folder}_cropped"
    # 1. Check if destination folder's name = folderName_cropped
    assert get_dest_folder(folder) == expected_folder_name, "Name of the created folder is incorrect"
    # 2. Check if destination folder is created indeed
    assert os.path.exists(expected_folder_path), "Folder does not exist"
    # 3. Check that there is no FileExistsError when creating already existing folder
    try:
        get_dest_folder(folder)
    except FileExistsError:
        assert False, "Error occurs when creating already existing folder"
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
