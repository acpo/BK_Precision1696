try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    import tkinter.filedialog   #seems to be necessary to be explicit about this dialog
from tkinter import messagebox
import tkinter.ttk as ttk

import serial
import serial.tools.list_ports

ser = serial.Serial()
 #port=None,  # not specifying a port initially, wait for scanSerial to populate options
ser.baudrate=9600
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.bytesize=serial.EIGHTBITS
ser.timeout = 1
ser.writeTimeout = 0        #ensure non-blocking
## exceptions won't occur unless truly zero COM ports on the computer.

CommPort = "no connection"  #set initial value

class MainWindow(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.maxVolt = 20 #dummy limit until serial port connects
        self.maxAmp = 10  #dummy limit until serial port connects
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
            entryC.insert(0, 1.00)
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

        self.PSconnect = tk.Button(text='Connect/Disconnect', bg = "pink", font='bold')
        self.PSconnect.grid(column=0, row=7, columnspan=2)
        self.PSconnect.bind('<ButtonRelease-1>', self.Connect_PS)

        self.button_Send = tk.Button(text = "Send program to PS", font='bold')
        self.button_Send.grid(column=0, row=8, columnspan=2)
        self.button_Send.bind('<ButtonRelease-1>', self.setupProgramMemory)

        tk.Label(text = "Max Volts =",).grid(column=3, row=7)
        self.maxVoltBox = tk.Label(text = "---", width=5)
        self.maxVoltBox.grid(column=4, row=7)
        tk.Label(text = "Max Amps =",).grid(column=3, row=8)
        self.maxAmpBox = tk.Label(text = "---", width=5)
        self.maxAmpBox.grid(column=4, row=8)

        self.button_Run = tk.Button(text = "Run program", bg = "powder blue", font='bold')
        self.button_Run.grid(column = 0, row = 9, columnspan=2)
        self.button_Run.bind('<ButtonRelease-1>', self.runProgram)

        self.button_stop = tk.Button(text = "STOP", bg="red", font='bold')
        self.button_stop.grid(column = 3, row = 9)
        self.button_stop.bind('<ButtonRelease-1>', self.stopProgram)

        tk.Label(text = "COM port", relief = 'sunken').grid(column=0, row=10, pady=10)
        # list of ports populated by PySerial call
        # the getComm function below in the Connect/Disconnect function chechecks that it is valid.
        self.ports_box = ttk.Combobox(values = scanSerial())
        self.ports_box.grid(column = 1, row = 10)
        self.ports_box.bind('<<ComboboxSelected>>', self.on_selectComm)
                
        self.button_write = tk.Button(text = "Write program", font='bold')
        self.button_write.grid(row=11, column=0, columnspan=2)
        self.button_write.bind('<ButtonRelease-1>', self.writeProgram)

        self.button_read = tk.Button(text = "Read program", font='bold')
        self.button_read.grid(row = 11, column=3, columnspan=2)
        self.button_read.bind('<ButtonRelease-1>', self.readProgram)


    def setVolt(self, event):        
        for x in self.volt:
            volt = x.get()
            try:
                float(volt) # can entry be coverted to float?
                if (float(volt) <= self.maxVolt) and (float(volt) >= 1.0):
                    x.delete(0, 'end')
                    x.insert(0, float(volt))
                    x.config({"background": "White"})
                else:
                    x.delete(0, 'end')
                    x.insert(0, 1.0)
                    x.config({"background": "Pink"})
            except:
                x.delete(0, 'end')
                x.insert(0, 1.0)
                x.config({"background": "Pink"})

    def setCur(self, event):        
        for x in self.current:
            cur = x.get()
            try:
                float(cur) # can entry be coverted to float?
                if (float(cur) <= self.maxAmp) and (float(cur) >= 0):
                    x.delete(0, 'end')
                    x.insert(0, float(cur))
                    x.config({"background": "White"})
                else:
                    x.delete(0, 'end')
                    x.insert(0, 0.00)
                    x.config({"background": "Pink"})
            except:
                x.delete(0, 'end')
                x.insert(0, 0.00)
                x.config({"background": "Pink"})
                
    def setTime(self, event):        
        for x in self.second:
            # check each seconds to see if between 0 and 59
            sec = x.get()
            try:
                float(sec) # can entry be coverted to float?
                if (float(sec) <= 59) and (float(sec) >= 0):
                    x.delete(0, 'end')
                    x.insert(0, float(sec))
                    x.config({"background": "White"})
                else:
                    x.delete(0, 'end')
                    x.insert(0, 0)
                    x.config({"background": "Pink"})
            except:
                x.delete(0, 'end')
                x.insert(0, 0)
                x.config({"background": "Pink"})
            
        for y in self.minute:
            # check each minutes if between 0 and 99
            min = y.get()
            try:
                float(min) # can entry be coverted to float?
                if (float(min) < 59) and (float(min) >= 0):
                    y.delete(0, 'end')
                    y.insert(0, float(min))
                    y.config({"background": "White"})
                else:
                    y.delete(0, 'end')
                    y.insert(0, 0)
                    y.config({"background": "Pink"})

            except:
                y.delete(0, 'end')
                y.insert(0, 0)
                y.config({"background": "Pink"})

    def Connect_PS(self, event):
        if (ser.isOpen() == True):  #checks if serial port is open
            try:
                self.PSconnect.configure(background = 'pink')
                ser.close()
            except:
                print("exception")
                self.PSconnect.configure(background = 'pink')
        else:
            ser.open()
            self.PSconnect.configure(background = 'light green')
            CommPort = getComm(ser) #query to power supply to verify Comm Port
            try:
                maxvalues = getMaxVoltCurr(ser)
                self.maxVolt = maxvalues[0]
                self.maxAmp = maxvalues[1]
                self.maxVoltBox.config(text = maxvalues[0])
                self.maxAmpBox.config(text = maxvalues[1])
                self.setCur(event)
                self.setVolt(event)
            except:
                print("exception")
                self.PSconnect.configure(background = 'pink')


    def setupProgramMemory(self, event, address=0, serial = ser): #serial, location, voltage, current, minutes, seconds, address=0):
        """Setup a program memory location"""
        """location - 0-19"""
        """voltage, current - xx.xx"""
        """minutes, seconds - whole numbers"""
        # needs to be modified with a loop 0 to 4 (5 steps, loc 0-4) and pull the step-number volt, etc.
        if(ser.isOpen() == False):  # check if serial port is open
            ser.open()
        steps = [0, 1, 2, 3, 4, 5]
        for x in steps:
            loc = int(x)
            vval = 10 *(float(self.volt[x].get())) # need to store voltages in arrays
            vval = int(vval)
            cval = 100 * (float(self.current[x].get()))
            cval = int(cval)
            minutes = int(float(self.minute[x].get()))
            seconds = int(float(self.second[x].get()))

            #print(type(address), type(loc), type(vval), type(cval), type(minutes), type(seconds))
            #print(address, loc, vval, cval, minutes, seconds)
            #print("PROP"+"%02d"%address+"%02d"%loc+"%03d"%vval+"%03d"%cval+"%02d"%minutes+"%02d\r"%seconds)
            sdpWrite("PROP"+"%02d"%address+"%02d"%loc+"%03d"%vval+"%03d"%cval+"%02d"%minutes+"%02d\r"%seconds, ser)
        times = int(1) # run one time

    def stopProgram(self, event, serial = ser, address=0):
        """Stop a running program"""
        sdpWrite("STOP"+"%02d\r"%address, ser)

    def runProgram(self, event, serial = ser, times=1, address=0):
        """Run the timed program:
        (times) - the number of time to run the program, 0-256 (0 = infinite)"""
        if(ser.isOpen() == True):   #checks for True
            sdpWrite("SOUT"+"%02d"%address+"0\r", serial) # connects outputs on BK 1696
            sdpWrite("RUNP"+"%02d"%address+"%04d\r"%times, serial)
        else:
            sdpWrite("SOUT"+"%02d"%address+"1\r", serial) # disconnects output
            print("no connection")
            pass

    def writeProgram(self, event):
        address = 0  # this is the only option for address of multistep program
        filename = tk.filedialog.asksaveasfile(title = "Select program to write", filetypes = [("Text file",".txt"),("CSV file",".csv")], defaultextension='.txt')
        if not filename:
            pass  #exits dialog on Cancel
        else:
            with open(filename.name, 'w') as file:
                steps = [0, 1, 2, 3, 4, 5]
                for x in steps:
                    loc = int(x)
                    vval = 10 *(float(self.volt[x].get())) # need to store voltages in arrays
                    vval = int(vval) # need to store integers because 'read' requires them
                    cval = 100 * (float(self.current[x].get()))
                    cval = int(cval)
                    minutes = int(float(self.minute[x].get()))
                    seconds = int(float(self.second[x].get()))
                    progstring = str(address) + "\n" + str(loc) + "\n" + str(self.volt[x].get()) + "\n" + str(self.current[x].get()) + "\n" + str(minutes) + "\n" + str(seconds) + "\n"
                    file.write(progstring) # writes one value per line

    def readProgram(self, event):
        filename = tk.filedialog.askopenfilename(title = "Select program to read", filetypes = [("Text file",".txt"),("CSV file",".csv")], defaultextension='.txt', multiple=False)
        if not filename:
            pass  #exits dialog on Cancel
        else:
            steps = [0, 1, 2, 3, 4, 5]
            with open(filename) as file:
                for x in steps:
                    address = file.readline()
                    loc = file.readline()
                    ## can't set lists directly, instead write to the Entry Boxes directly
                    self.volt[x].delete(0, 'end')
                    self.volt[x].insert(0, float(file.readline())) 
                    self.current[x].delete(0, 'end')
                    self.current[x].insert(0, float(file.readline())) 
                    self.minute[x].delete(0, 'end')
                    self.minute[x].insert(0, float(file.readline())) 
                    self.second[x].delete(0, 'end')
                    self.second[x].insert(0, float(file.readline())) 
            self.setVolt(event) # checks values after read
            self.setCur(event)
            self.setTime(event)

    def on_selectComm(self, event):
        global ser
        port = self.ports_box.get()
        ser.port = port
        ser.open()

# Service functions below
def getMaxVoltCurr(serial, address=0):
    """Get the maximum voltage and current from the supply. The response is an array: [0] = voltage, [1] = current"""
    resp = sdpQuery("GMAX"+"%02d"%address+"\r", serial)
    #return [int(resp[0:3])/10., int(resp[0][3:5])/10.]  #had to edit the parsing for Python 3, see next line
    return [int(str(int(resp))[0:3])/10., int(str(int(resp))[3:6])/100.]

def getComm(serial, address=0):
    """Get the comm settings"""
    """Returns address """
    resp = sdpQuery("GCOM"+"%02d"%address+"\r", serial)
    return int(resp) 

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
    else:
        sdpWrite("ENDS"+"%02d"%address+"\r", serial)

def scanSerial():
    ports = serial.tools.list_ports.comports()
    com_list = []
    for p in ports:
        com_list.append(p.name)
    return com_list


def main():
    root = tk.Tk()
    app = MainWindow(root)
    app.grid()
    root.mainloop()

if __name__ == '__main__':
    main()

