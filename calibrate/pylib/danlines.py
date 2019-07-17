
import cv2
import numpy as np

img = cv2.imread('image18.png', 0)
img = img[10:240, :]
cv2.namedWindow('canny')
lower = 30
upper = 60
edges = cv2.Canny(img, lower, upper)
ans = []
for y in range(0, edges.shape[0]):
    for x in range(0, edges.shape[1]):
        if edges[y, x] != 0:
            ans += [[x, y]]
ans = np.array(ans)
ans = ans[1::40, :]
print(edges.shape)
print(ans[0:240, :])
