import os
from PIL import Image

source_folder = "/Users/Sasha/Documents/22"
dest_folder = f"{source_folder}_cropped"
try:
    os.mkdir(dest_folder)
except FileExistsError:
    pass

files_in_folder = os.scandir(source_folder)
files_amount = len(list(files_in_folder))

with os.scandir(source_folder) as files_in_folder:
    count = 1
    for file in files_in_folder:
        file_name = '.'.join(file.name.split('.')[:-1])
        file_ext = file.name.split('.')[-1]

        if file_ext.lower() in ['png', 'jpg', 'jpeg']:
            full_filename = f"{source_folder}/{file.name}"
            img = Image.open(full_filename)
            width, height = img.size

            left = 0
            top = 210
            right = width
            bottom = height - 170

            img_cropped = img.crop((left, top, right, bottom))
            # percent = 75   # Percentage to resize
            # img_cropped = img_cropped.resize((img_cropped.size[0] * percent // 100, img_cropped.size[1] * percent // 100))  # To resize img
            img_cropped.save(f"{dest_folder}/{file_name}_cropped.{file_ext}")
            # img_cropped.save(f"{dest_folder}/{count}.{file_ext}")
            print(f"[INFO] File {count} of {files_amount} ready")
            count += 1
            # img.show()     # - Show the original image in the image viewer
            # img_cropped.show()     # - Show the cropped  image in the image viewer

