from ultralytics import YOLO
import cv2
import os

VIDEOS_DIR = os.path.join('.', 'video')
video_path = os.path.join(VIDEOS_DIR, 'gorev_v3_2.mp4')
video_path_out = '{}_out.mp4'.format(video_path)

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = os.path.join('.', 'runs', 'pose', 'train5', 'weights', 'last.pt')
model = YOLO(model_path)

fontScale = 1.5  # Yazının boyutunu ayarla
threshold = 0.5

while ret:
    results = model(frame)[0]
    if results.keypoints.conf is not None:
        for keypoint_indx, (keypoint, conf) in enumerate(zip(results.keypoints.xy[0], results.keypoints.conf[0])):
            x, y = keypoint.tolist()
            print(f"Keypoint1 {keypoint_indx + 1}: x={x}, y={y}, Confidence={conf}")
            #cv2.putText(frame, str(keypoint_indx + 1), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 255), 2)
            cv2.circle(frame, (int(x), int(y)), 10, (0, 0, 255), -1)

            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result

                if score > threshold:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                    cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        out.write(frame)
        ret, frame = cap.read()
    else:
        for keypoint_indx, keypoint in enumerate(results.keypoints.xy[0]):
            x, y = keypoint.tolist()
            print(f"Keypoint2 {keypoint_indx + 1}: x={x}, y={y}")
            #cv2.putText(frame, str(keypoint_indx + 1), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 255), 2)
            cv2.circle(frame, (int(x), int(y)), 10, (0, 0, 255), -1) #10 dairenin radiusu
            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result

                if score > threshold:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                    cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        out.write(frame)
        ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()
