from PIL import Image

file = "dj_1.png"
file_name = '.'.join(file.split('.')[:-1])
file_ext = file.split('.')[-1]
print(file_name, file_ext)

img = Image.open(file)
# img.show()         # - Show the original image in the image viewer

width, height = img.size

if width == 2880 and height == 1800 and file_ext.lower() in ['png', 'jpg', 'jpeg']:
    # Set the points for image that will survive (left-top, right-bottom)
    left = 0
    top = 210
    right = width
    bottom = height - 170

    img_cropped = img.crop((left, top, right, bottom))

    # img_cropped.save(f"{file_name}_cropped.{file_ext}")

    # img.show()            # - Show the original image in the image viewer
    # img_cropped.show()    # - Show the cropped  image in the image viewer
else:
    print('Check the input file resolution (it is not 2880x1800px)')
