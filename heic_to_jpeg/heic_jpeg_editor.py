import pillow_heif
import os
from pillow_heif import HeifError
from PIL import Image, UnidentifiedImageError
from crop_bars_on_screenshots import crop_2
from working_files.constants import *


# def heic_to_jpeg(dirpath):
#     pillow_heif.register_heif_opener()
#     file = "IMG_2226.HEIC"
#     file_name, file_ext = ".".join(file.split('.')[:-1]), file.split('.')[-1].lower()
#     percent = 50
#     input_px = {"width": 4032, "height": 3024}
#     output_px = {"width": int(input_px["width"]*percent/100),
#                  "height": int(input_px["height"]*percent/100)}
#     if file_ext == "heic":
#         image = pillow_heif.open_heif(file)
#         image.scale(output_px["width"], output_px["height"])
#         image.save(f"{file_name}.jpeg")
#     elif file_ext in ("jpg", "jpeg"):
#         image = pillow_heif.open_heif(file)
#         image.scale(output_px["width"], output_px["height"])
#         image.save(file)
#
# heic_to_jpeg(1)


def check_is_heic_and_get_img(file_path: str, file_ext: str) -> any:
    """Check if the file is a proper .heic image"""
    if file_ext.lower() == 'heic':
        pillow_heif.register_heif_opener()
        image = pillow_heif.open_heif(file_path)
        return image
    raise AttributeError(f"unknown extension to process: \'{file_ext}\'")


def resize_img_heic_to_default(image: Image, width: int, height: int) -> Image:
    """Check if image vertical rectangular and resize it with height=1800;
           else image is horizontal rectangular and resize it with width=2400"""
    if height > width:
        # If image is vertical rectangular, resize image.height = SCREEN_HEIGHT, image.width -> respectively
        resized_height = SCREEN_HEIGHT
        resized_width = int(width * resized_height / height)
    else:
        # If image is horizontal rectangular, resize image.width = FINAL_WIDTH, image.height -> respectively
        resized_width = DEFAULT_WIDTH
        resized_height = int(height * resized_width / width)
    image.scale(resized_width, resized_height)
    return image


def main_thread(init_folder: str):
    dest_folder_path = crop_2.create_dest_folder(init_folder)
    all_entities_list = crop_2.get_all_from_init_folder(init_folder)["all_entities_list"]
    all_entities_amount = crop_2.get_all_from_init_folder(init_folder)["all_entities_amount"]
    count = count_processed = 1
    for item in all_entities_list:
        start_good_msg = f"[INFO] {count} of {all_entities_amount}:"
        start_err_mgs = f"[INFO] {count} of {all_entities_amount}: Not processed"
        if crop_2.check_is_not_file(item):
            print(f"{start_err_mgs} (entity is not a file: \'{item.name}\')")
            count += 1
            continue
        file = item
        try:
            file_name, file_ext = crop_2.get_file_name_and_ext(file)
        except TypeError:
            print(f"{start_err_mgs} (wrong name or extension in file: \'{file.name}\')")
            count += 1
            continue
        file_path = f"{init_folder}/{file.name}"
        try:
            image = check_is_heic_and_get_img(file_path, file_ext)
            width, height = image.size
        except (AttributeError, HeifError) as err:
            print(f"{start_err_mgs} (file is not a proper .heic image: "
                  f"\'{file.name}\' ({err}))")
            count += 1
            continue
        if crop_2.check_img_bigger_than_default(width, height):
            image = resize_img_heic_to_default(image, width, height)
        crop_2.save_img_to_dest_folder(image, dest_folder_path, file_name, file_ext='jpg')
        print(f"{start_good_msg} File is ready")
        count += 1
        count_processed += 1
    # Prepare final message
    dest_folder_images_amount = \
        crop_2.get_all_from_init_folder(dest_folder_path)["all_entities_amount"]
    if dest_folder_images_amount:
        print(f"[Finish]\n"
              f"\t\tSource folder: \'{init_folder}\'\n"
              f"\t\tFiles in source folder: {count - 1}\n"
              f"\t\tDestination folder: \'{dest_folder_path}\'\n"
              f"\t\tSuccessfully processed and saved images: {count_processed - 1}\n")
    else:
        print(f"[Finish]\n"
              f"No images were processed. "
              f"Destination folder {dest_folder_path} will be deleted")
        os.rmdir(dest_folder_path)


if __name__ == "__main__":
    init_folder = "/Users/Sasha/Documents/25_heics"
    main_thread(init_folder)



