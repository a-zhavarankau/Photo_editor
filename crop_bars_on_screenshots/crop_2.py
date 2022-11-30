import os
from PIL import Image, UnidentifiedImageError
from working_files.constants import *
# from typing import Any


def create_dest_folder(init_folder: str) -> str:
    dest_folder = init_folder + "_cropped"
    try:
        os.mkdir(dest_folder)
    except FileExistsError:
        pass
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


def check_is_img(file_path: str, file_ext: str) -> any:
    if file_ext in ['bmp', 'jpeg', 'jpg', 'png']:
        image = Image.open(file_path)
        return image
    raise AttributeError(f"unknown extension to handle: \'{file_ext}\'")


def check_is_screenshot(width: int, height: int, file_ext: str) -> bool:
    return ((width, height) == (SCREEN_WIDTH, SCREEN_HEIGHT)) and file_ext.lower() == 'png'


def crop_bars(image: Image):
    left = 0  # Coordinates of the rectangular image that will survive after cropping
    top = 210
    right = SCREEN_WIDTH
    bottom = SCREEN_HEIGHT - 170

    image_cropped = image.crop((left, top, right, bottom))
    # img_cropped.show()    # Show cropped image in the image viewer (to check the result)
    return image_cropped


def img_bigger_than_default(width: int, height: int):
    return width > DEFAULT_WIDTH or height > SCREEN_HEIGHT


def resize_img(image: Image, width: int, height: int):
    if height > width:
        # If image is vertical rectangular, resize image.height = SCREEN_HEIGHT, image.width -> respectively
        resized_height = SCREEN_HEIGHT
        resized_width = int(width * resized_height / height)
    else:
        # If image is horizontal rectangular, resize image.width = FINAL_WIDTH, image.height -> respectively
        resized_width = DEFAULT_WIDTH
        resized_height = int(height * resized_width / width)
    resized_img = image.resize((resized_width, resized_height))
    return resized_img


def save_img(image: Image, dest_folder_name, file_name, file_ext, count):
    image.save(f"{dest_folder_name}/{file_name}.{file_ext}")  # Edited file name == source file name
    # img_edited.save(f"{dest_folder_name}/{count}.{file_ext}")     # Edited file name == count


def main_thread(init_folder: str):
    dest_folder_path = create_dest_folder(init_folder)
    all_entities_list = get_all_from_init_folder(init_folder)["all_entities_list"]
    all_entities_amount = get_all_from_init_folder(init_folder)["all_entities_amount"]
    count = count_handled = 1
    for item in all_entities_list:
        start_good_msg = f"[INFO] {count} of {all_entities_amount}:"
        start_err_mgs = f"[INFO] {count} of {all_entities_amount}: Not processed "
        if check_is_not_file(item):
            print(f"{start_err_mgs} (entity is not a file: \'{item.name}\')")
            count += 1
            continue
        file = item
        try:
            file_name, file_ext = get_file_name_and_ext(file)
        except Exception:
            print(f"{start_err_mgs} (wrong name or extension in file: \'{file.name}\')")
            count += 1
            continue
        # print(f"{init_folder}/{file.name}")
        try:
            file_path = f"{init_folder}/{file.name}"
            image = check_is_img(file_path, file_ext)
            # print("*"*50, image.filename, file_name)
            width, height = image.size
        except (AttributeError, UnidentifiedImageError) as err:
            print(f"{start_err_mgs} (file is not a proper image: \'{file.name}\' ({err}))")
            count += 1
            continue
        # print(f"[INFO] The file is genuine image: \'{image.filename.split('/')[-1]}\' (size: {image.size})")
        if check_is_screenshot(width, height, file_ext):
            # print(f"[INFO] The file is screenshot: \'{image.filename.split('/')[-1]}\' (size: {image.size})")
            image = crop_bars(image)
            # image.show()
        # else:
            # print(f"[INFO] The file is just image, not screenshot: \'{image.filename.split('/')[-1]}\' (size: {image.size})")
        # print("before", file_name)
        if img_bigger_than_default(width, height):
            image = resize_img(image, width, height)
        # print("after", file_name)
        # print(f"=====\'{image}\' => size: {image.size}")
        # print(image.__dir__())
        save_img(image, dest_folder_path, file_name, file_ext, count)
        print(f"{start_good_msg} File is ready")
        count += 1
        count_handled += 1

    dest_folder_images_amount = get_all_from_init_folder(dest_folder_path)["all_entities_amount"]
    if dest_folder_images_amount:
        print(f"[Finish]\n"
              f"\tSource folder: \'{init_folder}\'\n"
              f"\tFiles in source folder: {count - 1}\n"
              f"\tDestination folder: \'{dest_folder_path}\'\n"
              f"\tSuccessfully processed images: {count_handled - 1}\n")
    else:
        print(f"No images were processed. Destination folder {dest_folder_path} will be deleted")


if __name__ == "__main__":
    init_folder = "/Users/Sasha/Documents/24"
    main_thread(init_folder)

