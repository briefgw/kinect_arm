# Karl Preisner
# December 23, 2016
# GUI class for moving all four motors

# motorDemo.py builds and runs this GUI.

from Tkinter import *
import tkFont
from PIL import Image, ImageTk # sudo pip install Pillow
import time


# Class motorGUI builds the GUI and has methods for button actions.
class motorGUI:

	def __init__(self, master): # constructor
		# This constructor method adds all components to the GUI.
		# It also has methods for button interactions. 
		master.title("Camera Arm Motors")
		master.minsize(width = 550, height = 500)
		master.maxsize(width = 550, height = 500)

		self.master = master
		# master.grid_propagate(False)

		# -------- Image: 256x256
		self.arm_Image = ImageTk.PhotoImage(Image.open("arm_256x256.jpg"))
		self.arm_Logo_Label = Label(master, image = self.arm_Image)
		self.arm_Logo_Label.grid(row = 0, column = 20, columnspan = 30, rowspan = 12, sticky = "w", padx = 30, pady = 10)

		# -------- Title Label
		self.title_Label = Label(master, text = "Camera Arm Motors", fg = "blue", relief = "solid", bg = '#e6e6ff', borderwidth = 4, font = "Helvetica 18 bold")
		self.title_Label.grid(row = 0, column = 0, rowspan = 2, columnspan = 20, pady = 20, padx = 20, ipadx = 10, ipady = 5)

		# -------- Instruction 1 Label
		self.instruction1_Label = Label(master, text = "Select a motor:", font = "Helvetica 15 bold underline", pady = 4)
		self.instruction1_Label.grid(row = 2, column = 2, columnspan = 12, sticky = "w")

		# -------- Radio Buttons
		self.button_choice = IntVar()

		self.button1 = Radiobutton(master, text = "Servo Gearbox", variable = self.button_choice, value = 1, command = self.getButton, pady = 4)
		self.button1.grid(row = 3, column = 3, columnspan = 10, sticky = "w")

		self.button2 = Radiobutton(master, text = "Linear Actuator - middle", variable = self.button_choice, value = 2, command = self.getButton, pady = 4)
		self.button2.grid(row = 4, column = 3, columnspan = 15, sticky = "w")

		self.button3 = Radiobutton(master, text = "Linear Actuator - bottom", variable = self.button_choice, value = 3, command = self.getButton, pady = 4)
		self.button3.grid(row = 5, column = 3, columnspan = 15, sticky = "w")

		self.button4 = Radiobutton(master, text = "Stepper Motor (clockwise)", variable = self.button_choice, value = 4, command = self.getButton, pady = 4)
		self.button4.grid(row = 6, column = 3, columnspan = 16, sticky = "w")

		self.button5 = Radiobutton(master, text = "Stepper Motor (counterclockwise)", variable = self.button_choice, value = 5, command = self.getButton, pady = 4)
		self.button5.grid(row = 7, column = 3, columnspan = 18, sticky = "w")

		# -------- Entry Field with Labels
		self.value_Label = Label(master, text = "Enter Value:", font = "Helvetica 15 bold underline")
		self.value_Label.grid(row = 8, column = 2, columnspan = 7, sticky = "w", pady = 10)

		self.entry_Field = Entry(master, width = 8)
		self.entry_Field.selection_range(0, END)
		self.entry_Field.selection_clear()
		self.entry_Field.grid(row = 8, column = 9, columnspan = 6, sticky = "w", pady = 10, padx = 2)

		self.unit_Label = Label(master, text = "", fg = "blue")
		self.unit_Label.grid(row = 8, column = 15, columnspan = 7, sticky = "w", pady = 10)

		# -------- Message Box
		self.message_Box_Title_Label = Label(master, text = "", fg = "blue", font = "Helvetica 16 underline bold", pady = 8)
		self.message_Box_Title_Label.grid(row = 11, column = 2, rowspan = 2, columnspan = 20, sticky = "sw")

		self.message_Box = Message(master, text = "\n\n\n\n\n", width = 475)
		self.message_Box.grid(row = 13, column = 2, rowspan = 10, columnspan = 46, sticky = "nw" )

		# -------- Move Motor Button
		self.move_Button = Button(master, text = "Move motor!", command = self.moveMotorButton, fg = 'blue', state = "disabled")
		self.move_Button['font'] = tkFont.Font(family = 'Helvetica', size = 14, weight = 'bold')
		self.move_Button.grid(row = 8, column = 20, columnspan = 3) # place 'Move motor!' button

		# -------- Status Bar
		self.status_Label = Label(master, text = "", fg = "green3", font = "Helvetica 14 underline")
		self.status_Label.grid(row = 23, column = 2, columnspan = 6, sticky = "w")

		self.status_Message_Box = Message(master, text = "", width = 475, fg = "green3", font = "Helvetica 14 italic")
		self.status_Message_Box.grid(row = 23, column = 6, columnspan = 46, rowspan = 2, sticky = "w")

		# -------- Auto Check Entry Field for a valid entry
		self.autoCheckEntryField()



	# -------- Methods
	def autoCheckEntryField(self):
		value = self.checkValue(self.entry_Field.get()) # turn entry field into int and catch error

		if self.button_choice.get() == 0: # when no motor radiobutton is selected
			self.move_Button['state'] = "disabled"
		elif value == None:
			self.move_Button['state'] = "disabled"
			self.clearStatusMessage()
		elif value < 0:
			self.move_Button['state'] = "disabled"
			self.updateStatusMessage("Value must be a positive integer.", statusType = "Error:", color = "red")
		

		# Check if value is in range for the selected motor
		elif self.button_choice.get() == 1:
			if value < 37 or value > 154:
				self.move_Button['state'] = "disabled"
				self.updateStatusMessage("Value not in range.", statusType = "Error:", color = "red")
			else:
				self.clearStatusMessage()
				self.move_Button['state'] = "normal"
		
		elif self.button_choice.get() == 2:
			if value > 180:
				self.move_Button['state'] = "disabled"
				self.updateStatusMessage("Value not in range.", statusType = "Error:", color = "red")
			else:
				self.clearStatusMessage()
				self.move_Button['state'] = "normal"

		elif self.button_choice.get() == 3:
			if value > 180:
				self.move_Button['state'] = "disabled"
				self.updateStatusMessage("Value not in range.", statusType = "Error:", color = "red")
			else:
				self.clearStatusMessage()
				self.move_Button['state'] = "normal"

		elif self.button_choice.get() == 4:
			if value == 0:
				self.move_Button['state'] = "disabled"
				self.updateStatusMessage("Value must be at least 1.", statusType = "Error:", color = "red")
			else:
				self.clearStatusMessage()
				self.move_Button['state'] = "normal"

		elif self.button_choice.get() == 5:
			if value == 0:
				self.move_Button['state'] = "disabled"
				self.updateStatusMessage("Value must be at least 1.", statusType = "Error:", color = "red")
			else:
				self.clearStatusMessage()
				self.move_Button['state'] = "normal"

		else:
			self.move_Button['state'] = "normal"
			self.clearStatusMessage()

		self.master.after(100, self.autoCheckEntryField) # refresh every 100ms

	def checkValue(self, entry):
		if len(entry) == 0:
			return None
		try:
			value = int(entry)
		except:
			# print "Error: Value must be an integer."
			return -1
		return value


	def getButton(self):
		if self.button_choice.get() == 1:
			self.unit_Label.config(text = "degrees")
			self.message_Box_Title_Label.config(text = "Servo Gearbox:")
			self.message_Box.config(text = " - Move the gearbox from its current position to the goal position entered\n    in the 'Value' field.\n\n - Range = [37, 154] degrees.\n\n")

		elif self.button_choice.get() == 2:
			self.unit_Label.config(text = "degrees")
			self.message_Box_Title_Label.config(text = "Linear Actuator - middle:")
			self.message_Box.config(text = " - Move the actuator from its current position to the goal position entered\n    in the 'Value' field.\n\n - Range = [0, 180] degrees.\n\n")

		elif self.button_choice.get() == 3:
			self.unit_Label.config(text = "degrees")
			self.message_Box_Title_Label.config(text = "Linear Actuator - bottom:")
			self.message_Box.config(text = " - Move the actuator from its current position to the goal position entered\n    in the 'Value' field.\n\n - Range = [0, 180] degrees.\n\n")

		elif self.button_choice.get() == 4:
			self.unit_Label.config(text = "steps  ")
			self.message_Box_Title_Label.config(text = "Stepper Motor:")
			self.message_Box.config(text = " - Move the stepper motor clockwise the number of steps entered in the\n    'Value' field.\n\n - Steps to revolve clockwise around the table = #### steps.\n\n")

		elif self.button_choice.get() == 5:
			self.unit_Label.config(text = "steps  ")
			self.message_Box_Title_Label.config(text = "Stepper Motor:")
			self.message_Box.config(text = " - Move the stepper motor counterclockwise the number of steps entered\n    in the 'Value' field.\n\n - Steps to revolve counterclockwise around the table = #### steps.\n\n")

	def moveMotorButton(self):
		value = self.checkValue(self.entry_Field.get())

		if value < 0:
			self.updateStatusMessage("Value must be a non-negative integer.", "Error:", "red")
			return

		self.updateStatusMessage("Motor Moving. Please wait...")

		# ************/************\************
		# **********/****************\**********
		# ********/********i************\********

		# Call methods to move motors here.
		time.sleep(4) 
		# This simluates a motor moving.
		# ********\********************/********
		# **********\****************/**********
		# ************\************/************

		self.clearStatusMessage()
		self.entry_Field.selection_range(0, END) # highlight the text
		print "Move motor completed."

	def updateStatusMessage(self, statusMessage, statusType = "Status:", color = "green3"):
		self.status_Label.config(text = statusType, fg = color)
		self.status_Message_Box.config(text = statusMessage, fg = color)
		self.master.update_idletasks()

	def clearStatusMessage(self):
		self.status_Label.config(text = "")
		self.status_Message_Box.config(text = "")
		self.master.update_idletasks()

	



