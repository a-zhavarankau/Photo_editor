from getters import *
from checkers import *
from editors import *


def compress_and_save_jpg(img: Image, out_file_path: str, in_format: str,
                          quality: int=90, optimize: bool=True) -> None:
    """ Compress (except: .webp, .gif) and save image to .jpeg file.
    """
    if img.mode != 'RGB':
        img = img.convert('RGB')
    if in_format.lower() not in ['webp', 'gif']:
        img.save(out_file_path, 'JPEG', quality=quality, optimize=optimize)
    else:
        img.save(out_file_path)


def checker(item: Any, in_folder: str) -> bool | Any:
    """ Check item from the folder. If the item is an image, return it.
    """
    if not check_is_file(item):
        return False

    file = item
    file_path = os.path.join(in_folder, file.name)
    img = check_is_img_and_get_img(file_path)
    return img if img else False


def editor(img: Image, in_folder: str) -> Tuple[Any, Tuple]:
    """ Make some edit operations:
        - crop bars from genuine screenshot;
        - reduce the size to default if the image is bigger.
    """
    in_data = get_img_data(img, in_folder)

    if check_is_screenshot(img):
        img = crop_bars(img)
    if check_img_bigger_than_default(img):
        img = resize_img_to_default(img)

    return img, in_data


def saver(img: Image, in_data: Tuple) -> str:
    """ Compress and save image to .jpeg file.
        Prepare image data for reports (for new features).
    """
    out_folder = create_out_folder(in_folder)
    in_name, in_format = in_data[0], in_data[-2]
    out_ext = 'jpeg'
    out_file_path = os.path.join(out_folder, f"{in_name}.{out_ext}")

    compress_and_save_jpg(img, out_file_path, in_format)

    # Reopen the file to get new info about image
    out_img = Image.open(out_file_path)
    out_name, out_ext = get_name_ext(out_img)

    # Image info for reports
    out_res, out_format, out_mode = out_img.size, out_img.format, out_img.mode
    out_size = change_size_format_pretty(os.path.getsize(out_file_path))
    return f"{out_name}.{out_ext}"


def print_final_report(in_folder, out_folder) -> None:
    in_items_amount = get_folder_info(in_folder)["all_entities_amount"]
    in_folder_size = get_folder_info(in_folder)["folder_size"]
    in_folder_size_fmt = change_size_format_pretty(in_folder_size)

    out_items_amount = get_folder_info(out_folder)["all_entities_amount"]
    out_folder_size = get_folder_info(out_folder)["folder_size"]
    out_folder_size_fmt = change_size_format_pretty(out_folder_size)

    saved_size = out_folder_size - in_folder_size
    folder_size_change = saved_size / in_folder_size * 100

    print(f"[Finish process]\n")
    if out_items_amount:
        print(f"\t\tInput folder:                             {in_folder}\n"
              f"\t\tOutput folder:                            {out_folder:}\n"
              f"\t\tSuccessfully processed and saved images:  {out_items_amount} of {in_items_amount}\n"
              f"\t\tFolder size reduced:                      from {in_folder_size_fmt} to {out_folder_size_fmt} ({folder_size_change:.1f}%)")
    else:
        print(f"No images were processed.")
        os.rmdir(out_folder)


def main(in_folder: str) -> None:
    print("[Start process]")
    out_folder = create_out_folder(in_folder)

    in_folder_items = get_folder_info(in_folder)["all_entities_list"]
    in_items_amount = get_folder_info(in_folder)["all_entities_amount"]

    for i, item in enumerate(in_folder_items, start=1):
        start_good_msg = f"[+] {i} of {in_items_amount}:"
        start_err_mgs = f"[-] {i} of {in_items_amount}: Not processed"

        img = checker(item, in_folder)
        if img:
            img, init_data = editor(img, in_folder)
            out_name = saver(img, init_data)
            print(f"{start_good_msg} {out_name!r} saved successfully")
        else:
            print(f"{start_err_mgs} ({item.name!r} is not a proper image)")

    print_final_report(in_folder, out_folder)


if __name__ == "__main__":
    in_folder = input("Enter full folder path here: ")
    main(in_folder)
