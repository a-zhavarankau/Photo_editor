import os
import pillow_heif
from PIL import Image, UnidentifiedImageError
from typing import Any
from working_files.constants import *


def check_is_file(item: Any) -> bool:
    return os.path.isfile(item)


def check_is_img_and_get_img(file_path: str) -> any:
    """Check if the file is a proper image, and return image file.
    """
    try:
        pillow_heif.register_heif_opener()
        img = Image.open(file_path)
    except UnidentifiedImageError:
        return False

    return img


def check_is_screenshot(img: Image) -> bool:
    """ Check if the image is a MacBook Pro A1398 screenshot.
        If true, then upper and lower bars will be cropped.
    """
    width, height = img.size
    return ((width, height) == (SCREEN_WIDTH, SCREEN_HEIGHT)) \
           and img.format.lower() == 'png'


def check_img_bigger_than_default(img: Image) -> bool:
    """ Check if the image bigger than default size.
        Default values are in the 'constants.py'.
    """
    width, height = img.size
    return width > DEFAULT_WIDTH or height > SCREEN_HEIGHT
