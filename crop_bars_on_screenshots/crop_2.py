import os
from PIL import Image, UnidentifiedImageError
import pillow_heif
from constants import *


def create_dest_folder(init_folder: str) -> str:
    """Create destination folder named as initial folder + '_edited' """
    dest_folder = init_folder + "_edited"
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    #
    # try:
    #     os.mkdir(dest_folder)
    # except FileExistsError:
    #     pass
    return dest_folder


def get_all_from_init_folder(init_folder: str) -> dict[str: list | int]:
    all_entities = os.scandir(init_folder)
    all_entities_list = list(all_entities)
    all_entities_amount = len(all_entities_list)
    return {"all_entities_list": all_entities_list, "all_entities_amount": all_entities_amount}


def check_is_not_file(item: any) -> bool:
    return not os.path.isfile(item)


def get_file_name_and_ext(file: any) -> tuple[str] or False:
    file_name = '.'.join(file.name.split('.')[:-1])
    file_ext = file.name.split('.')[-1]
    if not all((file_name, file_ext)):
        return False
    return file_name, file_ext


def check_is_img_and_get_img(file_path: str, file_ext: str) -> any:
    """Check if the file is a proper image"""
    if file_ext.lower() in ['bmp', 'jpeg', 'jpg', 'png']:
        image = Image.open(file_path)
        return image
    raise AttributeError(f"unknown extension to process: \'{file_ext}\'")


def check_is_screenshot(width: int, height: int, file_ext: str) -> bool:
    return ((width, height) == (SCREEN_WIDTH, SCREEN_HEIGHT)) \
           and file_ext.lower() == 'png'


def crop_bars(image: Image) -> Image:
    # Coordinates of the rectangular image that will survive after cropping
    left = 0
    top = 210
    right = SCREEN_WIDTH
    bottom = SCREEN_HEIGHT - 170

    image_cropped = image.crop((left, top, right, bottom))
    # Command below is used to show cropped image (visual check of the result)
    # image_cropped.show()
    return image_cropped


def check_img_bigger_than_default(width: int, height: int) -> bool:
    return width > OUT_WIDTH or height > SCREEN_HEIGHT


def resize_img_to_default(image: Image, width: int, height: int) -> Image:
    """Check if image vertical rectangular and resize it with height=1800;
       else image is horizontal rectangular and resize it with width=2400"""
    if height > width:
        # If image is vertical rectangular, resize image.height = SCREEN_HEIGHT, image.width -> respectively
        resized_height = SCREEN_HEIGHT
        resized_width = int(width * resized_height / height)
    else:
        # If image is horizontal rectangular, resize image.width = FINAL_WIDTH, image.height -> respectively
        resized_width = OUT_WIDTH
        resized_height = int(height * resized_width / width)
    resized_img = image.resize((resized_width, resized_height))
    return resized_img


def save_img_to_dest_folder(image: Image, dest_folder_name: str, file_name: str, file_ext: str) -> None:
    pillow_heif.register_heif_opener()
    image.save(f"{dest_folder_name}/{file_name}.{file_ext}")
    return image


def main_thread(init_folder: str):
    dest_folder_path = create_dest_folder(init_folder)
    all_entities_list = get_all_from_init_folder(init_folder)["all_entities_list"]
    all_entities_amount = get_all_from_init_folder(init_folder)["all_entities_amount"]
    count = count_processed = 1
    for item in all_entities_list:
        start_good_msg = f"[INFO] {count} of {all_entities_amount}:"
        start_err_mgs = f"[INFO] {count} of {all_entities_amount}: Not processed"
        if check_is_not_file(item):
            print(f"{start_err_mgs} (entity is not a file: \'{item.name}\')")
            count += 1
            continue
        file = item
        try:
            file_name, file_ext = get_file_name_and_ext(file)
        except TypeError:
            print(f"{start_err_mgs} (wrong name or extension in the file: \'{file.name}\')")
            count += 1
            continue
        file_path = f"{init_folder}/{file.name}"
        try:
            image = check_is_img_and_get_img(file_path, file_ext)
            width, height = image.size
        except (AttributeError, UnidentifiedImageError) as err:
            print(f"{start_err_mgs} (file is not a proper image: "
                  f"\'{file.name}\' ({err}))")
            count += 1
            continue
        if check_is_screenshot(width, height, file_ext):
            image = crop_bars(image)
        if check_img_bigger_than_default(width, height):
            image = resize_img_to_default(image, width, height)
        save_img_to_dest_folder(image, dest_folder_path, file_name, file_ext)
        print(f"{start_good_msg} File is ready")
        count += 1
        count_processed += 1

    dest_folder_images_amount = \
        get_all_from_init_folder(dest_folder_path)["all_entities_amount"]
    if dest_folder_images_amount:
        print(f"[Finish]\n"
              f"\t\tSource folder:                            {init_folder}\n"
              f"\t\tFiles in source folder:                   {count - 1}\n"
              f"\t\tDestination folder:                       {dest_folder_path:}\n"
              f"\t\tSuccessfully processed and saved images:  {count_processed - 1}\n")
    else:
        print(f"[Finish]\n"
              f"No images were processed. "
              f"Destination folder {dest_folder_path} will be deleted")
        os.rmdir(dest_folder_path)


if __name__ == "__main__":
    init_folder = "/Users/Sasha/Documents/21"
    main_thread(init_folder)

