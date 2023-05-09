from PIL import Image
import os

# # Open the PNG file
# png_image = Image.open("Scrshot_1_(2).png")
#
# # Resize the image
# resized_image = png_image.resize((800, 600))
#
# # Compress and save as JPEG
# resized_image.save("Scrshot_1_(file_3).jpg", optimize=True, quality=50)
#
# # Delete the original PNG file
# os.remove("Scrshot_1_(2).png")

def get_name(img):
    spl_name = img.filename.split("/")[-1]
    img_name, img_ext = os.path.splitext(spl_name)[0], os.path.splitext(spl_name)[1].lstrip(".")
    return img_name, img_ext

img = Image.open("Снимок экрана 2022-11-01 в 19.45.14.jpeg")
print(img.size)
# print(type(get_name(img)))

def get_size_format(size, factor: int=1024, suffix: str="B") -> str:
    """ Scale bytes to its proper byte format, e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G"]:
        if size < factor:
            return f"{size:.0f}{unit}{suffix}"
        size /= factor


print(get_size_format(8))


