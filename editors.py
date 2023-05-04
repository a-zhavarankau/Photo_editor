from PIL import Image
from working_files.constants import *


def crop_bars(img: Image) -> Image:
    """ Crop upper and lower bars from a screenshot from MacBook Pro A1398.
    """
    # Coordinates of the rectangular image that will survive after cropping
    left = 0
    top = DEFAULT_SCR_TOP_OFFSET
    right = SCREEN_WIDTH
    bottom = SCREEN_HEIGHT - DEFAULT_SCR_BOTTOM_OFFSET

    img_cropped = img.crop((left, top, right, bottom))
    # Function show() is used to show cropped image (visual check of the result)
    # image_cropped.show()
    return img_cropped


def resize_img_to_default(img: Image) -> Image:
    """Check if image vertical rectangular and resize it with default height;
       else image is horizontal rectangular and resize it with default width.
    """
    width, height = img.size
    if height > width:
        # If image is vertical rectangular, resize image.height = SCREEN_HEIGHT, image.width -> respectively
        resized_height = SCREEN_HEIGHT
        resized_width = int(width * resized_height / height)
    else:
        # If image is horizontal rectangular, resize image.wib  dth = FINAL_WIDTH, image.height -> respectively
        resized_width = DEFAULT_WIDTH
        resized_height = int(height * resized_width / width)

    resized_img = img.resize((resized_width, resized_height))
    return resized_img


def change_size_format(size: int, factor: int=1024, suffix: str= "B") -> str:
    """ Scale bytes to its proper byte format, e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G"]:
        if size < factor:
            return f"{size:.0f}{unit}{suffix}"
        size /= factor
