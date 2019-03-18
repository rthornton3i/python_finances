import numpy as np
import random as r
import math

class Expenses:
    
    def __init__(self,var,
                 houseCosts,carYears,
                 maxChildYr=22):
                     
        self.years = var['years']      
        self.salary = sum(var['salary'])
        
        self.familyKids = var['familyKids']
        self.childYrs = var['childYrs']        
        self.childAges = var['childAges']        
        
        self.housePay = houseCosts[1]
        self.houseWth = houseCosts[3]
        self.houseDwn = houseCosts[5]
        
        self.carYears = carYears
        
        self.maxChildYr = maxChildYr
        
    def holidayExp(self,holExp=[400,500,200,300],chExp=[100,200,300,1200],famExp=[50,50]):
        """holExp = [B-day, X-mas, ValDay, Anniv]
           chExp  = [Base B-day, Add B-day, Base X-mas, Add X-mas]
           famExp   = [B-day, X-mas]"""
           
        numFamily = np.full((self.years,1),len(self.familyKids))
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
        
    def entExp(self,entProv=[75*12,80*12],subs=[120,130,100]):
        """entProv = [wifi/cable, cellular]
           subs    = [netflix, amazon, hulu]"""
        
        totalEnt = np.zeros((self.years,1))
        for n in range(self.years):
            totalEnt[n] = sum(entProv) + sum(subs)
        
            for m in range(len(self.childYrs)):
                if self.childAges[n,m] > 0:
                    totalEnt[n] = totalEnt[n] + (totalEnt[n] * 0.05) 
        
        self.totalEnt = totalEnt 
        
    def miscExp(self,persCare=[150*12,450*12,200*12,200*12],growthFactor=0.5,childFactor=0.25):
        """persCar = [clothing/hair, groceries, restaurants, general]"""
        
        totalMisc = np.zeros((self.years,1))
        for n in range(self.years):
            totalMisc[n] = sum(persCare) + ((n / self.years) * (growthFactor * sum(persCare)))
            
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
        
        totalHouse = repHouse + insHouse + utilElec + utilGas + utilWater + self.houseDwn + self.housePay
        
        self.totalHouse = totalHouse   
        
    def carExp(self,rates=[0.075,0.025,0.019],term=60,ezPass=50*12,gas=[15000,35,2.5]):  
        """carYears = [Purchase Yr, Sell Yr, Amount ($), Down Payment ($)]
           rates = [Insurance Rate (%), Repair Cost/Yr (%), Loan Interest (%)]
           term = Loan Term Length
           exPass = EZ-Pass Cost
           gas = [Annual Mileage, MPG, Fuel Cost ($)]"""
           
        carMonthly = np.zeros((np.shape(self.carYears)[0],2))
        carPayment = np.zeros((self.years,1))
        carDown = np.zeros((self.years,1))
        insCar = np.zeros((self.years,1))
        repCar = np.zeros((self.years,1))
        
        fuelCost = (gas[0] * gas[2]) / gas[1]
        
        n = 0
        for car in self.carYears:
            carPrin = car[2] - car[3]
            carMonthly[n,0] = car[0]
            carMonthly[n,1] = ((rates[2] / 12) * carPrin) / (1 - (1 + (rates[2] / 12)) ** (-term))
    
            carDown[car[0]] = carDown[car[0]] + car[3]        
            
            n += 1
        
        yrs = round(term / 12)
        for n in range(self.years):
            for car in carMonthly:
                if n == car[0]:
                    carPayment[n:n+yrs] = carPayment[n:n+yrs] + (car[1] * 12)
            for car in self.carYears:
                if n >= car[0] and n < car[1]:
                    insCar[n] = insCar[n] + (car[2] * rates[0])
                    repCar[n] = repCar[n] + (car[2] * rates[1])    
        
        totalAuto = np.zeros((self.years,1))
        for n in range(self.years):
            totalAuto[n] = ezPass + fuelCost + carPayment[n] + insCar[n] + repCar[n] + carDown[n]
        
        self.totalAuto = totalAuto
        
    def collegeExp(self,baseCol=50000):
        """baseCol = Annual College Cost ($)"""
        
        totalCollege = np.zeros((self.years,1))
        
        for n in range(self.years):
            for m in range(len(self.childYrs)):
                if self.childAges[n,m] >= 18 and self.childAges[n,m] <= 21:
                    totalCollege[n] = totalCollege[n] + baseCol
        
        self.totalCollege = totalCollege
        
    def wedExp(self,marYrs=[2,3],wedCost=[25000,12500,6000]):
        """marYr = [Year of Engagement,Year of Wedding]
           wedCost = [Cost of Wedding, Cost of Honeymoon, Cost of Ring]"""        
        
        totalWed = np.zeros((self.years,1))
        
        totalWed[marYrs[0]] = totalWed[marYrs[0]] + wedCost[2]
        totalWed[marYrs[1]] = totalWed[marYrs[1]] + wedCost[0] + wedCost[1]
        
        self.totalWed = totalWed
        
    def vacExp(self,baseVac=3000,growthFactor=1,childFactor=0.35):    
        """baseVac = Annual Vacation Cost ($)"""
        
        totalVac = np.zeros((self.years,1))
        
        for n in range(self.years):
            totalVac[n] = baseVac + ((n / self.years) * (growthFactor * baseVac))
            
            for m in range(len(self.childYrs)):
                totalVac[n] = totalVac[n] + (totalVac[n] * childFactor)
        
        self.totalVac = totalVac
        
    def charExp(self,baseChar=0.025):
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
        self.miscExp()
        self.housingExp()
        self.carExp()
        self.collegeExp()
        self.wedExp()
        self.vacExp()
        self.charExp()
        self.randExp()

        totalExp = self.totalHol + self.totalEnt + self.totalMisc + \
                   self.totalHouse + self.totalAuto + \
                   self.totalCollege + self.totalWed + self.totalVac + \
                   self.totalChar + self.totalRand    
                   
        totalItem = self.totalChar
                    
        return [totalExp,totalItem]
    
def holidayExp(years,numChild,ageChild,addKid=None):
    numFamily = np.full((years,1),len(addKid))
    familyBday = np.zeros((years,1))
    familyXmas = np.zeros((years,1))
    
    removeKid = [x+20 for x in addKid]
    
    for n in range(years):
        for kid in addKid:
            if n == kid:
                numFamily[n:] = numFamily[n] + 1
        for kid in removeKid:
            if n == kid:
                numFamily[n:] = numFamily[n] - 1
        
        familyBday[n] = 50 * numFamily[n]
        familyXmas[n] = 50 * numFamily[n]
    
    childBday = np.zeros((years,len(numChild)))
    childXmas = np.zeros((years,len(numChild)))
    
    for n in range(years):
        for m in range(len(numChild)):
            if n >= numChild[m] and n <= (numChild[m] + 22):
                childBday[n,m] = 100 + ((ageChild[n,m] / 22) * 200)
                childXmas[n,m] = 300 + ((ageChild[n,m] / 22) * 1200)
    
    childBday = np.sum(childBday, axis=1).reshape((years,1))
    childXmas = np.sum(childXmas, axis=1).reshape((years,1))
    
    bday = 400
    xmas = 500
    valDay = 200
    anniv = 300
    
    totalHol = np.zeros((years,1))
    for n in range(years):
        totalHol[n] = bday + xmas + valDay + anniv + familyBday[n] + familyXmas[n] + childBday[n] + childXmas[n]
    
    return totalHol
    
def entExp(years,numChild):
    wifiCable = 75
    cellular = 80
    
    nflx = 120
    amzn = 130
    hulu = 100
    
    totalSub = np.zeros((years,1))
    for n in range(years):
        totalSub[n] = nflx + amzn + hulu
    
    totalEnt = np.zeros((years,1))
    for n in range(years):
        totalEnt[n] = (wifiCable + cellular) * 12 + totalSub[n]
    
        for m in range(len(numChild)):
            if n >= (numChild[m] + 8) and n <= (numChild[m] + 22):
                totalEnt[n] = totalEnt[n] + (totalEnt[n] * 0.25) 
    
    return totalEnt
    
def miscExp(years,numChild,growthFactor=0.5,childFactor=0.25):
    clothHair = 150
    grocery = 450
    restaurant = 200
    genMerch = 200
    
    miscSum = (clothHair + grocery + restaurant + genMerch) * 12
    
    totalMisc = np.zeros((years,1))
    for n in range(years):
        totalMisc[n] = miscSum + ((n / years) * (growthFactor * miscSum))
        
        for m in range(len(numChild)):
            if n >= numChild[m] and n <= (numChild[m] + 22):
                totalMisc[n] = totalMisc[n] + (totalMisc[n] * childFactor) 
    
    return totalMisc
    
def rentExp(salary,years,termStart,termEnd,basePerc=0.25,percDec=0.01,percSal=None):
    if percSal is None:
        rentPerc = [basePerc * (1-percDec) ** n for n in range(years)]
    else:
        rentPerc = percSal
    
    rentPay = np.zeros((years,1))
    
    for n in range(termStart,termEnd):
        rentPay[n] = rentPerc[n] * salary[n]
    
    return rentPay
    
def housingExp(years,rentPay,totalPay,houseWth,totalDwn):    
    repHouse = np.zeros((years,1))
    insHouse = np.zeros((years,1))
    utilElec = np.zeros((years,1))
    utilGas = np.zeros((years,1))
    utilWater = np.zeros((years,1))
    
    for n in range(years):
        repHouse[n] = min(houseWth[n] * 0.015,50000)
        insHouse[n] = houseWth[n] * 0.005
        utilElec[n] = (35 + ((35/500000) * houseWth[n])) * 12
        utilGas[n] = (20 + ((20/500000) * houseWth[n])) * 12
        utilWater[n] = (25 + ((25/1000000) * houseWth[n])) * 12
    
    totalHouse = repHouse + insHouse + utilElec + utilGas + utilWater + totalDwn + totalPay + rentPay
    
    return totalHouse  
    
def carExp(years,carYears,insRate=0.075,repRate=0.025):    
    carMonthly = np.zeros((np.shape(carYears)[0],2))
    carPayment = np.zeros((years,1))
    carDown = np.zeros((years,1))
    insCar = np.zeros((years,1))
    repCar = np.zeros((years,1))
    carInt = 0.019  # %
    carLen = 60     # months
    
    n = 0
    for car in carYears:
        carPrin = car[2] - car[3]
        carMonthly[n,0] = car[0]
        carMonthly[n,1] = ((carInt / 12) * carPrin) / (1 - (1 + (carInt / 12)) ** (-carLen))

        carDown[car[0]] = carDown[car[0]] + car[3]        
        
        n += 1
    
    for n in range(years):
        for car in carMonthly:
            if n == car[0]:
                carPayment[n:n+5] = carPayment[n:n+5] + (car[1] * 12)
        for car in carYears:
            if n >= car[0] and n < car[1]:
                insCar[n] = insCar[n] + (car[2] * insRate)
                repCar[n] = repCar[n] + (car[2] * repRate)    
    
    ezPass = 50 * 12
    
    milesDaily = 15000
    mpg = 35
    costFuel = 2.75
    gas = (milesDaily * costFuel) / mpg
    
    totalAuto = np.zeros((years,1))
    for n in range(years):
        totalAuto[n] = ezPass + gas + carPayment[n] + insCar[n] + repCar[n] + carDown[n]
    
    return totalAuto
    
def collegeExp(years,numChild,ageChild,baseCol=50000):
    totalCollege = np.zeros((years,1))
    
    for n in range(years):
        for m in range(len(numChild)):
            if ageChild[n,m] >= 18 and ageChild[n,m] <= 21:
                totalCollege[n] = totalCollege[n] + baseCol
    
    return totalCollege
    
def wedExp(years,marYr,wed,hm,ring):
    totalWed = np.zeros((years,1))
    
    totalWed[marYr-2] = totalWed[marYr] + ring
    totalWed[marYr] = totalWed[marYr] + wed + hm
    
    return totalWed
    
def vacExp(years,numChild,ageChild,baseVac=3000,growthFactor=1,childFactor=0.35):    
    totalVac = np.zeros((years,1))
    
    for n in range(years):
        totalVac[n] = baseVac + ((n / years) * (growthFactor * baseVac))
        
        for m in range(len(numChild)):
            if ageChild[n,m] >= 5:
                totalVac[n] = totalVac[n] + (totalVac[n] * childFactor)
    
    return totalVac
    
def charExp(salary,years,baseChar=0.025):
    totalChar = np.zeros((years,1))
    
    for n in range(years):
        totalChar[n] = salary[n] * baseChar
    
    return totalChar

def randExp(years,maxExp,decayFactor=3,binWid=5):
    totalRand = np.zeros((years,1))
    
    x = np.arange(maxExp)
#    y = math.e**(-x/(len(x)/decayFactor))
    expWid = maxExp * binWid / years
    
    for n in range(years):
        curBin = math.floor(n / binWid)
        
        while True:
            randFactor = rand.random()
            expense = -(len(x)/decayFactor) * math.log(randFactor,math.e)
            expBin = math.floor(expense / expWid)
            
            if expBin <= curBin:
                totalRand[n] = expense
                break
    
    return totalRand