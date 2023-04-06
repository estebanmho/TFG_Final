import cv2
from cvzone.HandTrackingModule import HandDetector
import csv
import time

cap = cv2.VideoCapture(1)
detector = HandDetector(detectionCon=0.8, maxHands=1) #numero max de manos posiblemente 1 para que no se confunda
csv_file = "../data/simb_test_mar_5.csv"
i = 0
try:
    with open(csv_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["pulgar", "indice", "corazon", "anular", "menique", "pulgar_indice", "simb"])
        writer.writeheader()
        while True:
            time.sleep(0.05)
            success, img = cap.read()
            hands, img = detector.findHands(img)
            #hands = detector.findHands(img, draw=False) no drawibg



            if hands:
                hand1 = hands[0]
                puntos = hand1["lmList"]
                bbox = hand1["bbox"]  # Bounding box info x,y,w,h
                centerPoint = hand1["center"]
                pulgar, info = detector.findDistance(puntos[4][:2], puntos[0][:2])
                indice, info = detector.findDistance(puntos[8][:2], puntos[0][:2])
                corazon, info = detector.findDistance(puntos[12][:2], puntos[0][:2])
                anular, info = detector.findDistance(puntos[16][:2], puntos[0][:2])
                menique, info = detector.findDistance(puntos[20][:2], puntos[0][:2])
                pulgar_indice, info = detector.findDistance(puntos[4][:2], puntos[8][:2])
                magnitud, info = detector.findDistance(centerPoint, puntos[0][:2])

                dictDist = [{"pulgar": pulgar / magnitud, "indice": indice / magnitud, "corazon": corazon / magnitud, "anular": anular / magnitud, "menique": menique / magnitud, "pulgar_indice": pulgar_indice / magnitud, "simb": 5}]
                '''cv2.putText(img, f'Dist:{int(length)}', (bbox[0] + 400, bbox[1] - 30),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)'''

                for data in dictDist:
                        writer.writerow(data)
                        i += 1
                        print(i)
                if i == 250:
                    break


            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
except IOError:
    print("I/O error")
