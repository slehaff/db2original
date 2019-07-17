
import cv2
import numpy as np

# this function is needed for the createTrackbar step downstream
def nothing(x):
    pass

# read the experimental image
img = cv2.imread('image17.png', 0)
img = img[0:240, :]
phase = cv2.imread('im_wrap2.png', 0)

# create trackbar for canny edge detection threshold changes
cv2.namedWindow('canny')

# add ON/OFF switch to "canny"
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'canny', 0, 1, nothing)

# add lower and upper threshold slidebars to "canny"
cv2.createTrackbar('lower', 'canny', 0, 255, nothing)
cv2.createTrackbar('upper', 'canny', 0, 255, nothing)

# Infinite loop until we hit the escape key on keyboard
while(1):

    # get current positions of four trackbars
    lower = cv2.getTrackbarPos('lower', 'canny')
    upper = cv2.getTrackbarPos('upper', 'canny')
    s = cv2.getTrackbarPos(switch, 'canny')
    if s == 0:
        edges = img
    else:
        edges = cv2.Canny(img, lower, upper)
    # display images
    cv2.imshow('original', img)
    cv2.imshow('canny', edges)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:   # hit escape to quit
        ans = []
        for y in range(0, edges.shape[0]):
            for x in range(0, edges.shape[1]):
                if edges[y, x] != 0:
                    phi = phase[y, x]
                    ans += [[x, y, phi]]
        ans = np.array(ans)
        ans = ans[1::40, :]
        print(ans.shape)
        print(ans[0:240, :])
        break

cv2.destroyAllWindows()
