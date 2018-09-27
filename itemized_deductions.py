import main
import salary as sal

import numpy as np

# Property Taxes
propDed = np.zeros((main.years,1))

for n in range(main.years):
    propDed[n] = (3 * sal.salary[n]) * 0.015

# Mortgage & Loan Interest
try:
    houseIntFin
except NameError:
    houseInt = np.zeros((main.years,1))
    
    for n in range(main.years):
        houseInt[n] = 0.25 * houseProp[n]
    
loanDed = houseInt
 
## Charitable Donations
try:
    charExpenseFin
except NameError:
    charExpense = np.zeros((main.years,1))
    
    for n in range(main.years):
        charExpense[n] = 0.025 * sal.salary[n]
    
charDed = -charExpense 

itemDed = slpDed + loanDed + charDed

## Traditional 401k & IRA
trad401 = 0
tradIRA = 0
  
## HSA & FSA  
hsaCont = 0  
fsaCont = 0
  
## Total Pretax  
totalDed = np.zeros((main.years,1))
  
for n in range(main.years):
    if itemDed[n] > stdDed[n]:
        totalDed[n] = itemDed[n]
    else:
        totalDed[n] = stdDed[n]  
  
totalDed = totalDed + trad401 + tradIRA + hsaCont + fsaCont

#print(np.concatenate((totalDed,totalEx),axis=1))