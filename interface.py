from tkinter import ttk, Menu, Toplevel, Tk, StringVar, CENTER, PhotoImage
from PIL import Image, ImageTk
from datetime import date
import abc
import os
import sys
import glob
import serial

class interface():

    date = date.today()

    def serial_ports(self, *args, **kwargs):
        """ Lists serial port names. CREDIT: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    
    def connect_serial(self):
        
        status = False
        try:
            s = serial.Serial(self.COM.get(), baudrate=9600, timeout=5)
            self.port = s
            if s.in_waiting != 0:
                f = open(os.path.join(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), "Penetrometer - " + self.date.strftime("%b-%d-%Y")), "w+")
                data = s.readline()
                f.write(data)
                f.close()
                s.close()
                status = True
            else:
                status = False
        except (OSError, serial.SerialException):
            status = False
        if status == True:
            self.connect_screen(self, status='hide')
            self.connected_screen(self, status='show')
        else:
            # self.connect_screen(self, init=True, text="ERROR: Unable to connect. Please try a different COM port.")
            self.connect_screen(self, status='hide')
            self.connected_screen(self, status='show')
    
    def save_data(self, *args, **kwargs):

        location = filedialog.askdirectory() + "VetGloveData"
        print(str(location))

        ################################################
        # https://www.freecodecamp.org/news/python-write-to-file-open-read-append-and-other-file-handling-functions-explained/
        # Used above to learn how to read and write files
        
        f = filename.strftime("%Y_%m_%d-%I;%M;%S_%p")
        try:
            with open(location + f +".txt", "x") as file:
                # file.write("Hello World")
                # Init serial communication to actually retrive the data:
                data = self.port#.read()
                file.write(data)
                messagebox.showinfo("Notification", "Your Data has been succesfully saved")
        
        except (FileExistsError, UnboundLocalError):
            pass

    def get_Com(self,event):
        return self.Com.get()

    def wipe(self, *args, **kwargs):
        print("Wiped...")
    
    def DIE(self, *args, **kwargs):
        self.root.destroy()
    
    def view(self, *args, **kwargs):
        return
    
    def branding_screen(self, *args, **kwargs):
        """ Show/Hide the branding frame.
        """

        if 'init' in kwargs and kwargs['init'] == True:
            self.branding = ttk.Frame(self.root)
            self.branding.grid(row=0, column=0, columnspan=2)
            self.branding.config(padding=(30,15), style='TFrame')

            self.logoRaw = Image.open(os.path.join(sys._MEIPASS, './images/FPLRS-logo (white background).png')).resize((175, 175), Image.ANTIALIAS)
            self.logo = ImageTk.PhotoImage(self.logoRaw)
            ttk.Label(self.branding, style="TLabel").grid(row=0, column=0)
            ttk.Label(self.branding, text="Penetrometer Data Extraction Interface", style="TLabel").grid(row=1, column=0)
            

        if kwargs['status'] == "show":
            self.branding.grid(row=0, column=0, columnspan=2)
        if kwargs['status'] == "hide":
            self.branding.grid_forget()
    
    def connect_screen(self, *args, **kwargs):
        """Show/Hide the COM port connect frame.
        """

        if 'init' in kwargs and kwargs['init'] == True:
            # Init layout
            self.connect = ttk.Frame(self.root)
            self.connect.grid(row=1, column=0, rowspan=3, columnspan=2)
            self.connect.config(padding=(30,15))

            # Conditionally create the message on this Frame, based on failed connection attempts.
            if 'text'in kwargs:
                message = kwargs['text']
                styleClass = "VG_Error.TLabel"
            else:
                message = "To start, please connect your device and select it from the list below."
                styleClass = "VG_Help.TLabel"

            #  Place the message using the Grid Manager:
            ttk.Label(self.connect, text=message, wraplength=200, justify=CENTER, style=styleClass).grid(row=0, column=0, columnspan=2)
            
            # Define dropdown to connect device:
            ttk.Label(self.connect, text='COM ports available:', style="TLabel").grid(row = 1, column = 0, columnspan=2)
            self.COM = StringVar()
            self.Com = ttk.Combobox(self.connect, textvariable = self.COM)
            self.Com.bind("<<ComboboxSelected>>", self.get_Com)
            self.Com.grid(row=2, column=0, columnspan=2)
            self.Com.config(values = self.serial_ports()) # WAS: ('COM4','COM6')
            
            # Define buttons to Connect/Exit:
            ttk.Button(self.connect, text="Exit", command=self.DIE).grid(row=3, column=0)
            ttk.Button(self.connect, text="Connect", command=self.connect_serial).grid(row=3, column=1)
        
        
        if kwargs['status'] == "show":
            self.connect.grid(row=1, column=0, rowspan=3, columnspan=2)
        if kwargs['status'] == "hide":
            self.connect.grid_forget()        


    def connected_screen(self, *args, **kwargs):
        """Show/Hide the data-download frame.
        """

        if 'init' in kwargs and kwargs['init'] == True:
            self.connected = ttk.Frame(self.root)
            self.connected.grid(row=1, column=0, rowspan=3, columnspan=2)
            self.connected.config(padding=(30,15))

            ttk.Label(self.branding, image=self.logo, style="TLabel").grid(row=0, column=0)
            ttk.Label(self.connected, text='CONNECTED!', foreground='Green', background='SlateGrey').grid(row=1, column=0, columnspan=2)

            ttk.Label(self.connected, text="Options:", style='TLabel').grid(row=2, column=0, columnspan=2)
            ttk.Button(self.connected, text="Download data", command=self.save_data).grid(row=3, column=0, 
                                                                                                  columnspan=2)
            ttk.Button(self.connected, text="Exit", command=self.DIE).grid(row=6, column=0, columnspan=2)

        if kwargs['status'] == "show":
            self.connected.grid(row=1, column=0, rowspan=3, columnspan=2)
        if kwargs['status'] == "hide":
            self.connected.grid_forget()
    
    def __init__(self):

        # Init GUI Interface:
        self.root = Tk()
        self.root.title("Penetrometer Interface")
        self.root.resizable(True, True)
        self.root.configure(background = 'SlateGrey')

        # Create Styles:
        self.style = ttk.Style(self.root)
        self.style.configure("TFrame", background='SlateGrey')
        self.style.configure("TLabel", background='SlateGrey', padding=(0,10,0,0), font=('TkDefaultFont', 16, 'bold'))
        self.style.configure("VG_Help.TLabel", background='SlateGrey', padding=(0,10,0,0), font=('TkDefaultFont', 12))
        self.style.configure("VG_Error.TLabel", background='SlateGrey', foreground="Red", padding=(0,10,0,0), font=('TkDefaultFont', 16, 'bold'))

        # Create intro layout:
        self.branding_screen(self, init=True, status='show')
        self.connect_screen(self, init=True, status='show')
        self.connected_screen(self, init=True, status='hide')
        # Run the GUI:
        self.root.mainloop()
interface()

# %% [markdown]

# ## Generate Executable:

# For this project, we are using the package [PyInstaller](http://www.pyinstaller.org/) to turn our TKinter GUI into a standalone executable file.

# This is acheived using the CLI command `pyinstaller yourprogram.py`, as per the PyInstaller Docs.
# %%
