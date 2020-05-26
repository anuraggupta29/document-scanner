import numpy as np
import cv2
import imutils

#Auto Canny function by Adrian Rosebrock
def autocanny(image, sigma=0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma)*v))
    upper = int(min(255, (1.0 - sigma)*v))
    edged = cv2.Canny(image, lower, upper)

    return edged

filepath = 'test_images/test.jpg'
resizeHeight = 600
original = None
img = None
gray = None
blurred = None
edged = None
cnts = None
cntdrawn = None
hull = None
largestcnt = None
perimeter = None
corners = None
roidrawn = None
factor = None
cornerslist = None
tl, tr, br, bl = None, None, None, None
widthTop, widthBottom = None, None
heightLeft, heightRight = None, None
maxWidth, maxHeight = None, None
dst = None
transformMatrix = None
scan = None

original = cv2.imread(filepath)
img = imutils.resize(original.copy(), height=resizeHeight)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.bilateralFilter(gray, 10, 30, 30)
edged = autocanny(blurred)

if (int(cv2.__version__[0]) > 3):
    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
else:
    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]

largestcnt = max(cnts, key = lambda x: cv2.arcLength(x, True))
hull = cv2.convexHull(largestcnt)
perimeter = cv2.arcLength(hull, True)
corners = cv2.approxPolyDP(hull, 0.02*perimeter, True)
print(corners)
roidrawn = cv2.drawContours(img.copy(), [hull], -1, (0,255,0), 3)

factor = original.shape[0]/resizeHeight

cornerslist = (corners.reshape(4,2)*factor).astype(int).tolist()
print(cornerslist)

tl = min(cornerslist, key = lambda x: x[0]+x[1])
tr = max(cornerslist, key = lambda x: x[0]-x[1])
br = max(cornerslist, key = lambda x: x[0]+x[1])
bl = min(cornerslist, key = lambda x: x[0]-x[1])

cornerslist = np.array([tl, tr, br, bl], dtype='float32').reshape(4,2)

widthTop = np.sqrt((tl[0] - tr[0])**2 + (tl[1] - tr[1])**2)
widthBottom = np.sqrt((bl[0] - br[0])**2 + (bl[1] - br[1])**2)
heightLeft = np.sqrt((tl[0] - bl[0])**2 + (tl[1] - bl[1])**2)
heightRight = np.sqrt((tr[0] - br[0])**2 + (tr[1] - br[1])**2)

maxWidth = int((widthTop+widthBottom)/2)
maxHeight = int((heightLeft+heightRight)/2)

dst = np.array([
    [0,0],
    [maxWidth-1, 0],
    [maxWidth-1, maxHeight-1],
    [0, maxHeight-1]], dtype='float32')

transformMatrix = cv2.getPerspectiveTransform(cornerslist, dst)
scan = cv2.warpPerspective(original, transformMatrix, (maxWidth, maxHeight))

#cv2.imwrite('output/scanned.jpg', scan)

#cv2.imshow('Orignal', imutils.resize(original, height=resizeHeight))
#cv2.imshow('Gray', gray)
#cv2.imshow('Blurred', blurred)
cv2.imshow('Autocanny', edged)
cv2.imshow('Document', roidrawn)
cv2.imshow('Scanned', imutils.resize(scan, height=resizeHeight))
cv2.waitKey(0)
cv2.destroyAllWindows()
