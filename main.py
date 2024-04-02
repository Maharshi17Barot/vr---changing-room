import os
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Failed to open camera.")
    exit()

detector = PoseDetector()
shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
imageNumber = 0

imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read frame from camera.")
        break

    if img is None:
        print("Empty frame received.")
        continue

    img = detector.findPose(img)
    if img is None:
        print("Pose detection failed.")
        continue

    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        widthOfShirt = int((lm11[0] - lm12[0]) * 262 / 190)
        if widthOfShirt > 0:
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * 581 / 440)))
        else:
            print("Invalid width for resizing.")
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except Exception as e:
            print("Error overlaying image:", e)

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        if lmList[16][1] < 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0, counterRight * selectionSpeed, (0, 255, 0), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
        elif lmList[15][1] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
