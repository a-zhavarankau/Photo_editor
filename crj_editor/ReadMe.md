## CRJ-editor
### (Compress-Resize-Jpeg)
<br>
Image editor for converting images in different formats into the .jpeg files, resized and compressed. 
<p>The initial resolution becomes the default value of 2000x1250 if it was larger before.
<p>Initial formats are: 'bmp', 'jpeg', 'jpg', 'png', 'heif', 'tiff', 'gif', 'webp'. Formats 'webp', 'gif' are not compressed due to a significant decrease in quality.
<p>The program checks whether the object in the folder is a file, a valid image, or a screenshot. In case of a screenshot, the top and bottom bars are cropped.
<p>If the object is not a file, it is not copied to the new directory.

## How to start

Run 'Main.py' and in the terminal enter full path of the initial directory, then press 'Enter'. A new directory named '[initial directory]_edited' should appear. All files in the new directory should be .jpeg images 2000x1250 or smaller.

### Instruments:
- PIL (Python Image Library), pillow_heif
- PyTest