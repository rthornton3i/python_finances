import main
import salary as sal

import numpy as np

## Mortgages

# house# = [purchase year, mortgage period (yr), interest rate (#), purchase cost, down payment (#)
#       OPT{remortgage yr2, mortgage period2, interest rate2, NaN, NaN}
#       OPT{remortgage yr3, mortgage period3, interest rate3, NaN, NaN}]

house = np.array([[[0, 30, 4.25, 400000, 10],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]],

                  [[16, 20, 4, 750000, 10],
                   [22, 10, 3.25, 0, 0],
                   [0, 0, 0, 0, 0]],

                  [[27, 10, 3.25, 1250000, 10],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]]])
         
houseBal = np.zeros((main.years,1))
housePay = np.zeros((main.years,1))
housePrin = np.zeros((main.years,1))
houseInt = np.zeros((main.years,1))

x = np.size(house,axis = 0) 

print(x)

## House Payments
for n in range(x):
    if (isnan(house(3,1,n)) == 1) and (isnan(house(2,1,n)) == 1):
        if n == x:
            mortPeriod = [house(1,1,n), year]
        else:
            mortPeriod = [house(1,1,n), house(1,1,n + 1) - 1]     

        rateInt = house(1,3,n) / (100 * 12)    #r
        termLength = house(1,2,n) * 12         #n
        termToDate = house(1,1,n) - 1          #p

        if n == 1:
            mortDown = (house(1,5,n)/100) * house(1,4,n)
            mortPrin = house(1,4,n) - mortDown
        else:
            mortDown = (house(1,5,n)/100) * house(1,4,n)
            sellPrice = house(1,4,n - 1) * (1.0125 ** (house(1,1,n) - house (1,1,n - 1)))
            mortRemain = houseBal(house(1,1,n) - 1,1)
            mortPrin = house(1,4,n) - mortDown - sellPrice + mortRemain

            for m = mortPeriod(1,1):mortPeriod(1,2)
                houseBal(m) = (mortPrin * ((1 + rateInt) ** termLength - (1 + rateInt) ** ((m - termToDate) * 12)) / ((1 + rateInt) ** termLength - 1))
                housePay(m) = 12 * mortPrin * ((rateInt * (1 + rateInt) ** termLength) / (((1 + rateInt) ** termLength) - 1))
    elif isnan(house(3,1,n)) == 1:
        if n == x
            mortPeriod1 = [house(1,1,n), house(2,1,n) - 1]
            mortPeriod2 = [house(2,1,n), year]
        else
            mortPeriod1 = [house(1,1,n), house(2,1,n) - 1]
            mortPeriod2 = [house(2,1,n), house(1,1,n + 1) - 1]

        rateInt1 = house(1,3,n) / (100 * 12)    #r
        rateInt2 = house(2,3,n) / (100 * 12)
        termLength1 = house(1,2,n) * 12         #n
        termLength2 = house(2,2,n) * 12
        termToDate1 = house(1,1,n) - 1          #p
        termToDate2 = house(2,1,n) - 1

        if n == 1
            mortDown = (house(1,5,n)/100) * house(1,4,n)
            mortPrin1 = house(1,4,n) - mortDown
        else
            mortDown = (house(1,5,n)/100) * house(1,4,n)
            sellPrice = house(1,4,n - 1) * (1.0125 ** (house(1,1,n) - house (1,1,n - 1)))
            mortRemain = houseBal(house(1,1,n) - 1,1)
            mortPrin1 = house(1,4,n) - mortDown - sellPrice + mortRemain

            for m = mortPeriod1(1,1):mortPeriod1(1,2)
                houseBal(m) = (mortPrin1 * ((1 + rateInt1) ** termLength1 - (1 + rateInt1) ** ((m - termToDate1) * 12)) / ((1 + rateInt1) ** termLength1 - 1))
                housePay(m) = 12 * mortPrin1 * ((rateInt1 * (1 + rateInt1) ** termLength1) / (((1 + rateInt1) ** termLength1) - 1))

        mortPrin2 = houseBal(mortPeriod1(1,2))
        
            for m = mortPeriod2(1,1):mortPeriod2(1,2)
                houseBal(m) = (mortPrin2 * ((1 + rateInt2) ** termLength2 - (1 + rateInt2) ** ((m - termToDate2) * 12)) / ((1 + rateInt2) ** termLength2 - 1))
                housePay(m) = 12 * mortPrin2 * ((rateInt2 * (1 + rateInt2) ** termLength2) / (((1 + rateInt2) ** termLength2) - 1))
    else                                                        #3 mortgages
        if n == x
            mortPeriod1 = [house(1,1,n), house(2,1,n) - 1]
            mortPeriod2 = [house(2,1,n), house(3,1,n) - 1]
            mortPeriod3 = [house(3,1,n), year]
        else
            mortPeriod1 = [house(1,1,n), house(2,1,n) - 1]
            mortPeriod2 = [house(2,1,n), house(3,1,n) - 1]
            mortPeriod3 = [house(3,1,n), house(1,1,n + 1) - 1]

        rateInt1 = house(1,3,n) / (100 * 12)    #r
        rateInt2 = house(2,3,n) / (100 * 12)
        rateInt3 = house(3,3,n) / (100 * 12)
        termLength1 = house(1,2,n) * 12         #n
        termLength2 = house(2,2,n) * 12
        termLength3 = house(3,2,n) * 12
        termToDate1 = house(1,1,n) - 1          #p
        termToDate2 = house(2,1,n) - 1
        termToDate3 = house(3,1,n) - 1

        if n == 1
            mortDown = (house(1,5,n)/100) * house(1,4,n)
            mortPrin1 = house(1,4,n) - mortDown
        else
            mortDown = (house(1,5,n)/100) * house(1,4,n)
            sellPrice = house(1,4,n - 1) * (1.0125 ** (house(1,1,n) - house (1,1,n - 1)))
            mortRemain = houseBal(house(1,1,n) - 1,1)
            mortPrin1 = house(1,4,n) - mortDown - sellPrice + mortRemain

            for m = mortPeriod1(1,1):mortPeriod1(1,2)
                houseBal(m) = (mortPrin1 * ((1 + rateInt1) ** termLength1 - (1 + rateInt1) ** ((m - termToDate1) * 12)) / ((1 + rateInt1) ** termLength1 - 1))
                housePay(m) = 12 * mortPrin1 * ((rateInt1 * (1 + rateInt1) ** termLength1) / (((1 + rateInt1) ** termLength1) - 1))

        mortPrin2 = houseBal(mortPeriod1(1,2))

            for m = mortPeriod2(1,1):mortPeriod2(1,2)
                houseBal(m) = (mortPrin2 * ((1 + rateInt2) ** termLength2 - (1 + rateInt2) ** ((m - termToDate2) * 12)) / ((1 + rateInt2) ** termLength2 - 1))
                housePay(m) = 12 * mortPrin2 * ((rateInt2 * (1 + rateInt2) ** termLength2) / (((1 + rateInt2) ** termLength2) - 1))

        mortPrin3 = houseBal(mortPeriod2(1,2))

            for m = mortPeriod3(1,1):mortPeriod3(1,2)
                houseBal(m) = (mortPrin3 * ((1 + rateInt3) ** termLength3 - (1 + rateInt3) ** ((m - termToDate3) * 12)) / ((1 + rateInt3) ** termLength3 - 1))
                housePay(m) = 12 * mortPrin3 * ((rateInt3 * (1 + rateInt3) ** termLength3) / (((1 + rateInt3) ** termLength3) - 1))
#
### Balance and Payment
#for n in range(main.years):
#    if houseBal(n) < 0
#        houseBal(n) = 0
#
#for n = 2:year
#    if (houseBal(n - 1) == 0) and (houseBal(n) == 0)
#        housePay(n) = 0
#
### Principal & Interest
#for i = 1:x
#    for n = house(1,1,i)
#        if i == 1
#            mortDown = (house(1,5,i)/100) * house(1,4,i)
#            mortPrin = house(1,4,i) - mortDown
#        else
#            mortDown = (house(1,5,i)/100) * house(1,4,i)
#            sellPrice = house(1,4,i - 1) * (1.0125 ** (house(1,1,i) - house (1,1,i - 1)))
#            mortRemain = houseBal(house(1,1,i) - 1,1)
#            mortPrin = house(1,4,i) - mortDown - sellPrice + mortRemain
#            
#        housePrin(n) = mortPrin - houseBal(n)
#        houseInt(n) = housePay(n) - housePrin(n)
#
#for n = [house(1,1,1) + 1:house(1,1,2) - 1, house(1,1,2) + 1:house(1,1,3) - 1, house(1,1,3) + 1:year]
#    housePrin(n) = houseBal(n - 1) - houseBal(n)
#    houseInt(n) = housePay(n) - housePrin(n)
#
### Property 
#houseWorth = np.zeros((main.years,1))
#houseProp = np.zeros((main.years,1))
#
#for i = 1:x
#    if i == x
#        for n = house(1,1,i):year
#            houseWorth(n) = house(1,4,i) * (1.0125 ** (n - house(1,1,i)))
#            houseProp(n) = 0.02 * houseWorth(n)
#            
#    else
#        for n = house(1,1,i):house(1,1,i + 1) - 1
#            houseWorth(n) = house(1,4,i) * (1.0125 ** (n - house(1,1,i)))
#            houseProp(n) = 0.02 * houseWorth(n)
#
### TOTAL
#totalMortgage = aptRent + housePay + houseProp
#percMort = totalMortgage ./ netEarnings
