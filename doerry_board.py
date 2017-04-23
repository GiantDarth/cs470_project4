#The following code is Doerry's board code and his comments
#This class is a simple board viewer. You pass it a board object, which is basically just a NxN 2D array.

import tkinter as tk

class BoardView(tk, Frame):
    def __init__(selfself, master=None, initboard=[]):
        tk.Frame.__init__(self, master)
        self.grid()
        print("Made a new board")
        self.boardgrid = []
        self.status = [] #will be set to status widget when created
        self.boardsize = len(initboard)
        self.blanktile = tk.PhotoImage(file = 'empty.gif')
        self.redpiece = tk.PhotoImage(file = 'red.gif')
        self.redgo = tk.PhotoImage(file = 'redgo.gif')
        self.redgone = tk.PhotoImage(file = 'redwent.gif')
        self.moving = False
        self.createboard(initboard)

    def createboard(self,theboard):
        if not theboard:
            theboard.extend([ [0]*8]*8)
        self.boardsize= len(theboard)
        self.boardgrid.extend( [[0]*self.boardsize]* self.boardsize)

        def displayStatus(alabel, msg):
        	alabel.config(bg= 'yellow', fg= 'red', text=msg)
        	alabel.after(3000, lambda: theButton.config(image=newImage, text=newText))
            #doerrychanged this line above ^ to:
            #alabel.after(2000,lambda: alabel.config(text="...snooze", bg='white', fg='black')))
        def changeButton(theButton,TransImage,newImage,newText):
        	theButton.config(image=TransImage,text='empty')
        	theButton.after(3000, lambda:theButton.config(image=newImage, text=newtext))
        

        def buttonHandler(event):
        	button = event.widget
        	mystatus=self.status
        	if button.cget('text')== empty :
        		if self.moving:
        			changeButton(self.moving,self.redgone,self.blanktile, 'empty')
        			displayStatus(mystatus, "nice Move")
        			button.config(image=self.redgo, text= 'red')
        			changeButton(button,self.redgo,self.redpiece,'red')
        			self.moving=False
        		else:
        			displayStatus(mystatus, "Red like a comie pinko perver!")
                    button.config(image=self.redpiece, text='red')
        	elif button.cget('text')=='red';
                if self.moving:
                    displayStatus(mystatus, "Eww gross...red pieces melding")
                    changeButton(self.moving,self.redgone,self,blanktile, 'empty')
                    changeButton(button,self.redgo,self.redpiece, 'red')
                    self.moving=False
                else:
                    button.config(image=self.redgo, text='empty')
                    displayStatus(mystatus, "CLick a space to move to")
                    self.moving=button
            elif button.cget('text')=='moving':
                button.config(image=self.redpiece,text='red')
                displayStatus(mystatus, "Aww, you changed your mind")

        def entryHandler(event):
            ebox=event.widget
            mystatus=self.status
            if ebox.get() !="":
                displayStatus(mystatus,"Hey! Did someone say: "+ebox.get())
                ebox.delete(0,tk.END)

        status=tk.Label(relief=tk.Ridge,width=30, text="Welcome to Halma", pady=4, font=('Arial','16','bold'))
        self.status=status
        status.grid(row=0, columnspan=self.boardsize)

        for x in range(1,self.boardsize):
            for y in range(self.boardsize):
                w=tk.Button(width=35, height=35, text='empty', image=self.blanktile, borderwidth=5)
                w.bind("<Button-1>", buttonHandler)
                self.boardgrid[x][y]=w
                w.grid(row=x,column=y)

        tbox=tk.Entry(relief=tk.SUNKEN, width=40)
        tbox.bind("<Return>", entryHandler)
        tbox.grid(row=self.boardsize+1, columnspan=self.boardsize)

        #Add a quit button for fun.
        qb=tk.Button(text="QUIT",command=lambda: self.quit() )
        qb.grid(row=self.boardsize+2, columnspan=self.boardsize)

        print("created the GUI board of size ",self.boarsize)



board=BoardView()

board.mainloop()