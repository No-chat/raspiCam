import cv2
from cv2 import ADAPTIVE_THRESH_GAUSSIAN_C
from cv2 import THRESH_BINARY_INV
import numpy as np
import matplotlib.pyplot as plt
import sys
plt.style.use('dark_background')

img_car = cv2.imread('./car_number/car3.jpg')

if img_car is None:
  print('Image load failed!')
  sys.exit()

# 전단 변환
aff = np.array([[1,0,0],[-0.25,1,0]], dtype=np.float32)
affine_car = cv2.warpAffine(img_car, aff, (0,0))



gray_car = cv2.cvtColor(affine_car, cv2.COLOR_BGR2GRAY)
# 가우시안 필터 적용 -> 사진의 노이즈 제거
blurred_car = cv2.GaussianBlur(gray_car, (0,0), 0.7)
# Threshholding 적용 -> 사진을 흑과 백으로만 구성 / 가우시안 필터가 적용된 영상
car_blur_thresh = cv2.adaptiveThreshold(
  blurred_car,
  maxValue=255.0,
  adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
  thresholdType=cv2.THRESH_BINARY_INV,
  blockSize=19,
  C=9
)
height, width, channel = img_car.shape

# Find Contours 
contours, __=cv2.findContours(car_blur_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
temp_result = np.zeros((height, width, channel), dtype=np.uint8)

contours_dict = []

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(affine_car, pt1=(x,y), pt2=(x+w, y+h), color=(255,255,255), thickness=1)
    
    contours_dict.append({
        'contour': contour,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'cx': x + (w / 2),
        'cy': y + (h / 2)
    })

#cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255,255,255))

print(contours_dict)

# MIN_AREA = 100
# MIN_WIDTH, MIN_HEIGHT=1, 1
# MIN_RATIO, MAX_RATIO = 0.25, 1.0

# possible_contours = []

# cnt = 0
# for d in contours_dict:
#     area = d['w'] * d['h']
#     ratio = d['w'] / d['h']
    
#     if area > MIN_AREA \
#     and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
#     and MIN_RATIO < ratio < MAX_RATIO:
#         d['idx'] = cnt
#         cnt += 1
#         possible_contours.append(d)

# temp_result = np.zeros((height, width, channel), dtype = np.uint8)

# for d in possible_contours:
#     cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255, 255, 255), thickness=2)



plt.figure(figsize=(12, 10))
plt.imshow(affine_car, cmap='gray')
plt.show()
print(height, width, channel)

