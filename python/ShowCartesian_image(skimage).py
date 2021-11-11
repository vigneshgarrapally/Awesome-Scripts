from skimage import data
from skimage.io import imread,imshow
from skimage.transform import warp_polar
#image=imread(r'C:/Users/vignesh/Desktop/80mT6.jpg')
image=data.checkerboard()
warped=warp_polar(image)
print(imshow(image))
print(imshow(warped))
