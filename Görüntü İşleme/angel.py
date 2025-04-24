from ultralytics import YOLO
import cv2
import numpy as np


model_path = 'last4.pt'
model = YOLO(model_path)
cap = cv2.VideoCapture(0)

# new_width = 432  # Yeni genişlik
# new_height = 560  # Yeni yükseklik

while True:
    _, frame = cap.read()
    #frame = cv2.resize(frame, (new_width, new_height))
    results = model(frame)
    keypoints = results[0].keypoints
    
    for keypoint in keypoints.xy:
        if(len(keypoint)>2):
            for point in keypoint:
                cv2.circle(frame, (int(point[0]), int(point[1])), 5, (255, 0, 0), -1)

            point1_x , point1_y = keypoint[1][0] , keypoint[1][1] 
            point2_x , point2_y = keypoint[2][0] , keypoint[2][1]

            vektor = np.array([point2_x - point1_x , point2_y - point1_y])
            aci_radyan = np.arctan2(vektor[1], vektor[0])
            aci = np.degrees(aci_radyan)

            if aci < 0:
                direction = 'Sol'
                aci = -aci
                print(f"Araba {aci} açıyla {direction} yönde.")

            elif aci > 0:
                direction = 'Sağ'
                print(f"Araba {aci} açıyla {direction} yönde.")
            elif aci == 0 :
                direction = 'Düz'
                print(f"Araba {aci} açıyla {direction} yönde.")
            
            # 2. ve 3. noktalar arasında çizgi çizme
            cv2.line(frame, (int(keypoint[1][0]), int(keypoint[1][1])), (int(keypoint[2][0]), int(keypoint[2][1])), (0, 0, 255), 2)

            # 2. ve 3. nokta arasındaki çizginin orta noktasını bulma
            mid_x = (int(keypoint[1][0]) + int(keypoint[2][0])) / 2
            mid_y = (int(keypoint[1][1]) + int(keypoint[2][1])) / 2

            # 2. ve 3. nokta arasındaki çizginin yönünü bulma
            dx = int(keypoint[2][0]) - int(keypoint[1][0])
            dy = int(keypoint[2][1]) - int(keypoint[1][1])  

            # 90 derece açı ile bir çizgi çizme ve çizginin başlangıç ve bitiş noktalarını hesaplama
            line_length = 0.5
            start_x = int(mid_x - line_length * dy)
            start_y = int(mid_y + line_length * dx)
            end_x = int(mid_x + line_length * dy)
            end_y = int(mid_y - line_length * dx)
            

            cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)

    if(cv2.waitKey(5) & 0xFF == ord("q")):
        break

cap.release()
cv2.destroyAllWindows()