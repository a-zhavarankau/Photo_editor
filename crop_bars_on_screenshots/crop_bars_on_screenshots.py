import os
from PIL import Image


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
        return None
    return file_name, file_ext

def crop_image(img: Image, width: int, height: int) -> Image:
    left = 0  # Coordinates of the rectangular image that will survive after cropping
    top = 210
    right = width
    bottom = height - 170

    img_cropped = img.crop((left, top, right, bottom))
    img_edited = img_cropped.resize((2500, img_cropped.size[1] * 2500 // width))
    # img_cropped.show()    # Show cropped image in the image viewer (to check the result)
    return img_edited

def resize_image(img: Image, width: int, height: int) -> Image:
    img_edited = img.resize((width * 1800 // height, 1800))
    return img_edited

def save_img(img_edited, dest_folder, file_name, file_ext):
    img_edited.save(f"{dest_folder}/{file_name}.{file_ext}")  # Edited file name == source file name
    # img_edited.save(f"{dest_folder}/{count}.{file_ext}")     # Edited file name == count
    return img_edited


def save_images(source_folder):
    with os.scandir(source_folder) as folder_content:
        list_folder_content = list(folder_content)
        files_amount = len(list_folder_content)
        count = 1
        for entity in list_folder_content:
            if os.path.isfile(entity) and entity.name != '.DS_Store':
                file = entity
                try:
                    file_name, file_ext = get_file_name_and_ext(file)
                except Exception:
                    print(f"Something wrong with {file.name}")
                    pass
                else:
                    file_path = f"{source_folder}/{file.name}"
                    dest_folder = get_dest_folder(source_folder)

                    img = Image.open(file_path)
                    width, height = img.size
                    if file_ext.lower() == 'png' and width == 2880 and height == 1800:  # Check if file a screenshot
                        img_edited = crop_image(img, width, height)
                    elif all((file_ext.lower() in ['jpg', 'jpeg'], width > 2500, height > 2000)):
                        img_edited = resize_image(img, width, height)
                    else:
                        continue
                    save_img(img_edited, dest_folder, file_name, file_ext)
                    print(f"[INFO] File {count} of {files_amount} ready")
                    count += 1


source_folder = "/Users/Sasha/Documents/Python/Тестирования/TestingFolder"
save_images(source_folder)

