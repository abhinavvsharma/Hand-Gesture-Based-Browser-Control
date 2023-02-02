import cv2
import numpy as np
import math
import os
import time
from selenium import webdriver

print("Welcome to Hand-Gesture based browser control!!\n\nThis is the history of your gesture based control:\n")
file = open("website_history.txt", "r")
lines = file.readlines()
for i in range(3):
    print("%d-Fingers --> %s" % (i+2, lines[i]))
fingers2 = str(lines[0][:-1])
fingers3 = str(lines[1][:-1])
fingers4 = str(lines[2][:-1])
file.close()
decision = input("\nDo you want to update the gestures? If 'Yes' type 'Y/y' else type 'N/n':")
if decision == 'y' or decision == 'Y':
    file = open("website_history.txt", "w")
    fingers2=input("\nEnter Website name with domain for:\n2-Fingers:")
    file.write(fingers2)
    file.write("\n")
    fingers3=input("\n3-Fingers:")
    file.write(fingers3)
    file.write("\n")
    fingers4=input("\n4-Fingers:")
    file.write(fingers4)
    file.write("\n")
    file.close()

print ("\n\nPoint Closed Fist to Scroll-Down and Point 1-Finger to Scroll-Up\n\nYour gesture-based websites are:")
file = open("website_history.txt", "r")
lines = file.readlines()
for i in range(3):
    print("%d-Fingers --> %s" % (i+2, lines[i]))

file.close()
print("Starting Browser and Camera....")
time.sleep(7)

cap = cv2.VideoCapture(0)
latest = 0
browser = webdriver.Chrome()
counter = [0 for _ in range(6)]
page_flag = False
tab_flag = [None, None, False, False, False]
while(1):

    try:  #avoids error if the camera does not receive a video feed from camera

        _, current_frame = cap.read()
        current_frame = cv2.flip(current_frame, 1)
        kernel = np.ones((3,3), np.uint8)

        
        region_of_interest = current_frame[100:300, 100:300] #this box is the region-of-interest in which the user should place hand


        cv2.rectangle(current_frame, (100,100), (300,300), (0,255,0), 0)
        hue_sat_val = cv2.cvtColor(region_of_interest, cv2.COLOR_BGR2HSV)



        hand_range_high = np.array([20,255,255], dtype=np.uint8)    #higher range of skin color
        hand_range_low = np.array([0,20,70], dtype=np.uint8)   #lower range of skin color
        

        mask = cv2.inRange(hue_sat_val, hand_range_low, hand_range_high) #segment the hand from the region-of-interest



        mask = cv2.dilate(mask, kernel, iterations = 4)   #eliminating noise from hand


        mask = cv2.GaussianBlur(mask, (5,5), 100)   #use blur to smoothen to image


        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #extracting contour


        count = max(contours, key = lambda x: cv2.contourArea(x))  #find out the maximum area of hand

        epsilon = 0.0005*cv2.arcLength(count,True)
        approximation = cv2.approxPolyDP(count,epsilon,True)


        convex_hull = cv2.convexHull(count)     #draw convex-hull around hand


        area_hull = cv2.contourArea(convex_hull)  #calculate area of hull
        area_cnt = cv2.contourArea(count)       ##calculate area of hand
        

        area_ratio=((area_hull - area_cnt)/area_cnt)*100    #region of area not covered by hand
  
        convex_hull = cv2.convexHull(approximation, returnPoints=False)  #number of defects
        defects = cv2.convexityDefects(approximation, convex_hull)

        no_of_defects = 0   

        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approximation[s][0])
            end = tuple(approximation[e][0])
            far = tuple(approximation[f][0])
            pt = (100,180)


            tri_side_a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            tri_side_b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            tri_side_c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (tri_side_a+tri_side_b+tri_side_c)/2
            area = math.sqrt(s*(s-tri_side_a)*(s-tri_side_b)*(s-tri_side_c))    #find area of triangle

            dist = (2*area)/tri_side_a  #euclidean distacne between points and convex hull

            angle = math.acos((tri_side_b**2 + tri_side_c**2 - tri_side_a**2)/(2*tri_side_b*tri_side_c)) * 57


            if angle <= 90 and dist > 30:
                no_of_defects += 1
                cv2.circle(region_of_interest, far, 3, [255,0,0], -1)


            cv2.line(region_of_interest,start, end, [0,255,0], 2) #draw region around hand
        no_of_defects += 1
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        if no_of_defects == 1:
            if area_cnt<2000:
                cv2.putText(current_frame,'Put hand in the box',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            else:
                if area_ratio<12:
                    cv2.putText(current_frame,'0',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    browser.execute_script("window.scrollBy(0,20)","")                          #triggering scroll down
                
                else:
                    cv2.putText(current_frame,'1',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    browser.execute_script("window.scrollBy(0,-20)","")     #triggering scroll up

        elif no_of_defects == 2:
            cv2.putText(current_frame,'2',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            counter[2] += 1
            if counter[2] == 50:
                if tab_flag[2]:
                    browser.switch_to.window(window_name=twoopen)                    
                elif page_flag:
                    temp = 'https://'+fingers2
                    browser.execute_script(f'''window.open("{temp}","twoopen");''')   #opening a website
                    tab_flag[2] = True
                else:                
                    browser.get("https://"+fingers2)
                    twoopen = browser.current_window_handle
                    page_flag = True
                    tab_flag[2] = True
                counter = [0 for _ in range(6)]
        elif no_of_defects == 3:
            cv2.putText(current_frame,'3',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            counter[3] += 1
            if counter[3] == 50:
                if tab_flag[3]:
                    browser.switch_to.window(window_name="threeopen")
                elif page_flag:
                    temp = 'https://'+fingers3
                    browser.execute_script(f'''window.open("{temp}","threeopen");''')
                    tab_flag[3] = True
                else:                
                    browser.get("https://"+fingers3)
                    page_flag = True
                    tab_flag[3] = True
                counter = [0 for _ in range(6)]
        elif no_of_defects == 4:
            cv2.putText(current_frame,'4',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            counter[4] += 1
            if counter[4] == 50:
                if tab_flag[4]:
                    browser.switch_to.window(window_name="f4")                
                elif page_flag:
                    temp = 'https://'+fingers4
                    browser.execute_script(f'''window.open("{temp}","f4");''')
                    tab_flag[4] = True
                else:                
                    browser.get("https://"+fingers4)
                    page_flag = True
                    tab_flag[4] = True
                counter = [0 for _ in range(6)]
        elif no_of_defects == 5:
            cv2.putText(current_frame,'5',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            counter[5] += 1
            if counter[5] == 20:
                browser.close()             #closing a website
                counter = [0 for _ in range(6)]            

        else :
            cv2.putText(current_frame,'none',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        cv2.imshow('current_frame',current_frame)
    except:
        pass


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
