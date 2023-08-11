import cv2
import numpy as np
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode
import datetime
import time
import os


with open("qr_reader/whitelist.txt", "r") as f:

    author_user = [l[:-1] for l in f.readlines() if len(l)>2]
    f.close()

log_path = "qr_reader/log.txt"

cap  = cv2.VideoCapture(0)

most_recent_access = {}
time_between_logs = 5

while True:

    ret,frame = cap.read()


    qr_info = decode(frame)


    if len(qr_info)>0:

        qr = qr_info[0]
        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        if data.decode() in author_user:

            cv2.putText(frame, "ACCESS GRANTED" , (rect.left, rect.top -15), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            if data.decode() not in  most_recent_access.keys() or  time.time() - most_recent_access[data.decode()]  > time_between_logs:
                
                most_recent_access[data.decode()] = time.time()
                with open(log_path ,"a") as f:
                    f.write('{},{}\n'.format(data.decode(),datetime.datetime.now()))
                    f.close()

        else:
            cv2.putText(frame, "ACCESS DENIED" , (rect.left, rect.top -15), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)

        frame = cv2.rectangle(frame, (rect.left, rect.top),(rect.left + rect.width , rect.top + rect.height), (0,255,0),5)

        frame = cv2.polylines(frame, [np.array(polygon)], True , (255,0,0), 5)

    cv2.imshow("webcam",frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
