import numpy as np 
import cv2 
import time
import requests

# Constant REST API attributes
token = "patsV7k97MlTegAKp.6d88b5944a91a30b25a372cde590b5d4e6fe94c4afaa10b1a21eb6fbcdb04549"
url = "https://api.airtable.com/v0/apphONQQbp3lZsxcN/Thermometer"
headers = {
    "Authorization": "Bearer " + token,
    'Content-Type': 'application/json',
}

unit = "f"

# Function to update Airtable value
def doPatch(unit):
    data = {"records": [{"id": "rec8VqwIFGb9AMTaP","fields": {"Unit": unit}}]}
    response = requests.patch(url, json=data, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print('New record created:', data)
    else:
        print(f"Request failed with status code {response.status_code}")

# Function to toggle unit and avoid overload of API calls
def unitToggle(color):
    global unit
    if color == "green" and unit == "f":
        doPatch("Celsius")
        unit = "c"
    elif color == "red" and unit == "c":
        doPatch("Fahrenheit")
        unit = "f"

# Capturing video through webcam 
webcam = cv2.VideoCapture(1) 

# Main Loop
while True: 
	# Get image from webcam
    _, imageFrame = webcam.read() 
    # Convert image to HSV color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

	# Red color HSV threshold
    red_lower = np.array([145, 80, 80], np.uint8) 
    red_upper = np.array([180, 255, 230], np.uint8)
    red_lower1 = np.array([0, 180, 100], np.uint8) 
    red_upper1 = np.array([6, 255, 230], np.uint8)  
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    red_mask1 = cv2.inRange(hsvFrame, red_lower1, red_upper1)  
    red_mask = red_mask + red_mask1

	# Green color HSV threshold
    green_lower = np.array([25, 80, 80], np.uint8) 
    green_upper = np.array([90, 255, 230], np.uint8) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

	# Creating contour to track red color 
    contoursR, hierarchyR = cv2.findContours(red_mask, 
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 
    # Optional include raw contours for debugging of color thresholds:
    #imageFrame = cv2.drawContours(imageFrame, contours, -1, (0,0,255), 3)

    # Creating contour to track green color 
    contoursG, hierarchyG = cv2.findContours(green_mask, 
										cv2.RETR_TREE, 
										cv2.CHAIN_APPROX_SIMPLE) 
    # Optional include raw contours for debugging of color thresholds:
    #imageFrame = cv2.drawContours(imageFrame, contours, -1, (0,255,0), 3)

    maxIndexR = -1
    maxAreaR = 0

    for pic, contour in enumerate(contoursR): 
        area = cv2.contourArea(contour) 
        if maxIndexR == -1:
            maxIndexR = pic
            maxAreaR = area
        else:
            if area > maxAreaR:
                maxIndexR = pic
                maxAreaR = area

    maxIndexG = -1
    maxAreaG = 0

    for pic, contour in enumerate(contoursG): 
        area = cv2.contourArea(contour) 
        if maxIndexG == -1:
            maxIndexG = pic
            maxAreaG = area
        else:
            if area > maxAreaG:
                maxIndexG = pic
                maxAreaG = area

    if (maxAreaG > maxAreaR) and maxAreaG > 8000:
        x, y, w, h = cv2.boundingRect(contoursG[maxIndexG]) 
        imageFrame = cv2.rectangle(imageFrame, (x, y), 
									(x + w, y + h), 
									(0, 255, 0), 5) 
			
        cv2.putText(imageFrame, "Green -> Celsius", (x, y), 
						cv2.FONT_HERSHEY_SIMPLEX, 
						2.0, (0, 255, 0))
        unitToggle("green")
    elif (maxAreaR > maxAreaG) and maxAreaR > 8000:
        x, y, w, h = cv2.boundingRect(contoursR[maxIndexR]) 
        imageFrame = cv2.rectangle(imageFrame, (x, y), 
									(x + w, y + h), 
									(0, 0, 255), 5) 
			
        cv2.putText(imageFrame, "Red -> Fahrenheit", (x, y), 
						cv2.FONT_HERSHEY_SIMPLEX, 
						2.0, (0, 0, 255))
        unitToggle("red")
			
    time.sleep(0.01)
    
    # Program Termination 
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame) 
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        cap.release() 
        cv2.destroyAllWindows() 
        break
