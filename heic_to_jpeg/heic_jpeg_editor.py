import pillow_heif


def heic_to_jpeg(dirpath):
    pillow_heif.register_heif_opener()
    file = "IMG_2226.HEIC"
    file_name, file_ext = ".".join(file.split('.')[:-1]), file.split('.')[-1].lower()
    percent = 50
    input_px = {"width": 4032, "height": 3024}
    output_px = {"width": int(input_px["width"]*percent/100),
                 "height": int(input_px["height"]*percent/100)}
    if file_ext == "heic":
        image = pillow_heif.open_heif(file)
        image.scale(output_px["width"], output_px["height"])
        image.save(f"{file_name}.jpeg")
    elif file_ext in ("jpg", "jpeg"):
        image = pillow_heif.open_heif(file)
        image.scale(output_px["width"], output_px["height"])
        image.save(file)

if __name__ == "__main__":
    heic_to_jpeg(1)



