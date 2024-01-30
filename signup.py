import customtkinter
import subprocess
import threading
import time
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def signUp():
    un = userName.get()
    ps1 = passWord.get()
    ps2 = passWord2.get()
    global labelPlaced
    labelPlaced = False
    if(not(len(userName.get()) == 0 or len(passWord.get()) == 0 or len(passWord2.get()) == 0)):
        print("if num1")
        if(passWord.get() == passWord2.get()):
            #print("if entered")
            userFile = open("usernames.txt", "a")
            passFile = open("passwords.txt", "a")
            userFile.write('\n' + userName.get())
            passFile.write('\n' + passWord.get())
            userFile.close()
            passFile.close()
            root.withdraw()
            subprocess.run(['python', './login.py'])
        else:
            if(labelPlaced == True):
                errorLabel.place_forget()
                labelPlaced = False
            errorLabel.configure(text = "Passwords do not match", font = ("Roboto", 18))
            errorLabel.place(relx = 0.145, rely = 0.82)          
    else:
        if(labelPlaced == True):
                errorLabel.place_forget()
                labelPlaced = False    
        errorLabel.configure(text = "Fill out all the fields", font = ("Roboto", 18))
        errorLabel.place(relx = 0.225, rely = 0.82)

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
signUpButton = customtkinter.CTkButton(master = frame, text = "Sign Up", font = ("Roboto", 20), command = signUp)
frame.pack(pady = 20, padx = 60, fill = "both", expand = True)
title.place(relx = 0.20, rely = 0.1)
userName.place(relx = 0.4, rely = 0.50)
enterUser.place(relx = 0.01, rely = 0.50)
passWord.place(relx = 0.4, rely = 0.60)
enterPassword.place(relx = 0.01, rely = 0.60)
passWord2.place(relx = 0.45, rely = 0.70)
enterPassword2.place(relx = 0.01, rely = 0.70)
signUpButton.place(relx = 0.25, rely = 0.9)    
root.mainloop()