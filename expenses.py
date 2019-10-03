import numpy as np
import random as r
import math

import matplotlib.pyplot as plt

class Expenses:
    
    def __init__(self,var,maxChildYr=22):
                    
        self.years = var['years']      
        self.salary = np.sum(var['salary']['salary'],axis=1)
        
        self.familyKids = var['children']['familyKids']
        self.childYrs = var['children']['childYrs']        
        self.childAges = var['children']['childAges']        
        
        self.rentPay = var['housing']['rentCosts']
        
        self.housePay = var['housing']['houseCosts'][1]
        self.houseWth = var['housing']['houseCosts'][3]
        self.houseDwn = var['housing']['houseCosts'][5]
        
        self.carPay = var['cars']['carCosts'][0]
        self.carWth = var['cars']['carCosts'][1]
        self.carDwn = var['cars']['carCosts'][2]
        
        self.totalLoan = var['loans']['totalLoan']
        
        self.maxChildYr = maxChildYr
        
    def holidayExp(self,holExp=[400,500,200,300],chExp=[100,200,300,500],famExp=[50,50]):
        """holExp = [B-day, X-mas, ValDay, Anniv]
           chExp  = [Base B-day, Add B-day, Base X-mas, Add X-mas]
           famExp = [B-day, X-mas]"""
           
        numFamily = np.ones((self.years,1)) * len(self.familyKids)
        familyBday = np.zeros((self.years,1))
        familyXmas = np.zeros((self.years,1))
        
        removeKid = [x + self.maxChildYr for x in self.familyKids]
        
        for n in range(self.years):
            for kid in self.familyKids:
                if n == kid:
                    numFamily[n:] = numFamily[n] + 1
            for kid in removeKid:
                if n == kid:
                    numFamily[n:] = numFamily[n] - 1
            
            familyBday[n] = famExp[0] * numFamily[n]
            familyXmas[n] = famExp[1] * numFamily[n]
        
        childBday = np.zeros((self.years,len(self.childYrs)))
        childXmas = np.zeros((self.years,len(self.childYrs)))
        
        for n in range(self.years):
            for m in range(len(self.childYrs)):
                if self.childAges[n,m] > 0:
                    childBday[n,m] = chExp[0] + ((self.childAges[n,m] / self.maxChildYr) * chExp[1])
                    childXmas[n,m] = chExp[2] + ((self.childAges[n,m] / self.maxChildYr) * chExp[3])
        
        childBday = np.sum(childBday, axis=1).reshape((self.years,1))
        childXmas = np.sum(childXmas, axis=1).reshape((self.years,1))
        
        totalHol = np.zeros((self.years,1))
        for n in range(self.years):
            totalHol[n] = sum(holExp) + familyBday[n] + familyXmas[n] + childBday[n] + childXmas[n]
        
        self.totalHol = totalHol
        
    def entExp(self,ent=[75*12,80*12],subs=[120,130,100],childFactor=0.2):
        """entProv = [wifi/cable, cellular]
           subs    = [netflix, amazon, hulu]"""
        
        totalEnt = np.zeros((self.years,1))
        for n in range(self.years):
            totalEnt[n] = sum(ent) + sum(subs)
        
            for m in range(len(self.childYrs)):
                if self.childAges[n,m] > 0:
                    totalEnt[n] = totalEnt[n] + (totalEnt[n] * childFactor) 
        
        self.totalEnt = totalEnt 
        
    def personalExp(self,pers=[150*12,100*12,120*12],childFactor=0.2):
        """entProv = [medical, clothing, hair/makeup]"""
           
        totalPers = np.zeros((self.years,1))
        for n in range(self.years):
            totalPers[n] = sum(pers)
        
            for m in range(len(self.childYrs)):
                if self.childAges[n,m] > 0:
                    totalPers[n] = totalPers[n] + (totalPers[n] * childFactor) 
        
        self.totalPers = totalPers
        
    def petExp(self,pet=[100*12,25*12,20*250]):
        """pet = [food, toys/acccessories, daycare/walker]"""
           
        totalPet = np.zeros((self.years,1))
        for n in range(self.years):
            totalPet[n] = sum(pet) + np.random.triangular(25,25,150)*12
        
        self.totalPet = totalPet
        
    def miscExp(self,misc=[450*12,200*12,200*12],growthFactor=0.5,childFactor=0.25):
        """misc = [groceries, restaurants/social, general/entertainment]"""
        
        totalMisc = np.zeros((self.years,1))
        for n in range(self.years):
            totalMisc[n] = sum(misc) + ((n / self.years) * (growthFactor * sum(misc)))
            
            for m in range(len(self.childYrs)):
                if self.childAges[n,m] > 0:
                    totalMisc[n] = totalMisc[n] + (totalMisc[n] * childFactor) 
        
        self.totalMisc = totalMisc  
        
    def housingExp(self):
        repHouse = np.zeros((self.years,1))
        insHouse = np.zeros((self.years,1))
        utilElec = np.zeros((self.years,1)) 
        utilGas = np.zeros((self.years,1))
        utilWater = np.zeros((self.years,1))
        
        for n in range(self.years):
            repHouse[n] = min(self.houseWth[n] * 0.015,50000)
            insHouse[n] = self.houseWth[n] * 0.005
            utilElec[n] = (60 + ((1/10000) * self.houseWth[n])) * 12
            utilGas[n] = (25 + ((1/25000) * self.houseWth[n])) * 12
            utilWater[n] = (30 + ((1/50000) * self.houseWth[n])) * 12
        
        totalHouse = repHouse + insHouse + utilElec + utilGas + utilWater + self.houseDwn + self.housePay + self.rentPay
        
        self.totalHouse = totalHouse
        
    def carExp(self,rates=[[1250*2,0.0125],[250*2,0.01]],ezPass=50*12*2,gas=[15000*2,35,2.5],childFactor=0.25):  
        """carYears = [Purchase Yr, Sell Yr, Amount ($), Down Payment ($)]
           rates = [Insurance Rate (%), Repair Cost/Yr (%)]
           exPass = EZ-Pass Cost
           gas = [Annual Mileage, MPG, Fuel Cost ($)]"""
           
        insCar = np.zeros((self.years,1))
        repCar = np.zeros((self.years,1))
        
        fuelCost = (gas[0] * gas[2]) / gas[1]
        
        for n in range(self.years):
            insCar[n] = rates[0][0] + (self.carWth[n] * rates[0][1])
            repCar[n] = rates[1][0] + (self.carWth[n] * rates[1][1])
            
            for m in range(len(self.childYrs)):
                if self.childAges[n,m] > 0:
                    insCar[n] = insCar[n] + (insCar[n] * childFactor) 
                    repCar[n] = repCar[n] + (repCar[n] * childFactor) 
        
        totalAuto = np.zeros((self.years,1))
        for n in range(self.years):
            totalAuto[n] = ezPass + fuelCost + insCar[n] + repCar[n] + self.carDwn[n] + self.carPay[n] 
        
        self.totalAuto = totalAuto
        
    def collegeExp(self,baseCol=50000):
        """baseCol = Annual College Cost ($)"""
        
        totalCollege = np.zeros((self.years,1))
        
        for n in range(self.years):
            for m in range(len(self.childYrs)):
                if self.childAges[n,m] >= 18 and self.childAges[n,m] <= 21:
                    totalCollege[n] = totalCollege[n] + baseCol
        
        self.totalCollege = totalCollege
        
    def wedExp(self,marYrs=[0,2],wedCost=[sum([20000,6000,1500,4000,1000,500,2000,1500,2500,1500]),10000,6500],parentCont=[sum([10000,1500]),7500]):
        """marYr = [Year of Engagement,Year of Wedding]
           wedCost = [Cost of Wedding, Cost of Honeymoon, Cost of Ring]
               Cost of Wedding = (Venue, Band, Florist, Photographer, Decor, Officiant, Rings, Dress, Rehersal Dinner, Gifts)"""        
        
        totalWed = np.zeros((self.years,1))
        
        totalWed[marYrs[0]]                           = wedCost[2] + (0.10 * wedCost[0]) - (0.10 * sum(parentCont))
        totalWed[int(np.mean([marYrs[0],marYrs[1]]))] = (0.30 * wedCost[0]) - (0.30 * sum(parentCont))
        totalWed[marYrs[1]]                           = wedCost[1] + (0.60 * wedCost[0]) - (0.60 * sum(parentCont))
        
        self.totalWed = totalWed
        
    def vacExp(self,baseVac=3000,growthFactor=1,childFactor=0.35):    
        """baseVac = Annual Vacation Cost ($)"""
        
        totalVac = np.zeros((self.years,1))
        
        for n in range(self.years):
            totalVac[n] = baseVac + ((n / self.years) * (growthFactor * baseVac))
            
            for m in range(len(self.childYrs)):
                if self.childAges[n,m] > 0:
                    totalVac[n] = totalVac[n] + (totalVac[n] * childFactor)
        
        self.totalVac = totalVac
        
    def charExp(self,baseChar=0.015):
        """baseChar = Annual Charity Donations (%)"""
        
        totalChar = np.zeros((self.years,1))
        
        for n in range(self.years):
            totalChar[n] = self.salary[n] * baseChar
        
        self.totalChar = totalChar
    
    def randExp(self,maxExp=25000,decayFactor=3,binWid=5):
        totalRand = np.zeros((self.years,1))
        
        x = np.arange(maxExp)
       #y = math.e ** (-x / (len(x) / decayFactor))
        
        expWid = maxExp * binWid / self.years
        
        for n in range(self.years):
            curBin = math.floor(n / binWid)
            
            while True:
                randFactor = r.random()
                expense = -(len(x) / decayFactor) * math.log(randFactor,math.e)
                expBin = math.floor(expense / expWid)
                
                if expBin <= curBin:
                    totalRand[n] = expense
                    break
        
        self.totalRand = totalRand
        
    def expRun(self):
        self.holidayExp()
        self.entExp()
        self.personalExp()
        self.petExp()
        self.miscExp()
        self.housingExp()
        self.carExp()
        self.collegeExp()
        self.wedExp()
        self.vacExp()
        self.charExp()
        self.randExp()

        self.totalExp = [self.totalHol,self.totalEnt,self.totalPers,self.totalPet,self.totalMisc,self.totalHouse,self.totalAuto,self.totalCollege,self.totalWed,self.totalVac,self.totalChar,self.totalRand,self.totalLoan]
        self.totalItem = [self.totalChar]