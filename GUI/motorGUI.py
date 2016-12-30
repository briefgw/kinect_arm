# Karl Preisner
# December 27, 2016
# GUI class for moving all four motors

# motorDemo.py builds and runs this GUI.

# Note: all commands to socket must have \n character at the end.

from Tkinter import *
import tkFont
from PIL import Image, ImageTk # sudo pip install Pillow (might need to also install pip)
import time
import socket
import sys


# Class motorGUI builds the GUI and has methods for button actions.
class motorGUI:

	def doNothing(self):
		return

	def __init__(self, master, default_IP, default_PORT): # constructor
		
		self.master = master # this is important.

		# Add all components/widgets to window
		self.addGUIcomponents(self.master)

		# Set default ip address and port
		self.ip_Entry.insert(END, default_IP)
		self.port_Entry.insert(END, default_PORT)

		# Create client Socket
		self.clientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)

		
		# Set initial mode 
		self.setMode("Connect to RPi")
		# self.setMode("Motor interaction")

		

		# Begin Idle Loop
		# self.idleLoop() # updates every 100ms when program is idle.

	def setMode(self, mode):
		print "set mode = ",mode
		self.mode = mode
		# Modes:
		# - Connect to RPi
		# - Motor interaction
		if mode == "Connect to RPi":
			# Enable components associated with Connecting to RPi
			for c in self.connectionComponentList:
				self.enable(c)
			# Disable components associated with motor interaction
			
			# self.value_Entry.selection_range(0, END)
			# self.value_Entry.selection_clear()
			self.value_Entry.delete(0, END)

			for c in self.motorComponentList:
				self.disable(c)
			self.infoBox_Label.config(text = "")
			self.infoBox_Message.config(text = "\n\n\n\n\n")
			self.status_Label.config(text = "")
			self.status_Message.config(text = "")
			self.unit_Label.config(text = "")
			
			self.selectedMotor.set(0)
			self.master.update_idletasks()

		elif mode == "Motor interaction":
			# Enable components associated with motor interaction
			for c in self.motorComponentList:
				self.enable(c)
			self.selectedMotor.set(1) # default motor selection to Servo Gearbox
			self.selectMotorButton()
			# Disable components associated with Connecting to RPi
			for c in self.connectionComponentList:
				self.disable(c)
			self.master.update_idletasks()
		
		# Begin idleLoop
		self.idleLoop()

	def connectRPi(self):
		ip_address = self.ip_Entry.get()
		port = int(self.port_Entry.get())

		self.disable(self.connect_Button)
		self.disable(self.ip_Entry)
		self.disable(self.port_Entry)

		# Create new client Socket
		# self.clientSocket = None
		self.clientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)

		self.connectionStatus_Label.config(fg = "black", text = "Establishing connection...")
		self.master.update_idletasks()

		print "connecting to",ip_address, port
		self.clientSocket.connect((ip_address, port)) # uncomment when ready
		print "connected"
		self.connectionStatus_Label.config(fg = "green3", text = "Connected")
		self.setMode("Motor interaction")

		# # Try to connect to socket with IP_ADDRESS and PORT
		# try:
		# 	# self.clientSocket.settimeout(10)
		# 	print "connecting to"
		# 	self.clientSocket.connect((ip_address, port)) # uncomment when ready
		# 	# self.clientSocket.settimeout(None)
		# 	print "Connected"
		# 	self.connectionStatus_Label.config(fg = "green3", text = "Connected")
		# 	self.setMode("Motor interaction")
		# except:
		# 	print "Unable to connect"
		# 	self.connectionStatus_Label.config(fg = "red", text = "Unable to connect")
		# 	self.setMode("Connect to RPi")

	def disconnectRPi(self):
		print "Disconnected"
		self.clientSocket.shutdown(socket.SHUT_RDWR)
		print "shutdown done"
		self.clientSocket.close()
		print "close done"
		self.clientSocket = None
		self.connectionStatus_Label.config(fg = "red", text = "Disconnected")
		self.master.update_idletasks()
		# self.master.after(1000)
		self.setMode("Connect to RPi")
		

	def isConnected(self):
		# print "isConnected()"
		# send ping, get response
		try:
			self.clientSocket.send("Are you alive?\n")
			response = self.clientSocket.recv(1000) #receive up to 1000 characters (bytes)
			# print "isConnected() try successful"
			return True
		except:
			return False

	def idleLoop(self):
		# This method runs when there are no other tasks running.

		if self.mode == "Connect to RPi":
			# Refresh every 100ms
			self.doNothing()

		elif self.mode == "Motor interaction":
			# This loop does several things:
			# - Check if connection is still established
			# - Checks value_Entry for a valid entry
			# - Enables/disables the moveMotor_Button if entry is selected motor's range
			# - Sets the status message box on above conditions

			# Check if connection is broken
			if self.isConnected() != True:
				print "Connection failed"
				self.connectionStatus_Label.config(fg = "red", text = "Connection Failed")
				self.setMode("Connect to RPi")

			# Get selected motor button and convert entry field value to int
			button = self.selectedMotor.get()
			value = self.convertEntryFieldToInt(self.value_Entry.get()) # turn entry field into int and catch error
			[b, msg] = self.valueInRange(button, value) # b = T/F, msg = Error message

			# in case these are disabled, enable them
			self.enable(self.value_Entry)
			self.enable(self.disconnect_Button)
			for m in self.motorButtonList: # enable the motor selection buttons
				self.enable(m)

			# Check value for non-negative integer
			if value == None: # when entryField is empty
				self.disable(self.moveMotor_Button)
				if self.moveCompleteMsg == False:
					self.clearStatusMsg()
			elif value < 0: # when negative number or non-digit character
				self.disable(self.moveMotor_Button)
				self.moveCompleteMsg = False
				self.setStatusMsg("Value must be a non-negative integer.", statusType = "Error:", color = "red")
			
			# For each motor, check if value is in range
			elif b == "T":
				if self.moveCompleteMsg == False:
					self.clearStatusMsg()
				self.enable(self.moveMotor_Button)
			elif b == "F":
				self.disable(self.moveMotor_Button)
				self.setStatusMsg(msg, statusType = "Error:", color = "red")
				self.moveCompleteMsg = False

		# Refresh every 100ms
		self.master.after(100, self.idleLoop) 

	def valueInRange(self, button, value):
		# value is a non-negative integer
		if button == 1: # Servo Gearbox
			if value < 37 or value > 154:
				return ["F", "Value not in range."]
		elif button in [2, 3]: # Linear Actuators
			if value < 0 or value > 180: 
				return ["F", "Value not in range."]
		elif button in [4, 5]: # Stepper motor
			if value < 1:
				return ["F", "Value must be at least 1."]
		return ["T", ""] # Value in range

	def convertEntryFieldToInt(self, entry):
		if len(entry) == 0:
			return None
		try:
			value = int(entry)
		except:
			return -1 # prints "Error: Value must be an integer."
		return value

	def selectMotorButton(self):
		self.value_Entry.focus_set() # focus on entryField
		motor = self.selectedMotor.get()

		# set unit_Label
		if motor in [1, 2, 3]:
			self.unit_Label.config(text = "degrees")
		else:
			self.unit_Label.config(text = "steps")

		# set Message Box Title and Message
		if motor == 1:
			self.infoBox_Label.config(text = "Servo Gearbox:")
			self.infoBox_Message.config(text = "- Move the gearbox from its current position to the goal position entered in the 'Value' field.\n\n- Range = [37, 154] degrees.\n\n")
		elif motor == 2:
			self.infoBox_Label.config(text = "Linear Actuator - middle:")
			self.infoBox_Message.config(text = "- Move the actuator from its current position to the goal position entered in the 'Value' field.\n\n- Range = [0, 180] degrees.\n\n")
		elif motor == 3:
			self.infoBox_Label.config(text = "Linear Actuator - Bottom:")
			self.infoBox_Message.config(text = "- Move the actuator from its current position to the goal position entered in the 'Value' field.\n\n- Range = [0, 180] degrees.\n\n")
		elif motor == 4:
			self.infoBox_Label.config(text = "Stepper Motor (clockwise):")
			self.infoBox_Message.config(text = "- Move the stepper motor clockwise the number of steps entered in the 'Value' field.\n\n- Steps to revolve around the table = #### steps.\n\n")
		elif motor == 5:
			self.infoBox_Label.config(text = "Stepper Motor (counterclockwise):")
			self.infoBox_Message.config(text = "- Move the stepper motor counterclockwise the number of steps entered in the 'Value' field.\n\n- Steps to revolve around the table = #### steps.\n\n")

	def moveMotor(self):
		print "Move motor begin"

		# disable moveMotor_Button, value_Entry, motorButtonList
		self.disable(self.moveMotor_Button)
		self.disable(self.value_Entry)
		self.disable(self.disconnect_Button)
		for m in self.motorButtonList: # disable the motor selection buttons
			self.disable(m)

		# ************///******~~~~~~~~~~******\\\************
		# **********///********~~~~~~~~~~********\\\**********
		# ********///**********~~~~~~~~~~**********\\\********
		t = time.time()
		
		# create command to send to RPi
		value = str(self.value_Entry.get()) # NOTE: typing -0 works. might need to fix that
		text = self.infoBox_Label['text']
		command = text + value + "\n"


		# send command to RPi
		self.setStatusMsg("Sending command to RPi...")
		print "sending command:", command
		self.clientSocket.send(command)
		
		# get response from RPi
		self.setStatusMsg("Wait for RPi response. (If no response, quit with error message).")
		response = self.clientSocket.recv(1000)
		print "RPi response:", response

		# wait for RPi response that motor movement is complete
		self.setStatusMsg("Motor moving... Waiting for RPi signal that movement is completed.")
		# respone = self.clientSocket.recv(1000)
		self.master.after(3000)

		# This simluates a motor moving.
		self.setStatusMsg("RPi signal received.")

		elapsed_time = str(int(time.time() - t))
		self.setStatusMsg("Motor movement complete. Time elapsed: " + elapsed_time + " seconds.")
		# ********\\\**********~~~~~~~~~~**********///********
		# **********\\\********~~~~~~~~~~********///**********
		# ************\\\******~~~~~~~~~~******///************
		
		self.moveCompleteMsg = True # Used in idleLoop()
		self.value_Entry.selection_range(0, END) # highlight the text

		# Do NOT enable anything here. They must be enabled after method return. Trust me.
		print "Move motor completed"

	def setStatusMsg(self, statusMessage, statusType = "Status:", color = "green3"):
		# Do NOT call self.clearStatusMsg() here.
		self.status_Label.config(text = statusType, fg = color)
		self.status_Message.config(text = statusMessage, fg = color)
		self.master.update_idletasks() # Do NOT use update()

	def clearStatusMsg(self):
		self.status_Label.config(text = "")
		self.status_Message.config(text = "")
		self.master.update_idletasks() # Do NOT use update()

	def disable(self, widget):
		if widget['state'] != "disabled":
			widget['state'] = "disabled"

	def enable(self, widget):
		if widget['state'] == "disabled":
			widget['state'] = "normal"

	def addGUIcomponents(self, master):
		# Set Window Title
		master.title("Camera Arm Motors")
		
		# Set Window Dimensions
		master.minsize(width = 650, height = 650)
		master.maxsize(width = 650, height = 650)

		# -------- Image: 256x256
		self.armImage = ImageTk.PhotoImage(Image.open("arm_256x256.jpg"))
		self.armImage_Label = Label(master, image = self.armImage)
		self.armImage_Label.grid(row = 2, column = 20, columnspan = 30, rowspan = 14, sticky = "", padx = 30, pady = 0)

		# -------- Title Label
		self.title_Label = Label(master, text = "Camera Arm Motors", fg = "blue", relief = "solid", bg = '#e6e6ff', borderwidth = 5, font = "Helvetica 19 bold")
		self.title_Label.grid(row = 0, column = 0, rowspan = 2, columnspan = 50, pady = 20, padx = 190, ipadx = 40, ipady = 10)

		# -------- IP and port connection 
		self.connectRPi_Label = Label(master, text = "Connect to Raspberry Pi:", font = "Helvetica 15 bold underline", pady = 8)
		self.connectRPi_Label.grid(row = 2, column = 2, columnspan = 17, sticky = "sw")

		self.ip_Label = Label(master, text = "IP:")
		self.ip_Label.grid(row = 3, column = 3, columnspan = 1, sticky = "e")

		self.port_Label = Label(master, text = "Port:")
		self.port_Label.grid(row = 4, column = 3, columnspan = 1, sticky = "e")

		self.ip_Entry = Entry(master, width = 12)
		self.ip_Entry.grid(row = 3, column = 4, columnspan = 10, sticky = "w")

		self.port_Entry = Entry(master, width = 12) # casted to int() in connectRPi() method 
		self.port_Entry.grid(row = 4, column = 4, columnspan = 10, sticky = "w")

		# -------- Connection Status Label
		self.connectionStatus_Label = Label(master, text = "Not connected", fg = "red", font = "Helvetica 13",)
		self.connectionStatus_Label.grid(row = 3, column = 14, columnspan = 18, sticky = "w")

		# -------- Connect Button
		self.connect_Button = Button(master, text = "Connect!", command = self.connectRPi)
		self.connect_Button['font'] = tkFont.Font(family = 'Helvetica', size = 14, weight = 'bold')
		self.connect_Button.grid(row = 4, column = 14, columnspan = 9, sticky = "w") # place 'Move motor!' button

		# -------- Disconnect Button
		self.disconnect_Button = Button(master, text = "Disconnect", command = self.disconnectRPi)
		self.disconnect_Button['font'] = tkFont.Font(family = 'Helvetica', size = 14, weight = 'bold')
		self.disconnect_Button.grid(row = 4, column = 23, columnspan = 9, sticky = "w") # place 'Move motor!' button

		# -------- Select Motor Label
		self.selectMotor_Label = Label(master, text = "Select a motor:", font = "Helvetica 15 bold underline", pady = 8)
		self.selectMotor_Label.grid(row = 5, column = 2, columnspan = 12, sticky = "sw")

		# -------- Radio Buttons for motor selection
		self.selectedMotor = IntVar()

		self.mb1 = Radiobutton(master, variable = self.selectedMotor, value = 1, command = self.selectMotorButton, pady = 4)
		self.mb2 = Radiobutton(master, variable = self.selectedMotor, value = 2, command = self.selectMotorButton, pady = 4)
		self.mb3 = Radiobutton(master, variable = self.selectedMotor, value = 3, command = self.selectMotorButton, pady = 4)
		self.mb4 = Radiobutton(master, variable = self.selectedMotor, value = 4, command = self.selectMotorButton, pady = 4)
		self.mb5 = Radiobutton(master, variable = self.selectedMotor, value = 5, command = self.selectMotorButton, pady = 4)
		self.mb1.config(text = "Servo Gearbox")
		self.mb2.config(text = "Linear Actuator - middle")
		self.mb3.config(text = "Linear Actuator - bottom")
		self.mb4.config(text = "Stepper Motor (clockwise)")
		self.mb5.config(text = "Stepper Motor (counterclockwise)")
		self.mb1.grid(row = 6, column = 3, columnspan = 10, sticky = "w")
		self.mb2.grid(row = 7, column = 3, columnspan = 15, sticky = "w")
		self.mb3.grid(row = 8, column = 3, columnspan = 15, sticky = "w")
		self.mb4.grid(row = 9, column = 3, columnspan = 16, sticky = "w")
		self.mb5.grid(row = 10, column = 3, columnspan = 18, sticky = "w")
		# make a list of the motor buttons
		self.motorButtonList = [self.mb1, self.mb2, self.mb3, self.mb4, self.mb5]

		# -------- Entry Field with Labels
		self.value_Label = Label(master, text = "Enter Value:", font = "Helvetica 15 bold underline")
		self.value_Label.grid(row = 11, column = 2, columnspan = 4, sticky = "w")

		self.value_Entry = Entry(master, width = 10)
		self.value_Entry.selection_range(0, END)
		self.value_Entry.selection_clear()
		self.value_Entry.grid(row = 11, column = 6, columnspan = 6, sticky = "w", pady = 10, padx = 2)

		self.unit_Label = Label(master, text = "", fg = "blue")
		self.unit_Label.grid(row = 11, column = 12, columnspan = 6, sticky = "w", pady = 10)

		# -------- Move Motor Button
		self.moveMotor_Button = Button(master, text = "Move motor!", command = self.moveMotor)
		self.moveMotor_Button['font'] = tkFont.Font(family = 'Helvetica', size = 14, weight = 'bold')
		self.moveMotor_Button.grid(row = 11, column = 18, columnspan = 9, sticky = "w") # place 'Move motor!' button

		# -------- Message Box
		self.infoBox_Label = Label(master, text = "", fg = "blue", font = "Helvetica 16 underline bold", pady = 8)
		self.infoBox_Label.grid(row = 13, column = 2, rowspan = 2, columnspan = 20, sticky = "sw")

		self.infoBox_Message = Message(master, text = "\n\n\n\n\n", width = 600)
		self.infoBox_Message.grid(row = 16, column = 2, rowspan = 10, columnspan = 46, sticky = "nw" )
		
		# -------- Status Bar
		self.status_Label = Label(master, text = "", fg = "green3", font = "Helvetica 13 underline")
		self.status_Label.grid(row = 26, column = 2, columnspan = 2, sticky = "nw")

		self.status_Message = Message(master, text = "", width = 600, fg = "green3", font = "Helvetica 13")
		self.status_Message.grid(row = 26, column = 4, columnspan = 46, rowspan = 3, sticky = "nw")

		self.moveCompleteMsg = False # for displaying motor movement completion message

		# Lists of components used to iteratively enable/disable
		# Note: disable not available for Tkinter Message() widget
		self.connectionComponentList = [self.connectRPi_Label, self.ip_Label, self.ip_Entry, self.port_Label, self.port_Entry, self.connect_Button]
		self.motorComponentList = [self.disconnect_Button, self.selectMotor_Label, self.mb1, self.mb2, self.mb3, self.mb4, self.mb5, self.value_Label, self.value_Entry, self.unit_Label, self.moveMotor_Button, self.infoBox_Label, self.status_Label]




