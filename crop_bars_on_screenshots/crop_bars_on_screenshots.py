import os
from PIL import Image
from constants import *


def get_dest_folder(source_folder) -> str:
    dest_folder = f"{source_folder}_cropped"
    try:
        os.mkdir(dest_folder)
    except FileExistsError:
        pass
    return dest_folder


def get_file_name_and_ext(file) -> tuple[str, str] or None:
    file_name = '.'.join(file.name.split('.')[:-1])
    file_ext = file.name.split('.')[-1]
    if not all((file_name, file_ext)):
        # return False
        raise TypeError #(f"[WARNING] Something wrong with file: \'{file.name}\'")
    return file_name, file_ext


def crop_image(img: Image) -> Image:
    left = 0  # Coordinates of the rectangular image that will survive after cropping
    top = 210
    right = SCREEN_WIDTH
    bottom = SCREEN_HEIGHT - 170

    img_cropped = img.crop((left, top, right, bottom))
    # img_cropped.show()    # Show cropped image in the image viewer (to check the result)
    return img_cropped


def resize_image_to_default(image: Image) -> Image:
    """Check if image vertical rectangular and resize it with height=1800;
       else image is horizontal rectangular and resize it with width=2400"""
    width, height = image.width, image.height
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


def save_img(img_to_save: Image, dest_folder: str, file_name: str, file_ext: str) -> None:
    img_to_save.save(f"{dest_folder}/{file_name}.{file_ext}")  # Edited file name == source file name
    # img_edited.save(f"{dest_folder}/{count}.{file_ext}")     # Edited file name == count
    # return img_to_save


def get_list_folder_content(source_folder: str):
    with os.scandir(source_folder) as folder_content:
        list_folder_content = list(folder_content)
    return list_folder_content


def get_img_to_save(file_path: str, file_ext: str):
    """Check if image is a screenshot and crop+resize it;
       if image's width > 2400 or height > 1800 and resize it;
       if initial image <= 2400x1800, return it with no actions"""
    img_init = Image.open(file_path)
    width, height = img_init.size
    if all((file_ext.lower() == 'png', width == SCREEN_WIDTH, height == SCREEN_HEIGHT)):
        img_cropped = crop_image(img_init)
        img_cropped_resized = resize_image_to_default(img_cropped)
        return img_cropped_resized
    elif width > OUT_WIDTH or height > SCREEN_HEIGHT:
        img_resized = resize_image_to_default(img_init)
        return img_resized
    return img_init


def main_thread(source_folder):
    list_folder_content = get_list_folder_content(source_folder)
    amount_folder_content = len(list_folder_content)
    dest_folder = get_dest_folder(source_folder)
    count = final_count = 1
    for entity in list_folder_content:
        init_msg = f"[INFO] {count} of {amount_folder_content}:"
        # Check if entity is file
        if not os.path.isfile(entity):
            print(f"{init_msg} Not processed (entity \'{entity.name}\' is not a file)")
            count += 1
            continue

        file = entity
        # Check if filename is full and extension is known
        try:
            file_name, file_ext = get_file_name_and_ext(file)
            assert file_ext.lower() in ('bmp', 'jpeg', 'jpg', 'png')
        except AssertionError:
            print(f"{init_msg} Not processed (file \'{file.name}\' is not expected image)")
            count += 1
            continue
        except TypeError:
            print(f"{init_msg} Not processed (file \'{file.name}\' has wrong filename)")
            count += 1
            continue
        file_path = f"{source_folder}/{file.name}"
        img_to_save = get_img_to_save(file_path, file_ext)
        save_img(img_to_save, dest_folder, file_name, file_ext)
        print(f"{init_msg} File is ready")
        count += 1
        final_count += 1
    print(f"[Finish] Successfully processed {final_count-1} of {count-1} files in folder: \'{dest_folder}\'")


if __name__ == "__main__":
    source_folder = "/Users/Sasha/Documents/23"
    main_thread(source_folder)
