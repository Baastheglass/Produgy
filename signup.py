import customtkinter
import subprocess
import threading
import time
from pydub import AudioSegment
from pydub.playback import play
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

positiveAffirmationCheck = False
andrewTateQuoteCheck = False
wrongAnswer = AudioSegment.from_mp3("./sfx/wrong-answer.mp3")
login = AudioSegment.from_mp3("./sfx/login.mp3")
def signUp():
    un = userName.get()
    ps1 = passWord.get()
    ps2 = passWord2.get()
    global labelPlaced
    labelPlaced = False
    if(andrewTateQuoteCheck == False and positiveAffirmationCheck == False):
        if(labelPlaced == True):
            errorLabel.place_forget()
            labelPlaced = False
        errorLabel.configure(text = "You must select atleast one option", font = ("Roboto", 16))
        errorLabel.place(relx = 0.055, rely = 0.29)
        play(wrongAnswer)
        return
    elif(andrewTateQuoteCheck == True and positiveAffirmationCheck == True):
        print("if entered")
        if(labelPlaced == True):
            errorLabel.place_forget()
            labelPlaced = False
        errorLabel.configure(text = "You cannot select both options", font = ("Roboto", 18))
        errorLabel.place(relx = 0.04, rely = 0.29)
        play(wrongAnswer)
        return
    if(not(len(userName.get()) == 0 or len(passWord.get()) == 0 or len(passWord2.get()) == 0)):
        if(passWord.get() == passWord2.get()):
            userFile = open("usernames.txt", "r")
            usernames = []
            usernameFound = False
            for i in userFile:
                usernames.append(i.strip())
            for fileUserName in usernames:
                if(fileUserName == userName.get()):
                    usernameFound = True
            if(usernameFound == False):
                if(len(usernames) == 0):
                    userFile = open("usernames.txt", "w")
                    passFile = open("passwords.txt", "w")
                    choiceFile = open("choiceOfQuote.txt", "w")
                    taskFile = open("tasks.txt", "w")
                    pomodoroFile = open("pomodoros.txt", "w")
                    userFile.write(userName.get())
                    passFile.write(passWord.get())
                    taskFile.write("0")
                    pomodoroFile.write("0")
                    if(andrewTateQuoteCheck == True):
                        choiceFile.write("AndrewTateQuote")
                    else:
                        choiceFile.write("positiveAffirmation")
                else:
                    userFile = open("usernames.txt", "a")
                    passFile = open("passwords.txt", "a")
                    choiceFile = open("choiceOfQuote.txt", "a")
                    taskFile = open("tasks.txt", "a")
                    pomodoroFile = open("pomodoros.txt", "a")
                    userFile.write('\n' + userName.get())
                    passFile.write('\n' + passWord.get())
                    taskFile.write('\n' + "0")
                    pomodoroFile.write('\n' + "0")
                    if(andrewTateQuoteCheck == True):
                        choiceFile.write('\n' + "AndrewTateQuote")
                    else:
                        choiceFile.write('\n' + "positiveAffirmation")
                userFile.close()
                passFile.close()
                choiceFile.close()
                taskFile.close()
                pomodoroFile.close()
                play(login)
                root.withdraw()
                subprocess.run(['python', './login.py'])
            else:
                if(labelPlaced == True):
                    errorLabel.place_forget()
                    labelPlaced = False
                errorLabel.configure(text = "This username is already in use", font = ("Roboto", 18))
                errorLabel.place(relx = 0.04, rely = 0.29)
                play(wrongAnswer)
                return  
        else:
            if(labelPlaced == True):
                errorLabel.place_forget()
                labelPlaced = False
            errorLabel.configure(text = "Passwords do not match", font = ("Roboto", 18))
            errorLabel.place(relx = 0.145, rely = 0.29)
            play(wrongAnswer)          
    else:
        if(labelPlaced == True):
                errorLabel.place_forget()
                labelPlaced = False    
        errorLabel.configure(text = "Fill out all the fields", font = ("Roboto", 18))
        errorLabel.place(relx = 0.225, rely = 0.29)
        play(wrongAnswer)
    
def andrewTateQuote():
    print("Andrew function")
    global andrewTateQuoteCheck
    andrewTateQuoteCheck = True

def positiveAffirmations():
    print("positive function")
    global positiveAffirmationCheck
    positiveAffirmationCheck = True
        
root = customtkinter.CTk()    
root.geometry("400x450")
frame = customtkinter.CTkFrame(master = root)
errorLabel = customtkinter.CTkLabel(master = frame)
title = customtkinter.CTkLabel(master = frame, text = "Sign-Up", font = ("Roboto", 50))
userName = customtkinter.CTkEntry(master = frame)
enterUser = customtkinter.CTkLabel(master = frame, text = "Enter Username: ")
passWord = customtkinter.CTkEntry(master = frame, show = "*")
enterPassword = customtkinter.CTkLabel(master = frame, text = "Enter Password: ")
passWord2 = customtkinter.CTkEntry(master = frame, show = "*")
enterPassword2 = customtkinter.CTkLabel(master = frame, text = "Confirm Password: ")
positiveAffirmation = customtkinter.CTkLabel(master = frame, text = "Positive Affirmations ")
positiveAffirmationsButton = customtkinter.CTkCheckBox(master = frame, text = None, command = positiveAffirmations)

andrewTateQuotes = customtkinter.CTkLabel(master = frame, text = "Andrew Tate Quotes ")
andrewTateQuotesButton = customtkinter.CTkCheckBox(master = frame, text = None, command = andrewTateQuote)

signUpButton = customtkinter.CTkButton(master = frame, text = "Sign Up", font = ("Roboto", 20), command = signUp)

frame.pack(pady = 20, padx = 60, fill = "both", expand = True)
title.place(relx = 0.20, rely = 0.1)
userName.place(relx = 0.4, rely = 0.40)
enterUser.place(relx = 0.01, rely = 0.40)
passWord.place(relx = 0.4, rely = 0.50)
enterPassword.place(relx = 0.01, rely = 0.50)
passWord2.place(relx = 0.45, rely = 0.60)
enterPassword2.place(relx = 0.01, rely = 0.60)
positiveAffirmation.place(relx = 0.01, rely = 0.70)
positiveAffirmationsButton.place(relx = 0.5, rely = 0.7)
andrewTateQuotes.place(relx = 0.01, rely = 0.8)
andrewTateQuotesButton.place(relx = 0.5, rely = 0.8)
signUpButton.place(relx = 0.25, rely = 0.9)    
root.mainloop()