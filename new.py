from PIL import Image, UnidentifiedImageError
import pillow_heif
import os


# def compress(image_file):
#     filepath = os.path.join(os.getcwd(), image_file)
#
#     image = Image.open(filepath)
#     print(image.size)
#     image_size = os.path.getsize(image_file)
#     print(image_size)
#
#     # image.save("image-file-compressed",
#     #            "JPEG",
#     #            optimize=True,
#     #            quality=10)
#     return
#
# compress("Scrshot_1.png")


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compress_img(image_name, new_size_ratio=0.9, quality=90, width=None, height=None, to_jpg=True):
    img = Image.open(image_name)
    print("[*] Image shape:", img.size)
    image_size = os.path.getsize(image_name)
    print("[*] Size before compression:", get_size_format(image_size))
    if new_size_ratio < 1.0:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        print("[+] New Image shape:", img.size)
    elif width and height:
        img = img.resize((width, height), Image.ANTIALIAS)
        print("[+] New Image shape:", img.size)
    filename, ext = os.path.splitext(image_name)
    if to_jpg:
        new_filename = f"{filename}_compressed.jpg"
    else:
        new_filename = f"{filename}_compressed{ext}"
    try:
        img.save(new_filename, quality=quality, optimize=True)
    except OSError as ose:
        print(ose)
        img = img.convert("RGB")
        img.save(new_filename, quality=quality, optimize=True)
    print("[+] New file saved:", new_filename)
    new_image_size = os.path.getsize(new_filename)
    print("[+] Size after compression:", get_size_format(new_image_size))
    saving_diff = new_image_size - image_size
    print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")


filename = "Scrshot_1.png"
compress_img(filename)


# def image_format(filename, i):
#     pillow_heif.register_heif_opener()
#     image = Image.open(filename)
#     print(i, filename, "->", image.format)
#
# # lst = [
# #     "Scrshot_1.png",
# #     "Scrshot_1_compressed_jpg.heic",
# #     "Scrshot_1_png.jpeg",
# #     "img_heic.HEIC",
# # ]
#
# def get_all_from_init_folder(init_folder: str) -> dict[str: list | int]:
#     all_entities = os.scandir(init_folder)
#     all_entities_list = list(all_entities)
#     all_entities_amount = len(all_entities_list)
#     return {"all_entities_list": all_entities_list, "all_entities_amount": all_entities_amount}
#
# init_folder = "/Users/Sasha/Documents/24_different"
# lst_ = get_all_from_init_folder(init_folder)["all_entities_list"]
# lst = [f"{init_folder}/{file.name}" for file in lst_]
# # print(lst)
#
# for i, filename in enumerate(lst, start=1):
# # #     print(filename)
# # #     file_path = f"{init_folder}/{filename.name}"
# # #     # file_name = '.'.join(filename.name.split('.')[:-1])
# # #     # file_ext = filename.name.split('.')[-1]
# # #     # if not all((file_name, file_ext)):
# # #     #     print(False)
# # #     # print(file_name, file_ext)
# # #     image = Image.open(file_path)
#
#
#     # try:
#     #     image_format(filename, i)
#     # except (UnidentifiedImageError):
#     #     print(i, filename, "-> wrong image")
#     # except IsADirectoryError:
#     #     print(i, filename, "-> not file")
#     #     continue
#     print("Working file #", i)
#     try:
#         compress_img(filename)
#     except Exception:
#         print("Operation interrupted: wrong image")

