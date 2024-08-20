import cv2
import pyautogui
import pydirectinput
import time
import socket
from playsound import playsound

def matchTemplate(img, template):
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val = cv2.minMaxLoc(result)[0]
    thr = .05
    return min_val <= thr

def prepLua():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8888))
    clientsocket.send(b"Hello \n")
    sockCheck = True
    tempGame = ""
    while sockCheck:
        outMessage = clientsocket.recv(1024)
        sockCheck = False
    clientsocket.close()

def gameCheck():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8888))
    clientsocket.send(b"Hello \n")
    sockCheck = True
    tempGame = ""
    while sockCheck:
        outMessage = clientsocket.recv(1024)
        tempGame = str(outMessage.decode('utf-8')).replace("\n","").replace(" ","")
        print(tempGame + " detected.")
        sockCheck = False
    clientsocket.close()
    if("Ruby" in tempGame): return "Ruby"
    elif("Sapphire" in tempGame): return "Sapphire"
    elif("FireRed" in tempGame): return "Fire Red"
    elif("LeafGreen" in tempGame): return "Leaf Green"
    elif("Emerald" in tempGame): return "Emerald"
    else: return ""

# Horizontal, Vertical, Acro
mode = input("Please enter your RE mode: ").lower()

prepLua()
stream = True
counter = 0
firstPass = True
game = gameCheck()

if(game == "Ruby" or game == "Sapphire"):
    leftTemplate = cv2.imread("./assets/fightBoxRS.png")
    rightTemplate = cv2.imread("./assets/fightBoxRightRS.png")
elif(game == "Fire Red" or game == "Leaf Green" or game == "Emerald"):
    leftTemplate = cv2.imread("./assets/fightBox.png")
    rightTemplate = cv2.imread("./assets/fightBoxRight.png")


time.sleep(5)
pydirectinput.keyDown("enter")
pydirectinput.press("left")
pydirectinput.keyUp("enter")
print("Prep finished, script is starting.")

while(stream):

    if(mode == "horizontal"):
        pydirectinput.keyDown("x")
        pydirectinput.keyDown("left")
        time.sleep(1.5)
        pydirectinput.keyUp("left")
        pydirectinput.keyDown("right")
        time.sleep(1.5)
        pydirectinput.keyUp("x")
        pydirectinput.keyUp("right")
    elif(mode == "vertical"):
        pydirectinput.keyDown("x")
        pydirectinput.keyDown("up")
        time.sleep(1.5)
        pydirectinput.keyUp("up")
        pydirectinput.keyDown("down")
        time.sleep(1.5)
        pydirectinput.keyUp("x")
        pydirectinput.keyUp("down")
    elif(mode == "acro" and (game == "Ruby" or game == "Sapphire" or game == "Emerald")):
        pydirectinput.keyDown("x")
        time.sleep(5)
        pydirectinput.keyUp("x")
    elif(mode == "acro" and (game != "Ruby" or game != "Sapphire" or game != "Emerald")):
        stream = False
    else:
        stream = False

    pyautogui.screenshot("test.png")
    if(matchTemplate(cv2.imread("test.png"),leftTemplate) or matchTemplate(cv2.imread("test.png"),rightTemplate)):
        counter = counter + 1
        sockCheck = True
        print("Found a match. Checking for SID.")
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 8888))
        clientsocket.send(b"Hello \n")
        while sockCheck:
            outMessage = clientsocket.recv(1024)
            print("The shiny ID is " + str(outMessage.decode('utf-8')).replace("\n","") + ". This was attempt " + str(counter) + ".")
            sid = int(outMessage.decode('utf-8'))
            sockCheck = False
        clientsocket.close()
        if(sid < 8):
            playsound("./assets/shinysound.mp3",block=False)
            print("Congratulations! You have found a shiny!")
            time.sleep(5)
            stream = False
        else:
            pydirectinput.press("right")
            time.sleep(.25)
            pydirectinput.press("down")
            time.sleep(.25)
            pydirectinput.press("z")
            time.sleep(.25)
    else:
        print("No Screenshot found in this cycle. Continuing.")