from tkinter import *

def hello():
  """Callback function for button press."""
  print("Hello World")

# Main root window
root = Tk()

# A button with a callback function
Button(root, text="Press here", command=hello).pack()
# .pack() method is necessary to make the button appear

# Event loop
root.mainloop()