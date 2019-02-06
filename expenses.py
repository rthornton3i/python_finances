import numpy as np
import random as rand
import math

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
    if percSal == None:
        rentPerc = [basePerc * (1-percDec) ** n for n in range(years)]
    else:
        rentPerc = [percSal for n in range(years)]
    
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
    
def wedExp(years,marYr):
    totalWed = np.zeros((years,1))
    
    wedding = 20000
    honeymoon = 12500
    ring = 6000
    
    totalWed[marYr-2] = totalWed[marYr] + ring
    totalWed[marYr] = totalWed[marYr] + wedding + honeymoon
    
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