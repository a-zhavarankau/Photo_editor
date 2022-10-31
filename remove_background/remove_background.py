import cv2
from rembg import remove


image_name = '../temp/Jack_Russell_Terrier.png'
image = cv2.imread(image_name)
new_image = remove(image)
photo = cv2.imwrite('../temp/Jack_Russell_Terrier_no_bg.png', new_image)

cv2.imshow('frame1', new_image)
cv2.imshow('frame', image)
cv2.waitKey(0)




