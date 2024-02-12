import customtkinter
import time
import threading
import datetime
import subprocess 
from ultralytics import YOLO
import cv2
from pydub import AudioSegment
from pydub.playback import play

timerSound = AudioSegment.from_mp3("./sfx/done.mp3")
doneSound = AudioSegment.from_mp3("./sfx/taskfin.mp3")
model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
threads = []
stopTimer = threading.Event()
stopTimer.clear()

def playTimerStart():
    play(timerSound)
    return
def playDoneSound():
    play(doneSound)
    return

threads.append(threading.Thread(target = playTimerStart)) #index 0 is timerStart
threads.append(threading.Thread(target = playDoneSound)) #index 1 is doneSound
detect = False

def on_close():
    print("On close entered")
    if(cap.isOpened()):
            cap.release()
            cv2.destroyAllWindows()
    print("Cap destroyed")
    stopTimer.set()
    print("Timer stopped")
    root.destroy()
            
def checkDay():
    today = datetime.datetime.today()
    if(today.weekday() == 0 and displayed != True):
        dayisNow = True
    else:
        dayisNow = False
    if(dayisNow == True):
        subprocess.run(['python', './weeklyReview.py'])
        dayisNow = False

def horseDetection():
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            results = model(frame)
            #check for horse
            for result in results:
                for classvalue in result.boxes.cls:
                    if(classvalue.item() == 17):
                        print("HORSE FOUND")
                        cap.release()
                        cv2.destroyAllWindows()
                        break
                    else:
                        print("HORSE NOT FOUND")
                        cap.release()
                        cv2.destroyAllWindows()
                        break
    return
            
def runWeeklyReview():
    global displayed
    displayed = False
    if(dayisNow == True):
        subprocess.run(['python', './weeklyReview.py'])
        dayisNow = False
        displayed = True
    file = open("./pomodoros.txt", "w")
    file.write("0")
    file.close()
    file = open("./tasks.txt", "w")
    file.write("0")
    file.close()

def checkTrue():
    global detect
    if(detect == False):
        detect = True
        objectDetectButton.configure(bg_color = "gray", fg_color = "gray")
        objectDetectButton._hover_color = "black"
    else:
        detect = False
        objectDetectButton.configure(bg_color = originalBackColour, fg_color = originalForeColour)
        objectDetectButton._hover_color = originalHoverColour
    
def timerStart():
    threads[0].start()
    customtkinter.set_appearance_mode("light")
    t = int(enterTime.get())
    duration = t * 60
    start_time = time.time()    
    #progressBar.start()
    if(detect == True):
        model = YOLO('yolov8n.pt')
        cap = cv2.VideoCapture(0)
        progressBar.start()
        while(((time.time() - start_time) < duration) and cap.isOpened()):
            #progressBar.start()
            success, frame = cap.read()
            personDetected = False
            if success:
                # Run YOLOv8 inference on the frame
                results = model(frame)
                #check for phone
                for result in results:
                    for classvalue in result.boxes.cls:
                        if(classvalue.item() == 67):
                            print("CELLPHONE FOUND")
                        elif(classvalue.item() == 0):
                            personDetected = True
                if(personDetected == False):
                    print("Person not found")
        cap.release()
        cv2.destroyAllWindows()
    else:
        progressBar.start()
        while(((time.time() - start_time) < duration)):
            print("Pomodoro ongoing")
        print("While ended")
    progressBar.stop()
    # file = open("./pomodoros.txt", "r")
    # indexFile = open("./currentindex.txt", "r")
    # index = indexFile.read()
    # index.strip()
    # print(index)
    # index = int(index)
    # print(index)
    # pomodoroNum = file.read()
    # print(pomodoroNum[index - 1])
    # pomodoroNum[index - 1] = int(pomodoroNum[index - 1]) + 1
    # file.close()
    # file = open("./pomodoros.txt", "w")
    # file.write(pomodoroNum)
    # file.close()
    customtkinter.set_appearance_mode("dark")

def threadTimer():
    threads.append(threading.Thread(target = timerStart))
    threads[2].start()    

def done15():
    play(doneSound)
    label15.configure(bg_color = "green")
    tickbutton15.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del15)
    tickbutton15._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc15():
    global label15
    label15 = customtkinter.CTkLabel(master = frame, text = task15.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task15.place_forget()
    tickbutton15.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done15)
    tickbutton15._hover_color = "#32A86F"
    label15.place(relx = 0, rely = 0.94)

def del15():
    label15.place_forget()
    task15.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task15.delete(0, 'end')
    tickbutton15.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc15)
    tickbutton15._hover_color = originalHoverColour
    tickbutton15.place(relx = 0.785, rely = 0.94)
    task15.place(relx = 0, rely = 0.94)

def done14():
    play(doneSound)
    label14.configure(bg_color = "green")
    tickbutton14.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del14)
    tickbutton14._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc14():
    global task15
    task15 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton15
    tickbutton15 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc15)        
    global label14
    label14 = customtkinter.CTkLabel(master = frame, text = task14.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task14.place_forget()
    tickbutton14.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done14)
    tickbutton14._hover_color = "#32A86F"
    label14.place(relx = 0, rely = 0.88)
    task15.place(relx = 0, rely = 0.94)
    tickbutton15.place(relx = 0.785, rely = 0.94)

def del14():
    label14.place_forget()
    task14.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task14.delete(0, 'end')
    tickbutton14.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc14)
    tickbutton14._hover_color = originalHoverColour
    tickbutton14.place(relx = 0.785, rely = 0.88)
    task14.place(relx = 0, rely = 0.88)

def done13():
    play(doneSound)
    label13.configure(bg_color = "green")
    tickbutton13.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del13)
    tickbutton13._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc13():
    global task14
    task14 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton14
    tickbutton14 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc14)        
    global label13
    label13 = customtkinter.CTkLabel(master = frame, text = task13.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task13.place_forget()
    tickbutton13.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done13)
    tickbutton13._hover_color = "#32A86F"
    label13.place(relx = 0, rely = 0.82)
    task14.place(relx = 0, rely = 0.88)
    tickbutton14.place(relx = 0.785, rely = 0.88)

def del13():
    label13.place_forget()
    task13.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task13.delete(0, 'end')
    tickbutton13.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc13)
    tickbutton13._hover_color = originalHoverColour
    tickbutton13.place(relx = 0.785, rely = 0.82)
    task13.place(relx = 0, rely = 0.82)

def done12():
    play(doneSound)
    label12.configure(bg_color = "green")
    tickbutton12.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del12)
    tickbutton12._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc12():
    global task13
    task13 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton13
    tickbutton13 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc13)        
    global label12
    label12 = customtkinter.CTkLabel(master = frame, text = task12.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task12.place_forget()
    tickbutton12.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done12)
    tickbutton12._hover_color = "#32A86F"
    label12.place(relx = 0, rely = 0.76)
    task13.place(relx = 0, rely = 0.82)
    tickbutton13.place(relx = 0.785, rely = 0.82)

def del12():
    label12.place_forget()
    task12.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task12.delete(0, 'end')
    tickbutton12.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc12)
    tickbutton12._hover_color = originalHoverColour
    tickbutton12.place(relx = 0.785, rely = 0.76)
    task12.place(relx = 0, rely = 0.76)

def done11():
    play(doneSound)
    label11.configure(bg_color = "green")
    tickbutton11.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del11)
    tickbutton11._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc11():
    global task12
    task12 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton12
    tickbutton12 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc12)        
    global label11
    label11 = customtkinter.CTkLabel(master = frame, text = task11.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task11.place_forget()
    tickbutton11.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done11)
    tickbutton11._hover_color = "#32A86F"
    label11.place(relx = 0, rely = 0.70)
    task12.place(relx = 0, rely = 0.76)
    tickbutton12.place(relx = 0.785, rely = 0.76)

def del11():
    label11.place_forget()
    task11.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task11.delete(0, 'end')
    tickbutton11.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc11)
    tickbutton11._hover_color = originalHoverColour
    tickbutton11.place(relx = 0.785, rely = 0.70)
    task11.place(relx = 0, rely = 0.70)

def done10():
    play(doneSound)
    label10.configure(bg_color = "green")
    tickbutton10.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del10)
    tickbutton10._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc10():
    global task11
    task11 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton11
    tickbutton11 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc11)        
    global label10
    label10 = customtkinter.CTkLabel(master = frame, text = task10.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task10.place_forget()
    tickbutton10.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done10)
    tickbutton10._hover_color = "#32A86F"
    label10.place(relx = 0, rely = 0.64)
    task11.place(relx = 0, rely = 0.70)
    tickbutton11.place(relx = 0.785, rely = 0.70)

def del10():
    label10.place_forget()
    task10.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task10.delete(0, 'end')
    tickbutton10.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc10)
    tickbutton10._hover_color = originalHoverColour
    tickbutton10.place(relx = 0.785, rely = 0.64)
    task10.place(relx = 0, rely = 0.64)

def done9():
    play(doneSound)
    label9.configure(bg_color = "green")
    tickbutton9.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del9)
    tickbutton9._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc9():
    global task10
    task10 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton10
    tickbutton10 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc10)        
    global label9
    label9 = customtkinter.CTkLabel(master = frame, text = task9.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task9.place_forget()
    tickbutton9.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done9)
    tickbutton9._hover_color = "#32A86F"
    label9.place(relx = 0, rely = 0.58)
    task10.place(relx = 0, rely = 0.64)
    tickbutton10.place(relx = 0.785, rely = 0.64)

def del9():
    label9.place_forget()
    task9.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task9.delete(0 ,'end')
    tickbutton9.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc9)
    tickbutton9._hover_color = originalHoverColour
    tickbutton9.place(relx = 0.785, rely = 0.58)
    task9.place(relx = 0, rely = 0.58)

def done8():
    play(doneSound)
    label8.configure(bg_color = "green")
    tickbutton8.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del8)
    tickbutton8._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc8():
    global task9
    task9 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton9
    tickbutton9 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc9)        
    global label8
    label8 = customtkinter.CTkLabel(master = frame, text = task8.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task8.place_forget()
    tickbutton8.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done8)
    tickbutton8._hover_color = "#32A86F"
    label8.place(relx = 0, rely = 0.52)
    task9.place(relx = 0, rely = 0.58)
    tickbutton9.place(relx = 0.785, rely = 0.58)

def del8():
    label8.place_forget()
    task8.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task8.delete(0, 'end')
    tickbutton8.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc8)
    tickbutton8._hover_color = originalHoverColour
    tickbutton8.place(relx = 0.785, rely = 0.52)
    task8.place(relx = 0, rely = 0.52)

def done7():
    play(doneSound)
    label7.configure(bg_color = "green")
    tickbutton7.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del7)
    tickbutton7._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc7():
    global task8
    task8 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton8
    tickbutton8 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc8)        
    global label7
    label7 = customtkinter.CTkLabel(master = frame, text = task7.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task7.place_forget()
    tickbutton7.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done7)
    tickbutton7._hover_color = "#32A86F"
    label7.place(relx = 0, rely = 0.46)
    task8.place(relx = 0, rely = 0.52)
    tickbutton8.place(relx = 0.785, rely = 0.52)

def del7():
    label7.place_forget()
    task7.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task7.delete(0, 'end')
    tickbutton7.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc7)
    tickbutton7._hover_color = originalHoverColour
    tickbutton7.place(relx = 0.785, rely = 0.46)
    task7.place(relx = 0, rely = 0.46)

def done6():
    play(doneSound)
    label6.configure(bg_color = "green")
    tickbutton6.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del6)
    tickbutton6._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc6():
    global task7
    task7 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton7
    tickbutton7 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc7)        
    global label6
    label6 = customtkinter.CTkLabel(master = frame, text = task6.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task6.place_forget()
    tickbutton6.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done6)
    tickbutton6._hover_color = "#32A86F"
    label6.place(relx = 0, rely = 0.40)
    task7.place(relx = 0, rely = 0.46)
    tickbutton7.place(relx = 0.785, rely = 0.46)

def del6():
    label6.place_forget()
    task6.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task6.delete(0, 'end')
    tickbutton6.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc6)
    tickbutton6._hover_color = originalHoverColour
    tickbutton6.place(relx = 0.785, rely = 0.40)
    task6.place(relx = 0, rely = 0.40)

def done5():
    play(doneSound)
    label5.configure(bg_color = "green")
    tickbutton5.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del5)
    tickbutton5._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc5():
    global task6
    task6 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton6
    tickbutton6 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc6)        
    global label5
    label5 = customtkinter.CTkLabel(master = frame, text = task5.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task5.place_forget()
    tickbutton5.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done5)
    tickbutton5._hover_color = "#32A86F"
    label5.place(relx = 0, rely = 0.34)
    task6.place(relx = 0, rely = 0.40)
    tickbutton6.place(relx = 0.785, rely = 0.40)

def del5():
    label5.place_forget()
    task5.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task5.delete(0, 'end')
    tickbutton5.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc5)
    tickbutton5._hover_color = originalHoverColour
    tickbutton5.place(relx = 0.785, rely = 0.34)
    task5.place(relx = 0, rely = 0.34)

def done4():
    play(doneSound)
    label4.configure(bg_color = "green")
    tickbutton4.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del4)
    tickbutton4._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc4():
    global task5
    task5 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton5
    tickbutton5 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc5)        
    global label4
    label4 = customtkinter.CTkLabel(master = frame, text = task4.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task4.place_forget()
    tickbutton4.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done4)
    tickbutton4._hover_color = "#32A86F"
    label4.place(relx = 0, rely = 0.28)
    task5.place(relx = 0, rely = 0.34)
    tickbutton5.place(relx = 0.785, rely = 0.34)

def del4():
    label4.place_forget()
    task4.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task4.delete(0, 'end')
    tickbutton4.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc4)
    tickbutton4._hover_color = originalHoverColour
    tickbutton4.place(relx = 0.785, rely = 0.28)
    task4.place(relx = 0, rely = 0.28)

def done3():
    play(doneSound)
    label3.configure(bg_color = "green")
    tickbutton3.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del3)
    tickbutton3._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc3():
    global task4
    task4 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton4
    tickbutton4 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc4)        
    global label3
    label3 = customtkinter.CTkLabel(master = frame, text = task3.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task3.place_forget()
    tickbutton3.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done3)
    tickbutton3._hover_color = "#32A86F"
    label3.place(relx = 0, rely = 0.22)
    task4.place(relx = 0, rely = 0.28)
    tickbutton4.place(relx = 0.785, rely = 0.28)

def del3():
    label3.place_forget()
    task3.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task3.delete(0, 'end')
    tickbutton3.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc3)
    tickbutton3._hover_color = originalHoverColour
    tickbutton3.place(relx = 0.785, rely = 0.22)
    task3.place(relx = 0, rely = 0.22)

def done2():
    play(doneSound)
    label2.configure(bg_color = "green")
    tickbutton2.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del2)
    tickbutton2._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc2():
    global task3
    task3 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    global tickbutton3
    tickbutton3 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc3)        
    global label2
    label2 = customtkinter.CTkLabel(master = frame, text = task2.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task2.place_forget()
    tickbutton2.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done2)
    tickbutton2._hover_color = "#32A86F"
    label2.place(relx = 0, rely = 0.16)
    task3.place(relx = 0, rely = 0.22)
    tickbutton3.place(relx = 0.785, rely = 0.22)

def del2():
    label2.place_forget()
    task2.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task2.delete(0, 'end')
    tickbutton2.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc2)
    tickbutton2._hover_color = originalHoverColour
    tickbutton2.place(relx = 0.785, rely = 0.16)
    task2.place(relx = 0, rely = 0.16)

def done1():
    play(doneSound)
    label1.configure(bg_color = "green")
    tickbutton1.configure(text = "DEL", bg_color = "red", fg_color = "red", width = 20, font = ("Roboto", 27), command = del1)
    tickbutton1._hover_color = "#A83246"
    file = open("./tasks.txt", "r")
    tasksNum = file.read()
    file.close()
    int(tasksNum)
    tasksNum = int(tasksNum) + 1
    file = open("./tasks.txt", "w")
    file.write(str(tasksNum))
    file.close()
    
def addFunc1():
    print("In")
    global task2
    task2 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray") 
    global tickbutton2
    tickbutton2 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command = addFunc2)
    global label1
    label1 = customtkinter.CTkLabel(master = frame, text = task1.get(), height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    print("Widgets created")
    task1.place_forget()
    tickbutton1.configure(text = "DONE", width = 20, font = ("Roboto", 19), bg_color = "green", fg_color = "green", command = done1)
    tickbutton1._hover_color = "#32A86F"
    print("Tickbutton configured")
    label1.place(relx = 0, rely = 0.10)
    task2.place(relx = 0, rely = 0.16)
    tickbutton2.place(relx = 0.785, rely = 0.16)
    print("Executed")
    
def del1():
    label1.place_forget()
    task1.configure(height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
    task1.delete(0, 'end')
    tickbutton1.configure(text = "ADD", font = ("Roboto", 25), height = 40, width = 20, bg_color = originalBackColour, fg_color = originalForeColour, command = addFunc1)
    tickbutton1._hover_color = originalHoverColour
    tickbutton1.place(relx = 0.785, rely = 0.10)
    task1.place(relx = 0, rely = 0.1)
    

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("1366x768")
root.protocol("WM_DELETE_WINDOW", on_close)
frame = customtkinter.CTkFrame(master = root, height = 768, width = 315, bg_color = "black", corner_radius= 0)
task1 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton1 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20, command=addFunc1)
originalBackColour = tickbutton1._bg_color
originalForeColour = tickbutton1._fg_color
originalHoverColour = tickbutton1._hover_color
#task4 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
#tickbutton4 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task5 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton5 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task6 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton6 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task7 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton7 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task8 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton8 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task9 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton9 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task10 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton10 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task11 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton11 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task12 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton12 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task13 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton13 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task14 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton14 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
task15 = customtkinter.CTkEntry(master = frame, height = 40, width = 240, font = ("Roboto", 25), bg_color = "gray")
tickbutton15 = customtkinter.CTkButton(master = frame, text = "ADD", font = ("Roboto", 25), height = 40, width = 20)
check = False
objectDetectButton = customtkinter.CTkButton(master = root, text = "DETECT", font = ("Roboto", 25), height = 40, width = 20, command = checkTrue)
objectDetectButton.place(relx = 0.92, rely = 0.01)
horseDetectButton = customtkinter.CTkButton(master = root, text = "DETECT HORSE", font = ("Roboto", 20), height = 40, width = 20, command = horseDetection)
horseDetectButton.place(relx = 0.8, rely = 0.01)
tasks = []
tickbuttons = []
tasks.append(task1)
tickbuttons.append(tickbutton1)
#tasks.append(task2)
#tickbuttons.append(tickbutton2)
#tasks.append(task3)
#tickbuttons.append(tickbutton3)
#tasks.append(task4)
#tickbuttons.append(tickbutton4)
# tasks.append(task5)
# tickbuttons.append(tickbutton5)
# tasks.append(task6)
# tickbuttons.append(tickbutton6)
# tasks.append(task7)
# tickbuttons.append(tickbutton7)
# tasks.append(task8)
# tickbuttons.append(tickbutton8)
# tasks.append(task9)
# tickbuttons.append(tickbutton9)
# tasks.append(task10)
# tickbuttons.append(tickbutton10)
# tasks.append(task11)
# tickbuttons.append(tickbutton11)
# tasks.append(task12)
# tickbuttons.append(tickbutton12)
# tasks.append(task13)
# tickbuttons.append(tickbutton13)
# tasks.append(task14)
# tickbuttons.append(tickbutton14)
# tasks.append(task15)
# tickbuttons.append(tickbutton15)
#toggleStart()
progressBar = customtkinter.CTkProgressBar(root, height = 20, width = 900, indeterminate_speed = 0.1)
progressBar["maximum"] = 100
enterTimeLabel = customtkinter.CTkLabel(root, text = "Enter time: ", font = ("Roboto", 35))
enterTime = customtkinter.CTkEntry(root, font = ("Roboto", 30), width = 70)
tasksLabel = customtkinter.CTkLabel(frame, text = "Tasks", font = ("Roboto", 55))
start = customtkinter.CTkButton(root, text = "Start!", font = ("Roboto", 40), command = threadTimer)
frame.place(relx = 0, rely = 0)    
task1.place(relx = 0, rely = 0.10)
tickbutton1.place(relx = 0.785, rely = 0.10)
#task3.place(relx = 0, rely = 0.22)
#tickbutton3.place(relx = 0.785, rely = 0.22)
#task4.place(relx = 0, rely = 0.28)
#tickbutton4.place(relx = 0.785, rely = 0.28)
# task5.place(relx = 0, rely = 0.34)
# tickbutton5.place(relx = 0.785, rely = 0.34)
# task6.place(relx = 0, rely = 0.40)
# tickbutton6.place(relx = 0.785, rely = 0.40)
# task7.place(relx = 0, rely = 0.46)
# tickbutton7.place(relx = 0.785, rely = 0.46)
# task8.place(relx = 0, rely = 0.52)
# tickbutton8.place(relx = 0.785, rely = 0.52)
# task9.place(relx = 0, rely = 0.58)
# tickbutton9.place(relx = 0.785, rely = 0.58)
# task10.place(relx = 0, rely = 0.64)
# tickbutton10.place(relx = 0.785, rely = 0.64)
# task11.place(relx = 0, rely = 0.70)
# tickbutton11.place(relx = 0.785, rely = 0.70)
# task12.place(relx = 0, rely = 0.76)
# tickbutton12.place(relx = 0.785, rely = 0.76)
# task13.place(relx = 0, rely = 0.82)
# tickbutton13.place(relx = 0.785, rely = 0.82)
# task14.place(relx = 0, rely = 0.88)
# tickbutton14.place(relx = 0.785, rely = 0.88)
# task15.place(relx = 0, rely = 0.94)
# tickbutton15.place(relx = 0.785, rely = 0.94)
progressBar.set(0)
progressBar.place(relx = 0.28, rely = 0.75)
enterTimeLabel.place(relx = 0.50, rely = 0.8)
enterTime.place(relx = 0.63, rely = 0.8)
start.place(relx = 0.54, rely = 0.89)
tasksLabel.place(relx = 0.02, rely = 0.005)

checkDay()
root.mainloop()