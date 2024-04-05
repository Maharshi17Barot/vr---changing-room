import cv2

def main():
    # Iterate through camera indexes
    for i in range(10):  # Try up to 10 camera indexes
        cap = cv2.VideoCapture(i)

        # Check if the camera opened successfully
        if cap.isOpened():
            print(f"Camera found at index {i}.")
            break
    else:
        print("Error: Couldn't find any camera.")
        return

    # Loop to continuously capture frames from the camera
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Couldn't capture frame.")
            break

        # Display the captured frame
        cv2.imshow('Camera Feed', frame)

        # Wait for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
