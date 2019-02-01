import numpy as np
import random as rand

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
    
def housingExp(years,houseWth):    
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
    
    totalHouse = repHouse + insHouse + utilElec + utilGas + utilWater
    
    return totalHouse  

def homeDown(house,years):
    # Home Down Payments
    downHomeExpense = np.zeros((years,1))
    houseDown = np.zeros((len(house),2))
    
    n = 0
    for home in house:
        houseDown[n,0] = home[0]
        houseDown[n,1] = home[3] * (home[4] / 100)
        n += 1
    
    for n in range(years):
        for home in houseDown:
            if n == home[0]:
                downHomeExpense[n] = home[1]
                
    return

def carDown():
    # Auto Down Payments
    downCarExpense = np.zeros((years,1))
    carDown = np.zeros((len(carYears),2))
    
    n = 0
    for car in carYears:
        carDown[n,0] = car[0]
        carDown[n,1] = car[3]
        n += 1
    
    for n in range(years):
        for car in carDown:
            if n == car[0]:
                downCarExpense[n] = downCarExpense[n] + car[1]
                
    downCarExpense[0] = 0
    
    return
    
def carExp(years,carYears):    
    carMonthly = np.zeros((np.shape(carYears)[0],2))
    carPayment = np.zeros((years,1))
    insCar = np.zeros((years,1))
    repCar = np.zeros((years,1))
    carInt = 0.019  # %
    carLen = 60     # months
    
    n = 0
    for car in carYears:
        carPrin = car[2] - car[3]
        carMonthly[n,0] = car[0]
        carMonthly[n,1] = ((carInt / 12) * carPrin) / (1 - (1 + (carInt / 12)) ** (-carLen))
        n += 1
    
    for n in range(years):
        for car in carMonthly:
            if n == car[0]:
                carPayment[n:n+5] = carPayment[n:n+5] + (car[1] * 12)
        for car in carYears:
            if n >= car[0] and n < car[1]:
                insCar[n] = insCar[n] + (car[2] * 0.075)
                repCar[n] = repCar[n] + (car[2] * 0.075)
    
    ezPass = 50 * 12
    
    milesDaily = 15000 / 365
    mpg = 35
    costFuel = 2.75
    gas = (milesDaily * costFuel * 365) / mpg
    
    totalAuto = np.zeros((years,1))
    for n in range(years):
        totalAuto[n] = ezPass + gas + carPayment[n] + insCar[n] + repCar[n]
    
    return totalAuto

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
        totalEnt[n] = (wifiCable + cellular) * 12 + totalSub
    
        for m in range(len(numChild)):
            if n >= numChild[m] and n <= (numChild[m] + 22):
                totalEnt[n] = totalEnt[n] + (totalEnt[n] * 0.25) 
    
    return totalEnt
    
def miscExp(years,numChild):
    clothHair = 150
    grocery = 450
    restaurant = 400
    genMerch = 200
    
    totalMisc = np.zeros((years,1))
    for n in range(years):
        totalMisc[n] = (clothHair + grocery + restaurant + genMerch) * 12
        
        for m in range(len(numChild)):
            if n >= numChild[m] and n <= (numChild[m] + 22):
                totalMisc[n] = totalMisc[n] + (totalMisc[n] * 0.25) 
    
    return totalMisc
    
def collegeExp(years,numChild,ageChild):
    totalCollege = np.zeros((years,1))
    
    for n in range(years):
        for m in range(len(numChild)):
            if ageChild[n,m] >= 18 and ageChild[n,m] <= 21:
                totalCollege[n] = totalCollege[n] + 50000
    
    return totalCollege
    
def wedExp(years,marYr):
    totalWed = np.zeros((years,1))
    
    wedding = 30000
    honeymoon = 15000
    ring = 6000
    
    totalWed[marYr-2] = totalWed[marYr] + ring
    totalWed[marYr] = totalWed[marYr] + wedding + honeymoon
    
    return totalWed
    

    
    # Vacation
    vacExpense = np.zeros((years,1))
    
    for n in range(years):
        vacExpense[n] = 4000 + ((n / years) * 3000)
        
        for m in range(len(numChild)):
            if ageChild[n,m] >= 5:
                vacExpense[n] = vacExpense[n] + 1500
    
    # Charitable Donations
    charExpense = np.zeros((years,1))
    
    for n in range(years):
        charExpense[n] = salary[n] * 0.025
    
    # Miscellaneous
    miscCost = [[250   , 0.975 , 0  ],
                [500   , 0.9   , 0  ],
                [750   , 0.75  , 5  ],
                [1500  , 0.5   , 5  ],
                [3000  , 0.25  , 10 ],
                [5000  , 0.15  , 15 ],
                [10000 , 0.05  , 15 ],
                [20000 , 0.025 , 25 ]]
    
    miscExpense = np.zeros((years,1))
    
    for n in range(years):
        for m in miscCost:
            if n >= m[2] and rand.random() <= m[1]:
                miscExpense[n] = miscExpense[n] + m[0]
    
    # TOTAL
    totalPerExp = totalHol + totalSub + totalHouse + totalAuto + totalEnt + totalMisc + miscExpense + charExpense
    totalMajorExp = colExpense + loanPaySum + wedExpense + downHomeExpense + downCarExpense + vacExpense
    totalExpenses = totalPerExp + totalMajorExp
    
    return [totalExpenses,charExpense]