# from ultralytics import YOLO
# import cv2

# model = YOLO("yolov8n.pt")

# results = model.predict(source = 0, show = True)
# print(len(results.xyxy[0]))
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        #check for phone
        for result in results:
            print("For loop entered")
            for classvalue in result.boxes.cls:
                print("Second For loop entered")
                if(classvalue.item() == 67):
                    print("CELLPHONE FOUND")
        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()