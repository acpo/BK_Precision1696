try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    import tkinter.filedialog   #seems to be necessary to be explicit about this dialog

class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        tk.Label(text="Step", font='bold', fg='blue').grid(row=0,column=0)
        tk.Label(text = "0", font='bold', fg='blue').grid(row=1,column=0)
        tk.Label(text = "1", font='bold', fg='blue').grid(row=2,column=0)
        tk.Label(text = "2", font='bold', fg='blue').grid(row=3,column=0)
        tk.Label(text = "3", font='bold', fg='blue').grid(row=4,column=0)
        tk.Label(text = "4", font='bold', fg='blue').grid(row=5,column=0)
        tk.Label(text = "5", font='bold', fg='blue').grid(row=6,column=0)

# The Tab order is the order of creation of the entry boxes.  So we can
#  shuffle this order to force a specific order

        tk.Label(text = "Voltage", font='bold', fg='blue').grid(row=0,column=1)
        self.volt0 = tk.Entry(width='5')
        self.volt0.insert(0, 0.0)
        self.volt0.bind('<Return>', self.setVolt) and self.volt0.bind('<Tab>', self.setVolt)
        self.volt0.grid(column=1, row=1)
        self.volt1 = tk.Entry(width='5')
        self.volt1.insert(0, 0.0)
        self.volt1.bind('<Return>', self.setVolt) and self.volt1.bind('<Tab>', self.setVolt)
        self.volt1.grid(column=1, row=2)
        self.volt2 = tk.Entry(width='5')
        self.volt2.insert(0, 0.0)
        self.volt2.bind('<Return>', self.setVolt) and self.volt2.bind('<Tab>', self.setVolt)
        self.volt2.grid(column=1, row=3)
        self.volt3 = tk.Entry(width='5')
        self.volt3.insert(0, 0.0)
        self.volt3.bind('<Return>', self.setVolt) and self.volt3.bind('<Tab>', self.setVolt)
        self.volt3.grid(column=1, row=4)
        self.volt4 = tk.Entry(width='5')
        self.volt4.insert(0, 0.0)
        self.volt4.bind('<Return>', self.setVolt) and self.volt4.bind('<Tab>', self.setVolt)
        self.volt4.grid(column=1, row=5)
        self.volt5 = tk.Entry(width='5')
        self.volt5.insert(0, 0.0)
        self.volt5.bind('<Return>', self.setVolt) and self.volt5.bind('<Tab>', self.setVolt)
        self.volt5.grid(column=1, row=6)

        tk.Label(text = "Current", font='bold', fg='blue').grid(row=0,column=2)
        self.current0 = tk.Entry(width='5')
        #self.current0.bind('<Return>', self.setCur)
        self.current0.grid(column=2, row=1)
        self.current1 = tk.Entry(width='5')
        #self.current1.bind('<Return>', self.setCur)
        self.current1.grid(column=2, row=2)
        self.current2 = tk.Entry(width='5')
        #self.current1.bind('<Return>', self.setCur)
        self.current2.grid(column=2, row=3)
        self.current3 = tk.Entry(width='5')
        #self.current1.bind('<Return>', self.setCur)
        self.current3.grid(column=2, row=4)
        self.current4 = tk.Entry(width='5')
        #self.current1.bind('<Return>', self.setCur)
        self.current4.grid(column=2, row=5)
        self.current5 = tk.Entry(width='5')
        #self.current1.bind('<Return>', self.setCur)
        self.current5.grid(column=2, row=6)

        tk.Label(text = "Seconds", font='bold', fg='blue').grid(row=0,column=3)
        self.second0 = tk.Entry(width='5')
        #self.second0.bind('<Return>', self.setTime)
        self.second0.grid(column=3, row=1)
        self.second1 = tk.Entry(width='5')
        #self.second1.bind('<Return>', self.setTime)
        self.second1.grid(column=3, row=2)
        self.second2 = tk.Entry(width='5')
        #self.second1.bind('<Return>', self.setTime)
        self.second2.grid(column=3, row=3)
        self.second3 = tk.Entry(width='5')
        #self.second1.bind('<Return>', self.setTime)
        self.second3.grid(column=3, row=4)
        self.second4 = tk.Entry(width='5')
        #self.second1.bind('<Return>', self.setTime)
        self.second4.grid(column=3, row=5)
        self.second5 = tk.Entry(width='5')
        #self.second1.bind('<Return>', self.setTime)
        self.second5.grid(column=3, row=6)

        tk.Label(text = "Program to write", font='bold').grid(row=7, column=0, columnspan=2)
        self.Program = tk.Entry(width='5')
        #self.Program.bind('<Return>', self.memorySlot)
        self.Program.grid(column=2, row=7)

        self.button_Send = tk.Button(text = "Send program to PS", font='bold')
        self.button_Send.grid(column=0, row=8, columnspan=2)
        #self.button_Send.bind('<ButtonRelease-1>', self.sendProgram)
        
        ConnectState = tk.IntVar()
        PSconnect = tk.Checkbutton(text='Connect/Disconnect',variable=ConnectState, onvalue=1, offvalue=0)
        PSconnect.grid(column=0, row=9, columnspan=2)
        #self.load_data_button.grid(row=7,column=0, columnspan=2)
        #self.load_data_button.bind('<ButtonRelease-1>', self.Load_SpecData)
        #self.calc_abs_button = tk.Button(text = 'Select Incident Emission')
        #self.calc_abs_button.grid(row=2,column=0)
        #self.calc_abs_button.bind('<ButtonRelease-1>', self.Incident_Abs)

    def setVolt(self, event):        
        voltages = [self.volt0, self.volt1, self.volt2]
        for x in voltages:
            x = x.get()
            print(x)

def Connect_PS():
    print(ConnectState)
    pass




def main():
    root = tk.Tk()
    app = MainWindow(root)
    app.grid()
    root.mainloop()

if __name__ == '__main__':
    main()
