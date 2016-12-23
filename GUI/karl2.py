# Karl Preisner
# December 23, 2016
# GUI for moving all four motors


from Tkinter import *
from PIL import Image, ImageTk
import time


# -------- Methods

def getButton():
	moveButton.grid(row = 4, column = 30, columnspan = 8) # place 'Move motor!' button

	if button_choice.get() == 1:
		unit_label.config(text = "degrees")
		messageBox.config(text = "Servo Gearbox:\n\n - Move the gearbox from its current position to the goal position entered\n    in the 'Value' field.\n\n - Range = [37, 154] degrees.")

	elif button_choice.get() == 2:
		unit_label.config(text = "degrees")
		messageBox.config(text = "Linear Actuator: middle:\n\n - Move the actuator from its current position to the goal position entered\n    in the 'Value' field.\n\n - Range = [0, 180] degrees.")

	elif button_choice.get() == 3:
		unit_label.config(text = "degrees")
		messageBox.config(text = "Linear Actuator: bottom:\n\n - Move the actuator from its current position to the goal position entered\n    in the 'Value' field.\n\n - Range = [0, 180] degrees.")

	elif button_choice.get() == 4:
		unit_label.config(text = "steps")
		messageBox.config(text = "Stepper motor:\n\n - Move the stepper motor the number of steps entered in the 'Value'\n    field.\n\n - Number of steps to revolve around the table = #### steps.")


def moveMotorButton(event):
	print "Move motor:", entry_field.get(), "degrees"
	statusLabel.config(text = "Status: Motor moving. Please wait...")
	root.update()

	# ***************/************\***************
	# *************/****************\*************
	# ***********/********************\***********

	# Call methods to move motors here.
	time.sleep(3) 
	# This simluates a motor moving.
	# ***********\********************/***********
	# *************\****************/*************
	# ***************\************/***************

	entry_field.selection_range(0, END) # highlight the text
	statusLabel.config(text = "")
	print "Move motor completed."





# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 				         Build GUI
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# -------- Main Window: root
root = Tk()
root.title("Camera Motors Demo")
root.minsize(width = 550, height = 500)
root.maxsize(width = 550, height = 500)



# -------- Image: 256x256
armLogo = ImageTk.PhotoImage(Image.open("arm_256x256.jpg"))
arm = Label(root, image = armLogo)
arm.grid(row = 0, column = 20, columnspan = 20, rowspan = 10, sticky = "nw", padx = 0, pady = 20)
# arm.pack(side = "top", fill = "both", expand = "yes")



# -------- Title Label
label1_text = "Select a motor to move."
label1 = Label(root, text = label1_text, fg = "blue", relief = "solid", bg = '#e6e6ff', borderwidth = 4, font = "Helvetica 18 bold")
label1.grid(row = 0, column = 0, rowspan = 2, columnspan = 20, sticky = "", pady = 20, padx = 20, ipadx = 10, ipady = 5)



# -------- Radio Buttons
button_choice = IntVar()

button1 = Radiobutton(root, text = "Servo Gearbox", variable = button_choice, value = 1, command = getButton, pady = 4)
button1.grid(row = 2, column = 3, columnspan = 12, sticky = "w")

button2 = Radiobutton(root, text = "Linear actuator: middle", variable = button_choice, value = 2, command = getButton, pady = 4)
button2.grid(row = 3, column = 3, columnspan = 15, sticky = "w")

button3 = Radiobutton(root, text = "Linear actuator: bottom", variable = button_choice, value = 3, command = getButton, pady = 4)
button3.grid(row = 4, column = 3, columnspan = 15, sticky = "w")

button4 = Radiobutton(root, text = "Stepper motor", variable = button_choice, value = 4, command = getButton, pady = 4)
button4.grid(row = 5, column = 3, columnspan = 12, sticky = "w")



# -------- Entry Field with Labels
label2 = Label(root, text = "Value:")
label2.grid(row = 6, column = 2, columnspan = 5, sticky = "w", pady = 10)

entry_field = Entry(root, width = 8)
entry_field.grid(row = 6, column = 5, columnspan = 6, sticky = "w", pady = 10)

unit_label = Label(root, text = "", fg = "blue")
unit_label.grid(row = 6, column = 11, columnspan = 7, sticky = "w", pady = 10)



# -------- Message Box 
messageBox = Message(root, text = "\n\n\n\n\n", width = 475, pady = 15)
messageBox.grid(row = 10, column = 2, rowspan = 8, columnspan = 40, sticky = "nw" )



# -------- Move Motor Button
moveButton = Button(root, text = "Move motor!")
moveButton.bind("<Button-1>", moveMotorButton)



# -------- Status Bar
statusLabel = Label(root, text = "", fg = "green3")
statusLabel.grid(row = 25, column = 19, columnspan = 18)






# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 				           Run GUI
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# Main Loop
root.mainloop()






