import tkinter
import tkinter.ttk as tkink

def exitMw():
    exit()

def hideShow():
    if firstLabel.winfo_viewable():
        firstLabel.grid_remove()
    else:
        firstLabel.grid()

# Init main window
mainWindow = tkinter.Tk()
# Set minimum windows size  
mainWindow.minsize(600, 400)

okButton = tkinter.ttk.Button(mainWindow, text = "Exit", command = exitMw)
okButton.grid()
okButton.place(x = 510, y = 360)
okButton.focus()

hideButton = tkink.Button(mainWindow, text = "Hide\Show", command = hideShow)
hideButton.grid()
hideButton.place(x = 430, y = 360)

firstLabel = tkink.Label(text = "I am First Label :)")
firstLabel.grid()

mainWindow.mainloop()