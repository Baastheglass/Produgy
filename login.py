import customtkinter
import subprocess
import string
from pydub import AudioSegment
from pydub.playback import play

wrongAnswer = AudioSegment.from_mp3("./sfx/wrong-answer.mp3")
loginSound = AudioSegment.from_mp3("./sfx/login.mp3")
wrongPlaced = False

def login():
    userName = entry1.get()
    passWord = entry2.get()
    userFile = open("usernames.txt", "r")
    userNames = []
    passWords = []
    for i in userFile:
        userNames.append(i.strip())
    userFile.close()
    passFile = open("passwords.txt", "r")
    for i in passFile:
        passWords.append(i.strip())
    passFile.close()
    index = 0
    for i in userNames:
        print("File username:" + i)
        print("Textbox username:" + userName)
        print("File password:" + passWords[index])
        print("Textbox password:" + passWord)
        if(i == userName and passWords[index] == passWord):
            print("First if entered")
            if(checkbox.get() == True):
                rememberedCred = open("rememberedCredentials.txt", "w")
                rememberedCred.write(userName + '\n')
                rememberedCred.write(passWord)
                rememberedCred.close()
            print("Potty emitted")
            indexFile = open("currentindex.txt", "w")
            indexFile.write(str(index))
            play(loginSound)
            global wrongPlaced
            if(wrongPlaced == True):
                wrongLabel.place_forget()
            root.withdraw()
            subprocess.run(['python', './mainappy.py'])
            print("Subprocess ran")
        index = index + 1
        
    #print("Butt")
    play(wrongAnswer)
    wrongPlaced = True
    wrongLabel.place(relx = 0.215, rely = 0.92)
    return
    
            
#window
oldCred = []
remCred = open("rememberedCredentials.txt", "r")
runLogin = True
for i in remCred:
    oldCred.append(i)
if(len(oldCred) != 0):
    runLogin = False
    play(loginSound)
    subprocess.run(['python', './mainappy.py'])
if(runLogin == True):
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root = customtkinter.CTk()
    root.geometry("400x450")
    frame = customtkinter.CTkFrame(master = root)
    frame.pack(pady = 20, padx = 60, fill = "both", expand = True)
    label = customtkinter.CTkLabel(master = frame, text = "Login", font = ("Roboto", 60))
    label.pack(pady = 20, padx = 10)
    entry1 = customtkinter.CTkEntry(master = frame, placeholder_text="Username")
    entry1.pack(pady = 20, padx = 10)
    
    entry2 = customtkinter.CTkEntry(master = frame, placeholder_text="Password", show = "*")
    entry2.pack(pady = 20, padx = 10)
    button = customtkinter.CTkButton(master = frame, text = "Login", command = login)
    button.pack(pady = 20, padx = 10)

    checkbox = customtkinter.CTkCheckBox(master = frame, text = "Remember Me")
    checkbox.pack(pady = 20, padx = 10)
    wrongLabel = customtkinter.CTkLabel(master = frame, text = "Wrong credentials", font = ("Roboto", 20))
    root.mainloop()
