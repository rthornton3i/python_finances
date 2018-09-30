import main

import numpy as np
import matplotlib.pyplot as plt

# house# = [purchase year, mortgage period (yr), interest rate (%), purchase cost, down payment (%)
#       OPT{remortgage yr2, mortgage period2, interest rate2, NaN, NaN}
#       OPT{remortgage yr3, mortgage period3, interest rate3, NaN, NaN}]

house = np.array([[0  , 30 , 4.25 , 400000  , 10],
                  [10 , 20 , 4    , 800000  , 10],
                  [20 , 20 , 3.5  , 1500000 , 10],
                  [30 , 10 , 3.25 , 2750000 , 10]])

x = np.size(house,axis = 0)

## Property 
houseWorth = np.zeros((main.years,x))
houseProp = np.zeros((main.years,x))
app = 0.0375

for n in range(x):
    for m in range(main.years):
        if m >= house[n,0]:
            houseWorth[m,n] = house[n,3] * ((1 + app) ** (m - house[n,0]))
            houseProp[m,n] = 0.015 * houseWorth[m,n]

for n in range(x-1):
    for m in range(main.years):
        if m >= house[n+1,0]:
            houseWorth[m,n] = 0
            houseProp[m,n] = 0

houseWorthSum = np.sum(houseWorth, axis=1).reshape((main.years,1))
housePropSum = np.sum(houseProp, axis=1).reshape((main.years,1))

## Mortgage
mortPeriod = np.zeros((x,2))

housePay = np.zeros((main.years * 12,x))
houseBal = np.zeros((main.years * 12,x))
housePrin = np.zeros((main.years * 12,x))
houseInt = np.zeros((main.years * 12,x)) 
    
for n in range(x):
    startMort = int(house[n,0] * 12)
    endMort = int((house[n,0] + house[n,1]) * 12) - 1
    
    mortDown = (house[n,4]/100) * house[n,3]  
    
    rateInt = house[n,2] / (100 * 12)     #r - interest rate, monthly
    termLength = house[n,1] * 12          #n - number of months
    termCount = 0
    
    if n == 0:
        mortPrin = house[n,3] - mortDown
    else:
        mortPrin = house[n,3] - mortDown - houseWorth[int(house[n,0]),n-1]
        
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

houseBalSum = np.zeros((main.years,x))
housePrinSum =  np.zeros((main.years,x)) 
houseIntSum =  np.zeros((main.years,x)) 

for n in range(main.years):
    for m in range(x):
        houseBalSum[n,m] = houseBal[n*12,m]
    
    tempHousePrin = np.zeros((12,x))
    tempHousePrin = housePrin[n*12:(n*12)+11]
    housePrinSum[n] = np.sum(tempHousePrin,axis=0)
    
    tempHouseInt = np.zeros((12,x))
    tempHouseInt = houseInt[n*12:(n*12)+11]
    houseIntSum[n] = np.sum(tempHouseInt,axis=0)

housePrinSum = np.sum(housePrinSum,axis=1).reshape((main.years,1))
houseIntSum = np.sum(houseIntSum,axis=1).reshape((main.years,1))

houseBalSum = np.sum(houseBalSum,axis=1).reshape((main.years,1))
housePaySum = housePrinSum + houseIntSum + housePropSum

#plt.plot(houseBalSum)
#plt.plot(housePrinSum)
#plt.plot(houseIntSum)