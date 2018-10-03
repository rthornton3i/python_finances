import main
import mortgage as mort
import salary as sal
import children as ch

import numpy as np
import random as rand
import matplotlib.pyplot as plt

## Periodic Expenses
# Holidays
numFamily = np.full((main.years,1),7)
familyBday = np.zeros((main.years,1))
familyXmas = np.zeros((main.years,1))

addKid = [6,8,10,10,12,13,14]
removeKid = [x+20 for x in addKid]

for n in range(main.years):
    for kid in addKid:
        if n == kid:
            numFamily[n:] = numFamily[n] + 1
    for kid in removeKid:
        if n == kid:
            numFamily[n:] = numFamily[n] - 1
    
    familyBday[n] = 50 * numFamily[n]
    familyXmas[n] = 50 * numFamily[n]

childBday = np.zeros((main.years,len(main.numChild)))
childXmas = np.zeros((main.years,len(main.numChild)))

for n in range(main.years):
    for m in range(len(main.numChild)):
        if n >= main.numChild[m] and n <= (main.numChild[m] + 22):
            childBday[n,m] = 200
            childXmas[n,m] = 300

childBday = np.sum(childBday, axis=1).reshape((main.years,1))
childXmas = np.sum(childXmas, axis=1).reshape((main.years,1))

bday = 400
xmas = 400
valDay = 200
anniv = 300

totalHol = np.zeros((main.years,1))
for n in range(main.years):
    totalHol[n] = bday + xmas + valDay + anniv + familyBday[n] + familyXmas[n] + childBday[n] + childXmas[n]

# Subscriptions
nflx = 120
amzn = 130
hulu = 100

totalSub = np.zeros((main.years,1))
for n in range(main.years):
    totalSub[n] = nflx + amzn + hulu

# Housing
repHouse = np.zeros((main.years,1))
insHouse = np.zeros((main.years,1))
utilElec = np.zeros((main.years,1))
utilGas = np.zeros((main.years,1))
utilWater = np.zeros((main.years,1))

for n in range(main.years):
    repHouse[n] = min(mort.houseWorthSum[n] * 0.015,20000)
    insHouse[n] = mort.houseWorthSum[n] * 0.005
    utilElec[n] = (35 + ((35/500000) * mort.houseWorthSum[n])) * 12
    utilGas[n] = (20 + ((20/500000) * mort.houseWorthSum[n])) * 12
    utilWater[n] = (25 + ((25/1000000) * mort.houseWorthSum[n])) * 12

totalHouse = repHouse + insHouse + utilElec + utilGas + utilWater

# Auto
# carYears = [purchase Yr, sell Yr, amount ($), down payment ($)]
carYears = [[0  , 8  , 23500 , 5000  ],   #Rich
            [0  , 10 , 19500 , 4000  ],   #Becca
            [8  , 16 , 25000 , 5000  ],   #Crossover1
            [10 , 18 , 25000 , 7500  ],   #Sedan1
            [16 , 26 , 30000 , 10000 ],   #Crossover2
            [18 , 27 , 30000 , 12500 ],   #Sedan2
            [23 , 27 , 22500 , 5000  ],   #Child1
            [25 , 29 , 22500 , 5000  ],   #Child2
            [26 , 33 , 40000 , 15000 ],   #Sedan3a
            [27 , 35 , 40000 , 15000 ],   #Sedan3b
            [33 , 40 , 45000 , 17500 ],   #Sedan4a
            [35 , 40 , 45000 , 20000 ]]   #Sedan4b

carMonthly = np.zeros((len(carYears),2))
carPayment = np.zeros((main.years,1))
insCar = np.zeros((main.years,1))
repCar = np.zeros((main.years,1))
carInt = 0.019  # %
carLen = 60     # months

n = 0
for car in carYears:
    carPrin = car[2] - car[3]
    carMonthly[n,0] = car[0]
    carMonthly[n,1] = ((carInt / 12) * carPrin) / (1 - (1 + (carInt / 12)) ** (-carLen))
    n += 1

for n in range(main.years):
    for car in carMonthly:
        if n == car[0]:
            carPayment[n:n+5] = carPayment[n:n+5] + (car[1] * 12)
    for car in carYears:
        if n >= car[0] and n < car[1]:
            insCar[n] = insCar[n] + (car[2] * 0.075)
            repCar[n] = repCar[n] + (car[2] * 0.075)

ezPass = 50

milesDaily = 75
mpg = 25
costFuel = 2.75
gas = (milesDaily * costFuel * 30) / mpg

totalAuto = np.zeros((main.years,1))
for n in range(main.years):
    totalAuto[n] = ((ezPass + gas) * 12) + carPayment[n] + insCar[n] + repCar[n]

# Entertainment
wifiCable = 75
cellular = 80
otherEnt = 150

totalEnt = np.zeros((main.years,1))
for n in range(main.years):
    totalEnt[n] = (wifiCable + cellular + otherEnt) * 12

    for m in range(len(main.numChild)):
        if n >= main.numChild[m] and n <= (main.numChild[m] + 22):
            totalEnt[n] = totalEnt[n] + (totalEnt[n] * 0.25) 

# Miscellaneous
clothHair = 100
food = 450
otherMisc = 200

totalMisc = np.zeros((main.years,1))
for n in range(main.years):
    totalMisc[n] = (clothHair + food + otherMisc) * 12
    
    for m in range(len(main.numChild)):
        if n >= main.numChild[m] and n <= (main.numChild[m] + 22):
            totalMisc[n] = totalMisc[n] + (totalMisc[n] * 0.25) 

## Major Expenses
# College Expenses
colExpense = np.zeros((main.years,1))

for n in range(main.years):
    for m in range(len(main.numChild)):
        if ch.ageChild[n,m] >= 18 and ch.ageChild[n,m] < 22:
            colExpense[n] = colExpense[n] + 50000

# Wedding & Honeymoon
wedExpense = np.zeros((main.years,1))

wedExpense[4] = 30000
wedExpense[4] = 10000

# Home Down Payments
downHomeExpense = np.zeros((main.years,1))
houseDown = np.zeros((len(mort.house),2))

n = 0
for home in mort.house:
    houseDown[n,0] = home[0]
    houseDown[n,1] = home[3] * (home[4] / 100)
    n += 1

for n in range(main.years):
    for home in houseDown:
        if n == home[0]:
            downHomeExpense[n] = home[1]

# Auto Down Payments
downCarExpense = np.zeros((main.years,1))
carDown = np.zeros((len(carYears),2))

n = 0
for car in carYears:
    carDown[n,0] = car[0]
    carDown[n,1] = car[3]
    n += 1

for n in range(main.years):
    for car in carDown:
        if n == car[0]:
            downCarExpense[n] = downCarExpense[n] + car[1]
            
downCarExpense[0] = 0

# Vacation
vacExpense = np.zeros((main.years,1))

for n in range(main.years):
    vacExpense[n] = 4000 + ((n / main.years) * 3000)
    
    for m in range(len(main.numChild)):
        if ch.ageChild[n,m] >= 5:
            vacExpense[n] = vacExpense[n] + 1500

# Charitable Donations
charExpense = np.zeros((main.years,1))

for n in range(main.years):
    charExpense[n] = sal.salary[n] * 0.025

# Miscellaneous
miscCost = [[250   , 0.95  , 0  ],
            [500   , 0.8   , 0  ],
            [750   , 0.7   , 5  ],
            [1500  , 0.5   , 7  ],
            [3000  , 0.25  , 10 ],
            [5000  , 0.15  , 15 ],
            [10000 , 0.05  , 20 ],
            [20000 , 0.025 , 30 ]]

miscExpense = np.zeros((main.years,1))

for n in range(main.years):
    for m in miscCost:
        if n >= m[2] and rand.random() <= m[1]:
            miscExpense[n] = miscExpense[n] + m[0]

# TOTAL
totalPerExp = totalHol + totalSub + totalHouse + totalAuto + totalEnt + totalMisc + miscExpense + charExpense
totalMajorExp = colExpense + wedExpense + downHomeExpense + downCarExpense + vacExpense
totalExpenses = totalPerExp + totalMajorExp

#print(totalExpenses)
#plt.plot(totalExpenses)