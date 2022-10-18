try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    import tkinter.filedialog   #seems to be necessary to be explicit about this dialog
from tkinter import messagebox

import serial
import a1696lib
try:
    ser = serial.Serial(port='COM3',
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout = 1,
                        writeTimeout = 0
                    ) #ensure non-blocking
except serial.SerialException:
    messagebox.showerror("Error", "Error opening serial port. \nIs another connection open?")
    exit()
except:
    messagebox.showerror("Error", "Other problem with serial port communication")
    exit()
    
ConnectState = False  #set initial state of serial port connect to not connected

class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        steps = [0, 1, 2, 3, 4, 5]
        tk.Label(text="Step", font='bold', fg='blue').grid(row=0,column=0)
        for x in steps:
            tk.Label(text = str(x), font='bold', fg='blue').grid(row=x+1,column=0)

        self.volt = []    
        tk.Label(text = "Voltage", font='bold', fg='blue').grid(row=0,column=1)
        for x in steps:
            entryV = tk.Entry(width='5')
            entryV.insert(0, 1.0)
            entryV.bind('<Return>', self.setVolt) and entryV.bind('<Tab>', self.setVolt)
            entryV.grid(column=1, row=x+1)
            self.volt.append(entryV)

        self.current = []
        tk.Label(text = "Current", font='bold', fg='blue').grid(row=0,column=2)
        for x in steps:
            entryC = tk.Entry(width='5')
            entryC.insert(0, 1.0)
            entryC.bind('<Return>', self.setCur) and entryC.bind('<Tab>', self.setCur)
            entryC.grid(column=2, row=x+1)
            self.current.append(entryC)

        self.minute = []
        tk.Label(text = "Minutes", font='bold', fg='blue').grid(row=0,column=3) #values 0 to 59
        for x in steps:
            entryM = tk.Entry(width='5')
            entryM.insert(0, 1.0)
            entryM.bind('<Return>', self.setTime) and entryM.bind('<Tab>', self.setTime)
            entryM.grid(column=3, row=x+1)
            self.minute.append(entryM)

        self.second = []
        tk.Label(text = "Seconds", font='bold', fg='blue').grid(row=0,column=4) #values 0 to 59
        for x in steps:
            entryS = tk.Entry(width='5')
            entryS.insert(0, 1.0)
            entryS.bind('<Return>', self.setTime) and entryS.bind('<Tab>', self.setTime)
            entryS.grid(column=4, row=x+1)
            self.second.append(entryS)
        
        tk.Label(text = "Program to write", font='bold').grid(row=7, column=0, columnspan=2)
        self.Program = tk.Entry(width='5')
        self.Program.bind('<Return>', self.memorySlot) and self.Program.bind('<Tab>', self.memorySlot)
        self.Program.grid(column=2, row=7)

        self.button_Send = tk.Button(text = "Send program to PS", font='bold')
        self.button_Send.grid(column=0, row=8, columnspan=2)
        self.button_Send.bind('<ButtonRelease-1>', self.sendProgram)
        
        self.PSconnect = tk.Button(text='Connect/Disconnect', bg = "pink")
        self.PSconnect.grid(column=0, row=9, columnspan=2)
        self.PSconnect.bind('<ButtonRelease-1>', self.Connect_PS)

        tk.Label(text = "Max Volts =",).grid(column=3, row=8)
        self.maxVoltBox = tk.Label(text = "20.1", width=5).grid(column=4, row=8)
        tk.Label(text = "Max Amps =",).grid(column=3, row=9)
        self.maxVoltBox = tk.Label(text = "9.99", width=5).grid(column=4, row=9)

        self.button_test = tk.Button(text = "test Code")
        self.button_test.grid(column = 0, row = 10)
        self.button_test.bind('<ButtonRelease-1>', self.setupProgramMemory)

        self.button_stop = tk.Button(text = "STOP", bg="red")
        self.button_stop.grid(column = 2, row = 10)
        self.button_stop.bind('<ButtonRelease-1>', self.stopProgram)

    def setVolt(self, event):        
        for x in self.volt:
            volt = x.get()
            print(volt)
            try:
                float(volt) # can entry be coverted to float?
                if (float(volt) <= 20) and (float(volt) >= 1.0):
                    x.delete(0, 'end')
                    x.insert(0, float(volt))
                else:
                    x.delete(0, 'end')
                    x.insert(0, 1.0)
            except:
                x.delete(0, 'end')
                x.insert(0, 1.0)
    def setCur(self, event):        
        for x in self.current:
            cur = x.get()
            print(cur)
            try:
                float(cur) # can entry be coverted to float?
                if (float(cur) <= 9.99) and (float(cur) >= 0):
                    x.delete(0, 'end')
                    x.insert(0, float(cur))
                else:
                    x.delete(0, 'end')
                    x.insert(0, 0.0)
            except:
                x.delete(0, 'end')
                x.insert(0, 0.0)
    def setTime(self, event):        
        for x in self.second:
            # check each seconds to see if between 0 and 59
            sec = x.get()
            print(sec)
            try:
                float(sec) # can entry be coverted to float?
                if (float(sec) <= 59) and (float(sec) >= 0):
                    x.delete(0, 'end')
                    x.insert(0, float(sec))
                else:
                    x.delete(0, 'end')
                    x.insert(0, 0)
            except:
                x.delete(0, 'end')
                x.insert(0, 0)
            
        for y in self.minute:
            # check each minutes if between 0 and 99
            min = y.get()
            print(min)
            try:
                float(min) # can entry be coverted to float?
                if (float(min) < 59) and (float(min) >= 0):
                    y.delete(0, 'end')
                    y.insert(0, float(min))
                else:
                    y.delete(0, 'end')
                    y.insert(0, 0)
            except:
                y.delete(0, 'end')
                y.insert(0, 0)

    def memorySlot(self, event):
        memoryslot = self.Program.get()
        print(memoryslot)

    def Connect_PS(self, event):
        global ConnectState
        if ConnectState:  #checks for True
            ConnectState = False
            self.PSconnect.configure(background = 'pink')
            remoteMode(ConnectState)
        else:
            ConnectState = True
            self.PSconnect.configure(background = 'light green')
            remoteMode(ConnectState)
            try:
                maxvalues = getMaxVoltCurr(ser)
                print (maxvalues[1], " amps")
                print (maxvalues[0], " volts")
                self.maxVolt = maxvalues[0]
                self.maxAmp = maxvalues[1]
            except:
                print("exception")
                ConnectState = False
                self.PSconnect.configure(background = 'pink')


    def sendProgram(self, event):
        if ConnectState:  #if connected
            print("send string...")
            # construct strings
            
            #sdpWrite()
            # end construct strings
        else:
            pass

    def setupProgramMemory(self, event, address=0, serial = ser): #serial, location, voltage, current, minutes, seconds, address=0):
        """Setup a program memory location"""
        """location - 0-19"""
        """voltage, current - xx.xx"""
        """minutes, seconds - whole numbers"""
        # needs to be modified with a loop 0 to 4 (5 steps, loc 0-4) and pull the step-number volt, etc.
        steps = [0, 1, 2, 3, 4, 5]
        for x in steps:
            loc = int(x)
            vval = int(float(self.volt[x].get())) # need to store voltages in arrays
            vval = vval * 10
            cval = int(float(self.current[x].get()))
            cval = cval * 100
            minutes = int(float(self.minute[x].get()))
            seconds = int(float(self.second[x].get()))

            print(type(address), type(loc), type(vval), type(cval), type(minutes), type(seconds))
            print(address, loc, vval, cval, minutes, seconds)
            print("PROP"+"%02d"%address+"%02d"%loc+"%03d"%vval+"%03d"%cval+"%02d"%minutes+"%02d\r"%seconds)
            sdpWrite("PROP"+"%02d"%address+"%02d"%loc+"%03d"%vval+"%03d"%cval+"%02d"%minutes+"%02d\r"%seconds, ser)
        times = int(1) # run one time
        runProgram(ser, times)

    def stopProgram(self, event, serial = ser, address=0):
        """Stop a running program"""
        sdpWrite("STOP"+"%02d\r"%address, ser)

def runProgram(serial, times, address=0):
    """Run the timed program:
    (times) - the number of time to run the program, 0-256 (0 = infinite)"""
    print("RUNP"+"%02d"%address+"%03d\r"%times, ser)
    sdpWrite("RUNP"+"%02d"%address+"%04d\r"%times, ser)

def getMaxVoltCurr(serial, address=0):
    """Get the maximum voltage and current from the supply. The response is an array: [0] = voltage, [1] = current"""
    resp = sdpQuery("GMAX"+"%02d"%address+"\r", serial)
    #return [int(resp[0:3])/10., int(resp[0][3:5])/10.]  #had to edit the parsing for Python 3, see next line
    return [int(str(int(resp))[0:3])/10., int(str(int(resp))[3:6])/100.]

def sdpWrite(cmd, serial):
    ser.write(cmd.encode())
    #return ser.read_until(terminator=b'\r')  #prior to v3.5
    return ser.read_until(expected=b'\r')

def sdpQuery(cmd, serial):
    resp = []
    notDone = True
    ser.write(cmd.encode())
    while(notDone):
        #r = ser.read_until(terminator=b'\r')  #prior to v3.5
        r = ser.read_until(expected=b'\r')
        if(not(len(r) > 0)):
           notDone = False
        else:
            resp.append(r)
    return resp[0]

def remoteMode(state, address=0):
    """Enable or Disable Remote mode. Other commands over usb automatically set PS to remote"""
    """state - True/False = Enable/Disable"""
    if state == True:
        sdpWrite("SESS"+"%02d"%address+"\r", serial)
        print(state)
    else:
        sdpWrite("ENDS"+"%02d"%address+"\r", serial)
        print(state)


def main():
    root = tk.Tk()
    app = MainWindow(root)
    app.grid()
    root.mainloop()

if __name__ == '__main__':
    main()

