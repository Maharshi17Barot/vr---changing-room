import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
sunglasses = cv2.imread('glasses.png')
cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        if h > 0 and w > 0:
            h, w = int(1.4 * h), int(1.2 * w)
            y += 25
            x -= 17

        eye = eye_cascade.detectMultiScale(gray, 1.3, 9)
        for (ex, ey, ew, eh) in eye:
            if eh > 0 and ew > 0:
                eh, ew = int(3 * eh), int(4.5 * ew)
                ey -= 30
                ex -= 50

                img_roi = img[ey:ey + eh, ex:ex + ew]  # the postiton of the left eye

                sunglasses_small = cv2.resize(sunglasses, (ew, eh), interpolation=cv2.INTER_AREA)
                gray_sunglasses = cv2.cvtColor(sunglasses_small, cv2.COLOR_BGR2GRAY)

                ret, mask = cv2.threshold(gray_sunglasses, 230, 255, cv2.THRESH_BINARY_INV)
                mask_inv = cv2.bitwise_not(mask)
                masked_face = cv2.bitwise_and(sunglasses_small, sunglasses_small, mask=mask)

                masked_frame = cv2.bitwise_and(img_roi, img_roi, mask=mask_inv)
                img[ey:ey + eh, ex:ex + ew] = cv2.add(masked_face, masked_frame)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()