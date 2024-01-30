import customtkinter
import subprocess
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def login():
    root.withdraw()
    subprocess.run(['python', './login.py'])

def signup():
    root.withdraw()
    subprocess.run(['python', './signup.py'])
    
root = customtkinter.CTk()
root.geometry("400x450")
mainframe = customtkinter.CTkFrame(master = root)
title = customtkinter.CTkLabel(master = mainframe, text = "ProduGy" , font = ("Roboto", 60))
loginButton = customtkinter.CTkButton(master = mainframe, text = "Login", font = ("Roboto", 25), command = login)
signUpButton = customtkinter.CTkButton(master = mainframe, text = "Sign Up", font = ("Roboto", 25), command = signup)
mainframe.pack(pady = 20, padx = 60, fill = "both", expand = True)
title.place(relx = 0.10, rely = 0.1)
loginButton.place(relx = 0.25, rely = 0.6)
signUpButton.place(relx = 0.25, rely = 0.75)
root.mainloop()