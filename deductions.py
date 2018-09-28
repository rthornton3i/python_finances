import main
import salary as sal

import numpy as np

## Itemized
# Property Taxes
try:
    housePropFin
except NameError:
    houseProp = np.zeros((main.years,1))
    
    for n in range(main.years):
        houseProp[n] = (3 * sal.salary[n]) * 0.015

propDed = houseProp

# Mortgage & Loan Interest
try:
    houseIntFin
except NameError:
    houseInt = np.zeros((main.years,1))
    
    for n in range(main.years):
        houseInt[n] = 0.25 * houseProp[n]
    
loanDed = houseInt
 
# Charitable Donations
try:
    charExpenseFin
except NameError:
    charExpense = np.zeros((main.years,1))
    
    for n in range(main.years):
        charExpense[n] = 0.025 * sal.salary[n]
    
charDed = charExpense 

# Traditional 401k & IRA
trad401 = 0
tradIRA = 0
  
# HSA & FSA  
hsaCont = 0  
fsaCont = 0

itemDed = loanDed + charDed + trad401 + tradIRA + hsaCont + fsaCont

### Federal Taxes
## Deductions
# Standard
stdFedDed = np.full((main.years,1),24000)
        
### State Taxes
## Deductions
# Standard Deduction
stdStateDed = np.zeros((main.years,1))
for n in range(main.years):
    stdStateDed[n] = 0.15 * sal.salary[n]
    
    if stdStateDed[n] < 3000:
        stdStateDed[n] = 3000
    elif stdStateDed[n] > 4000:
        stdStateDed[n] = 4000

## Exemptions
# Personal Exemption
persStateEx = np.zeros((main.years,1))
for n in range(main.years):  
    if sal.salary[n] < 150000:
        persStateEx[n] = 3200 * 2
    elif sal.salary[n] < 175000:
        persStateEx[n] = 1600 * 2
    elif sal.salary[n] < 200000:
        persStateEx[n] = 800 * 2
    else:
        persStateEx[n] = 0
        
# Dependent Exemption
childStateEx = np.zeros((main.years,len(main.numChild)))

for n in range(main.years):
    for m in range(len(main.numChild)):
        if n >= main.numChild[m] and n <= (main.numChild[m] + 22):
            childStateEx[n,m] = 4050
            
childStateEx = childStateEx.sum(axis=1).reshape(main.years,1)            
totalStateEx = persStateEx + childStateEx

#### Total Pretax  
#totalDed = np.zeros((main.years,1))
#  
#for n in range(main.years):
#    if itemDed[n] > stdDed[n]:
#        totalDed[n] = itemDed[n]
#    else:
#        totalDed[n] = stdDed[n]  
#  
#totalDed = totalDed + trad401 + tradIRA + hsaCont + fsaCont
#
#for n in range(main.years):
#    if slpDed[n] > 10000:
#        slpDed[n] = 10000
        
#print(np.concatenate((totalDed,totalEx),axis=1))