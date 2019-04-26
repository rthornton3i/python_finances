from atlaas import Query
from record import Write

import os
import time
from datetime import datetime,timedelta
import tkinter as tk
from tkinter.filedialog import askdirectory as filedir, askopenfilename as fileopen, asksaveasfilename as filesave
from tkinter import messagebox
import pickle

class App:

    def __init__(self, root):
        self.root = root
        
        self.root.geometry('700x470')
        self.root.resizable(width=False,height=False)
        
        self.root.title('Atlaas Inputs')
        
        self.main()
        
    def varSave(self):
        self.sats = [self.satList.get(n) for n in range(self.satList.size())]
        self.tf = [self.tf1.get(),self.tf2.get()]
        self.dbType = self.dbVar.get()
        self.mnems = [self.telemList.get(n) for n in range(self.telemList.size())]
        self.file = self.fnField.get() if '.xlsx' in self.fnField.get() or '.xls' in self.fnField.get() else self.fnField.get() + '.xlsx'
        self.path = self.dirField.get()
        
        self.varList = [self.sats,self.tf,self.dbType,self.mnems,self.file,self.path]
        
    def main(self): 
        def run():
            self.varSave()
            
            startTime = time.time()
            
            print('Accessing database...')
            sql = Query(self.sats,self.tf,self.dbType,self.mnems)
            self.results = sql.query()
            
            print('Savings results...')
            Write(self.results,self.sats,self.mnems,self.path,self.file)
            
            runTime = time.time() - startTime
            print('Total run time: ',str(round(runTime,2)),' seconds\n')
        
        def close():
            self.root.destroy()
        
        ##Menu
        self.menu()
        
        ##Mnemonics
        self.mnemonics()
        
        ##Satellite
        self.satellites()      
        
        ##Time Frame
        self.timeFrame()        
        
        ##Database Type
        self.databaseType()
        
        ##File name
        self.filename()        
        
        ##Directory
        self.directory()
        
        ##Run/Close
        #Run Button
        runBut = tk.Button(self.root,
            text="Run",
#            font=('Helvetica',10,'bold'),
            command=run)
        runBut.pack()
        runBut.place(height=30,width=125,x=162.5,y=430)
        
        #Close Button
        closeBut = tk.Button(self.root,
            text="Close",
#            font=('Helvetica',10,'bold'),
            command=close)
        closeBut.pack()
        closeBut.place(height=30,width=125,x=412.5,y=430)

#==============================================================================

    def menu(self):
        def menuNew():
            #Telemetry
            self.telemList.delete(0,'end')
            
            #Satellites
            self.satList.delete(0,'end')
            
            #Time Frame
            self.tf1.delete(0,'end')
            self.tf2.delete(0,'end')
            self.tf1.insert(0,(datetime.now()-timedelta(days=2)).strftime("%Y-%m-%d"))
            self.tf2.insert(0,(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d"))
            
            #Database
            self.dbVar.set(None)
            
            #File name
            fn = self.fnField.get()
            self.fnField.delete(0,'end')
            if fn.find('_') < 0:
                self.fnField.insert(0,fn.replace('.xlsx','_01.xlsx'))
            else:
                fnInd = int(fn[fn.find('_')+1:fn.find('_')+3])
                self.fnField.insert(0,fn.replace('_'+str(fnInd).zfill(2)+'.xlsx','_'+str(fnInd+1).zfill(2)+'.xlsx'))
        
        def menuOpen():
            varFile = fileopen(initialdir=str(os.path.dirname(os.path.realpath(__file__))),
                               title="Select Variable File",
                               filetypes=(("pickle files","*.pickle"),("all files","*.*")))
                               
            variables = open(varFile,'rb')
            varList = pickle.load(variables)
            variables.close()
            
            self.sats = varList[0]
            self.tf = varList[1]
            self.dbType = varList[2]
            self.mnems = varList[3]
            self.file = varList[4]
            self.path = varList[5]
            
            #Telemetry
            self.telemList.delete(0,'end')
            for mnem in self.mnems:
                self.telemList.insert('end',mnem)
            
            #Satellites
            self.satList.delete(0,'end')
            for sat in self.sats:
                self.satList.insert('end',sat)
            
            #Time Frame
            self.tf1.delete(0,'end')
            self.tf2.delete(0,'end')
            self.tf1.insert(0,self.tf[0])
            self.tf2.insert(0,self.tf[1])
            
            #Database
            self.dbVar.set(self.dbType)
            
            #File name
            self.fnField.delete(0,'end')
            self.fnField.insert(0,self.file)
            
            #Path
            self.dirField.delete(0,'end')
            self.dirField.insert(0,self.path)
            
        def menuSave():
            self.varSave()
            
            if not hasattr(self,'varFile'):
                self.varFile = filesave(initialdir=str(os.path.dirname(os.path.realpath(__file__))),
                                        title="Select Directory",
                                        defaultextension=".pickle",
                                        filetypes=(("pickle files","*.pickle"),("all files","*.*")))
            
            variables = open(self.varFile,'wb')
            pickle.dump(self.varList, variables)
            variables.close()
        
        def menuAbout():
            messagebox.showinfo("About", "ehhhh, this is a message box, it does some stuff... fuhgetaboutit")
            
        menubar = tk.Menu(self.root)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=menuNew)
        filemenu.add_command(label="Open", command=menuOpen)
        filemenu.add_command(label="Save", command=menuSave)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.destroy)
        
        menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=menuAbout)
        
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.root.config(menu=menubar)
    
    def mnemonics(self):
        def addMnem():
            listedTelems = [telemList.get(n) for n in range(telemList.size())]
            mnem = telem.get()
            
            if mnem != '' and mnem not in listedTelems:
                telemList.insert('end',mnem)
            
            telem.delete(0,'end')
    
        def remMnem():
            telemList.delete('active')
            
        def clearMnem():
            telemList.delete(0,'end')
        
        #Mnemonic Label
        telemLabel = tk.Label(self.root,
            text='Mnemonic: ')
        telemLabel.pack(anchor=tk.W)
        telemLabel.place(height=30,x=10,y=10)
        
        #Mnemonic Entry
        telem = tk.Entry(self.root)
        telem.pack()
        telem.place(height=30,width=125,x=100,y=10)
        
        #Mnemonic Add
        telemAdd = tk.Button(self.root,
            text="Add",
            command=addMnem)
        telemAdd.pack()
        telemAdd.place(height=30,width=100,x=240,y=10)
        
        #Mnemonic Remove
        telemRem = tk.Button(self.root,
            text="Remove",
            command=remMnem)
        telemRem.pack()
        telemRem.place(height=30,width=100,x=240,y=55)
        
        #Mnemonic Clear
        telemCl = tk.Button(self.root,
            text="Clear",
            command=clearMnem)
        telemCl.pack()
        telemCl.place(height=30,width=100,x=240,y=175)
        
        #Mnemonic List
        telemList = tk.Listbox(self.root)
        
        telemScroll = tk.Scrollbar(telemList)
        telemScroll.config(command=telemList.yview)
        telemList.config(yscrollcommand=telemScroll.set)
        
        telemScroll.pack(side='right',fill='y')
        telemList.pack()
        telemList.place(height=150,width=125,x=100,y=55)
        
        self.telemList = telemList
    
    def satellites(self):
        def addSat():
            listedSats = [satList.get(n) for n in range(satList.size())]
            newSat = sat.get()
            
            if newSat not in listedSats:
                satList.insert('end',newSat)
        
        def remSat():
            satList.delete('active')
            
        def clearSat():
            satList.delete(0,'end')
        
        #Satellite Label            
        satLabel = tk.Label(self.root,
            text='Satellite: ')
        satLabel.pack(anchor=tk.W)
        satLabel.place(height=30,x=360,y=10)  
        
        #Satellite Drop Down
        sats = {'F15','F16','F17','F18'}
        sat = tk.StringVar(self.root)
        
        satDrop = tk.OptionMenu(self.root,
            sat,
            *sats)
        satDrop.pack()
        satDrop.place(height=30,width=125,x=450,y=10)
        
        #Satellite Add
        satAdd = tk.Button(self.root,
            text="Add",
            command=addSat)
        satAdd.pack()
        satAdd.place(height=30,width=100,x=590,y=10)
        
        #Satellite Remove
        satRem = tk.Button(self.root,
            text="Remove",
            command=remSat)
        satRem.pack()
        satRem.place(height=30,width=100,x=590,y=55)
        
        #Satellite Clear
        satCl = tk.Button(self.root,
            text="Clear",
            command=clearSat)
        satCl.pack()
        satCl.place(height=30,width=100,x=590,y=175)
        
        #Satellite List
        satList = tk.Listbox(self.root)
        
        satScroll = tk.Scrollbar(satList)
        satScroll.config(command=satList.yview)
        satList.config(yscrollcommand=satScroll.set)
        
        satScroll.pack(side='right',fill='y')
        satList.pack()
        satList.place(height=150,width=125,x=450,y=55)  
        
        self.satList = satList
        
    def timeFrame(self):
        #Time Frame Label            
        tfLabel = tk.Label(self.root,
            text='Time Frame: ')
        tfLabel.pack(anchor=tk.W)
        tfLabel.place(height=30,x=10,y=220)
        
        #Time Frame Input
        tf1 = tk.Entry(self.root)
        tf1.pack()
        tf1.place(height=30,width=125,x=100,y=220)
        tf1.insert(0,(datetime.now()-timedelta(days=2)).strftime("%Y-%m-%d"))
        
        tf2 = tk.Entry(self.root)
        tf2.pack()
        tf2.place(height=30,width=125,x=100,y=280)
        tf2.insert(0,(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d"))
        
        #Time Frame Units
        tfStart = tk.Label(self.root,
            text='Start Date',
            font=('Helvetica',8,'italic'))
        tfStart.pack(anchor=tk.W)
        tfStart.place(height=30,x=230,y=220)
        
        tfEnd = tk.Label(self.root,
            text='End Date',
            font=('Helvetica',8,'italic'))
        tfEnd.pack(anchor=tk.W)
        tfEnd.place(height=30,x=230,y=280)
        
        #Time Frame Notes
        tfUnit1 = tk.Label(self.root,
            text='YYYY-MM-DD',
            font=('Helvetica',6,'italic'))
        tfUnit1.pack(anchor=tk.NW)
        tfUnit1.place(height=30,x=100,y=250)
        
        tfUnit2 = tk.Label(self.root,
            text='YYYY-MM-DD',
            font=('Helvetica',6,'italic'))
        tfUnit2.pack(anchor=tk.NW)
        tfUnit2.place(height=30,x=100,y=310)
        
        self.tf1 = tf1
        self.tf2 = tf2
        
    def databaseType(self):
        #Database Label            
        dbLabel = tk.Label(self.root,
            text='Database: ')
        dbLabel.pack(anchor=tk.W)
        dbLabel.place(height=30,x=360,y=220)
        
        #Database Radio Buttons
        dbVar = tk.IntVar(self.root)
        
        dbTrend = tk.Radiobutton(self.root, 
            text="Trend",
            variable=dbVar, 
            value=1)
        dbTrend.pack()
        dbTrend.place(x=450,y=220)
        
        dbFull = tk.Radiobutton(self.root, 
            text="Full",
            variable=dbVar, 
            value=2)
        dbFull.pack()
        dbFull.place(x=450,y=250)    
        
        self.dbVar = dbVar
        
    def filename(self):
        #File Name Label
        fnLabel = tk.Label(self.root,
            text='File Name: ')
        fnLabel.pack(anchor=tk.W)
        fnLabel.place(height=30,x=10,y=340)
        
        #File Name Field
        fnField = tk.Entry(self.root)
        fnField.pack()
        fnField.place(height=30,width=240,x=100,y=340)
        
        fnField.insert(0,'telemetryData.xlsx')
        
        self.fnField = fnField
        
    def directory(self):
        def direct():
            path = filedir(initialdir=str(os.path.dirname(os.path.realpath(__file__))),
                           title="Select Directory")
             
            dirField.delete(0,'end')
            dirField.insert(0,path)
        
        #Directory Label
        dirLabel = tk.Label(self.root,
            text='Folder: ')
        dirLabel.pack(anchor=tk.W)
        dirLabel.place(height=30,x=10,y=385)
        
        #Directory Field
        dirField = tk.Entry(self.root)
        dirField.pack()
        dirField.place(height=30,width=475,x=100,y=385)
        dirField.insert(0,str(os.path.dirname(os.path.realpath(__file__))))
        
        #Directory Search Button
        dirBut = tk.Button(self.root,
            text="Select",
            command=direct)
        dirBut.pack()
        dirBut.place(height=30,width=100,x=590,y=385)
        
        self.dirField = dirField  