from PIL import Image

file = "dj_1.png"
# Opens a image in RGB mode
im = Image.open(file)
# im.show()

# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
print(width, height)

# Setting the points for cropped image
left = 0
top = 210
right = width
bottom = height - 170

# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))

# Shows the image in image viewer
im1.save(f"{'.'.join(file.split('.')[:-1])}_cropped.png")
# im1.show()