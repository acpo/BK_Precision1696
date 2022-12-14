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
        self.volt0.insert(0, 1.0)
        self.volt0.bind('<Return>', self.setVolt) and self.volt0.bind('<Tab>', self.setVolt)
        self.volt0.grid(column=1, row=1)
        self.volt1 = tk.Entry(width='5')
        self.volt1.insert(0, 1.0)
        self.volt1.bind('<Return>', self.setVolt) and self.volt1.bind('<Tab>', self.setVolt)
        self.volt1.grid(column=1, row=2)
        self.volt2 = tk.Entry(width='5')
        self.volt2.insert(0, 1.0)
        self.volt2.bind('<Return>', self.setVolt) and self.volt2.bind('<Tab>', self.setVolt)
        self.volt2.grid(column=1, row=3)
        self.volt3 = tk.Entry(width='5')
        self.volt3.insert(0, 1.0)
        self.volt3.bind('<Return>', self.setVolt) and self.volt3.bind('<Tab>', self.setVolt)
        self.volt3.grid(column=1, row=4)
        self.volt4 = tk.Entry(width='5')
        self.volt4.insert(0, 1.0)
        self.volt4.bind('<Return>', self.setVolt) and self.volt4.bind('<Tab>', self.setVolt)
        self.volt4.grid(column=1, row=5)
        self.volt5 = tk.Entry(width='5')
        self.volt5.insert(0, 1.0)
        self.volt5.bind('<Return>', self.setVolt) and self.volt5.bind('<Tab>', self.setVolt)
        self.volt5.grid(column=1, row=6)

        tk.Label(text = "Current", font='bold', fg='blue').grid(row=0,column=2)
        self.current0 = tk.Entry(width='5')
        self.current0.insert(0, 0.0)
        self.current0.bind('<Return>', self.setCur) and self.current0.bind('<Tab>', self.setCur)
        self.current0.grid(column=2, row=1)
        self.current1 = tk.Entry(width='5')
        self.current1.insert(0, 0.0)
        self.current1.bind('<Return>', self.setCur) and self.current1.bind('<Tab>', self.setCur)
        self.current1.grid(column=2, row=2)
        self.current2 = tk.Entry(width='5')
        self.current2.insert(0, 0.0)
        self.current2.bind('<Return>', self.setCur) and self.current2.bind('<Tab>', self.setCur)
        self.current2.grid(column=2, row=3)
        self.current3 = tk.Entry(width='5')
        self.current3.insert(0, 0.0)
        self.current3.bind('<Return>', self.setCur) and self.current3.bind('<Tab>', self.setCur)
        self.current3.grid(column=2, row=4)
        self.current4 = tk.Entry(width='5')
        self.current4.insert(0, 0.0)
        self.current4.bind('<Return>', self.setCur) and self.current4.bind('<Tab>', self.setCur)
        self.current4.grid(column=2, row=5)
        self.current5 = tk.Entry(width='5')
        self.current5.insert(0, 0.0)
        self.current5.bind('<Return>', self.setCur) and self.current5.bind('<Tab>', self.setCur)
        self.current5.grid(column=2, row=6)

        tk.Label(text = "Minutes", font='bold', fg='blue').grid(row=0,column=3) #values 0 to 59
        self.minute0 = tk.Entry(width='5')
        self.minute0.insert(0, 0)
        self.minute0.bind('<Return>', self.setTime) and self.minute0.bind('<Tab>', self.setTime)
        self.minute0.grid(column=3, row=1)
        self.minute1 = tk.Entry(width='5')
        self.minute1.insert(0, 0)
        self.minute1.bind('<Return>', self.setTime) and self.minute1.bind('<Tab>', self.setTime)
        self.minute1.grid(column=3, row=2)
        self.minute2 = tk.Entry(width='5')
        self.minute2.insert(0, 0)
        self.minute2.bind('<Return>', self.setTime) and self.minute2.bind('<Tab>', self.setTime)
        self.minute2.grid(column=3, row=3)
        self.minute3 = tk.Entry(width='5')
        self.minute3.insert(0, 0)
        self.minute3.bind('<Return>', self.setTime) and self.minute3.bind('<Tab>', self.setTime)
        self.minute3.grid(column=3, row=4)
        self.minute4 = tk.Entry(width='5')
        self.minute4.insert(0, 0)
        self.minute4.bind('<Return>', self.setTime) and self.minute4.bind('<Tab>', self.setTime)
        self.minute4.grid(column=3, row=5)
        self.minute5 = tk.Entry(width='5')
        self.minute5.insert(0, 0)
        self.minute5.bind('<Return>', self.setTime) and self.minute5.bind('<Tab>', self.setTime)
        self.minute5.grid(column=3, row=6)

        tk.Label(text = "Seconds", font='bold', fg='blue').grid(row=0,column=4) #values 0 to 59
        self.second0 = tk.Entry(width='5')
        self.second0.insert(0, 0)
        self.second0.bind('<Return>', self.setTime) and self.second0.bind('<Tab>', self.setTime)
        self.second0.grid(column=4, row=1)
        self.second1 = tk.Entry(width='5')
        self.second1.insert(0, 0)
        self.second1.bind('<Return>', self.setTime) and self.second1.bind('<Tab>', self.setTime)
        self.second1.grid(column=4, row=2)
        self.second2 = tk.Entry(width='5')
        self.second2.insert(0, 0)
        self.second2.bind('<Return>', self.setTime) and self.second2.bind('<Tab>', self.setTime)
        self.second2.grid(column=4, row=3)
        self.second3 = tk.Entry(width='5')
        self.second3.insert(0, 0)
        self.second3.bind('<Return>', self.setTime) and self.second3.bind('<Tab>', self.setTime)
        self.second3.grid(column=4, row=4)
        self.second4 = tk.Entry(width='5')
        self.second4.insert(0, 0)
        self.second4.bind('<Return>', self.setTime) and self.second4.bind('<Tab>', self.setTime)
        self.second4.grid(column=4, row=5)
        self.second5 = tk.Entry(width='5')
        self.second5.insert(0, 0)
        self.second5.bind('<Return>', self.setTime) and self.second5.bind('<Tab>', self.setTime)
        self.second5.grid(column=4, row=6)

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

    def setVolt(self, event):        
        voltages = [self.volt0, self.volt1, self.volt2, self.volt3, self.volt4, self.volt5]
        for x in voltages:
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
        currents = [self.current0, self.current1, self.current2, self.current3, self.current4, self.current5]
        for x in currents:
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
        seconds = [self.second0, self.second1, self.second2, self.second3, self.second4, self.second5]
        minutes = [self.minute0, self.minute1, self.minute2, self.minute3, self.minute4, self.minute5]
        for x in seconds:
            # check each seconds to see if between 0 and 59
            sec = x.get()
            print(sec)
            try:
                float(sec) # can entry be coverted to float?
                if (float(sec) < 59) and (float(sec) >= 0):
                    x.delete(0, 'end')
                    x.insert(0, float(sec))
                else:
                    x.delete(0, 'end')
                    x.insert(0, 0)
            except:
                x.delete(0, 'end')
                x.insert(0, 0)
            
        for y in minutes:
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
            maxvalues = getMaxVoltCurr(ser)
            print (maxvalues[1], " amps")
            print (maxvalues[0], " volts")
            self.maxVolt = maxvalues[0]
            self.maxAmp = maxvalues[1]

    def sendProgram(self, event):
        if ConnectState:  #if connected
            print("send string...")
            # construct strings
            
            #sdpWrite()
            # end construct strings
        else:
            pass

def setupProgramMemory(serial, location, voltage, current, minutes, seconds, address=0):
    """Setup a program memory location"""
    """location - 0-19"""
    """voltage, current - xx.xx"""
    """minutes, seconds - whole numbers"""
    # needs to be modified with a loop 0 to 4 (5 steps, loc 0-4) and pull the step-number volt, etc.
    steps = [0, 1, 2, 3, 4, 5]
    for x in steps:
        loc = int(x)
        vval = int(voltage[x]) # need to store voltages in arrays

        
    loc = int(location)
    vval = int(voltage*10)
    cval = int(current*100)
    sdpWrite("PROP"+"%02d"%address+"%2d"%loc+"%3d"%vval+"%03d"%cval+"%02d"%minutes+"%02d\r"%seconds, serial)

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
