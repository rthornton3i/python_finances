import main
import salary as sal

import numpy as np
import matplotlib.pyplot as plt

# house# = [purchase year, mortgage period (yr), interest rate (%), purchase cost, down payment (%)]

house = np.array([[7  , 30 , 4.25 , 450000  , 20 ],
                  [20 , 30 , 4    , 650000  , 20 ],
                  [32 , 10 , 3.25 , 5000000 , 20 ]])

numHouse = np.size(house,axis = 0)

## Rent
rentPay = np.zeros((main.years,1))

for n in range(int(house[0,0])):
    rentPay[n] = 0.175 * sal.salary[n]
    
rentPay[0] = 1700 * 12

## Property 
houseWorth = np.zeros((main.years,numHouse))
houseProp = np.zeros((main.years,numHouse))
app = 0.0375

for n in range(numHouse):
    for m in range(main.years):
        if m >= house[n,0]:
            houseWorth[m,n] = house[n,3] * ((1 + app) ** (m - house[n,0]))
            houseProp[m,n] = 0.015 * houseWorth[m,n]

for n in range(numHouse-1):
    for m in range(main.years):
        if m >= house[n+1,0]:
            houseWorth[m,n] = 0
            houseProp[m,n] = 0

houseWorthSum = np.sum(houseWorth, axis=1).reshape((main.years,1))
housePropSum = np.sum(houseProp, axis=1).reshape((main.years,1))

## Mortgage
mortPeriod = np.zeros((numHouse,2))

housePay = np.zeros((main.years * 12,numHouse))
houseBal = np.zeros((main.years * 12,numHouse))
housePrin = np.zeros((main.years * 12,numHouse))
houseInt = np.zeros((main.years * 12,numHouse)) 
    
for n in range(numHouse):
    startMort = int(house[n,0] * 12)
    endMort = int((house[n,0] + house[n,1]) * 12) - 1
    
    if endMort > (main.years * 12) - 1:
        endMort = (main.years * 12) - 1
    
    mortDown = (house[n,4]/100) * house[n,3]  
    
    rateInt = house[n,2] / (100 * 12)     #r - interest rate, monthly
    termLength = house[n,1] * 12          #n - number of months
    termCount = 0
    
    if n == 0:
        mortPrin = house[n,3] - mortDown
    else:
        mortPrin = house[n,3] - mortDown - houseWorthSum[int(house[n-1,0])]
        
        if mortPrin < 0:
            mortPrin = 0
    
    for m in range(startMort,endMort):
        termCount += 1 
        
        housePay[m,n] = mortPrin * (rateInt * (1 + rateInt) ** termLength) / ((1 + rateInt) ** termLength - 1)
        houseBal[m,n] = mortPrin * ((1 + rateInt) ** termLength - (1 + rateInt) ** termCount) / ((1 + rateInt) ** termLength - 1)
        
        if m > startMort:
            housePrin[m,n] = houseBal[m-1,n] - houseBal[m,n]                
        else:
            housePrin[m,n] = mortPrin - houseBal[m,n]
        
        houseInt[m,n] = housePay[m,n] - housePrin[m,n]

houseBalSum = np.zeros((main.years,numHouse))
housePrinSum =  np.zeros((main.years,numHouse)) 
houseIntSum =  np.zeros((main.years,numHouse)) 

for n in range(main.years):
    for m in range(numHouse):
        houseBalSum[n,m] = houseBal[n*12,m]
    
    tempHousePrin = np.zeros((12,numHouse))
    tempHousePrin = housePrin[n*12:(n*12)+11]
    housePrinSum[n] = np.sum(tempHousePrin,axis=0)
    
    tempHouseInt = np.zeros((12,numHouse))
    tempHouseInt = houseInt[n*12:(n*12)+11]
    houseIntSum[n] = np.sum(tempHouseInt,axis=0)

housePrinSum = np.sum(housePrinSum,axis=1).reshape((main.years,1))
houseIntSum = np.sum(houseIntSum,axis=1).reshape((main.years,1))

houseBalSum = np.sum(houseBalSum,axis=1).reshape((main.years,1))
housePaySum = housePrinSum + houseIntSum + housePropSum + rentPay

percMortSal = np.zeros((main.years,1))

for n in range(main.years):
    percMortSal[n] = housePaySum[n] / sal.salary[n]
    
#plt.clf()
#plt.plot(houseBalSum)
#plt.plot(housePaySum)
#plt.plot(housePrinSum)
#plt.plot(houseIntSum)

#plt.plot(houseWorthSum)
#plt.plot(housePropSum)

#plt.plot(percMortSal)