import main
import salary as sal
import mortgage as mort
import expenses as ex

import numpy as np
import matplotlib.pyplot as plt

## Itemized
# Property Taxes
propDed = mort.housePropSum

# Mortgage & Loan Interest
loanDed = mort.houseIntSum
 
# Charitable Donations  
charDed = ex.charExpense 

# Traditional 401k & IRA
trad401Percent = np.full((main.years,1),0)
trad401MatchPercent = np.zeros((main.years,1))

for n in range(1,main.years):
    if n % 5 == 0:
        trad401Percent[n:main.years] = trad401Percent[n] + 0

for n in range(main.years):
    if trad401Percent[n] <= 0.04:
        trad401MatchPercent[n] = trad401Percent[n]
    elif trad401Percent[n] <= 0.1:
        trad401MatchPercent[n] = 0.04 + ((trad401Percent[n] - 0.04) * .5)
    else:
        trad401MatchPercent[n] = 0.07
        
trad401 = trad401Percent * sal.salary
trad401Match = trad401MatchPercent * sal.salary

for n in range(main.years):
    if trad401[n] > 18500:
        trad401[n] = 18500
    if trad401Match[n] > 18500:
        trad401Match[n] = 18500

tradIRA = 0

# HSA & FSA  
hsaCont = 0  
fsaCont = 0

### Federal Taxes
## Deductions
# Standard
stdFedDed = np.full((main.years,1),24000)

# Itemized
itemFedDed = propDed + loanDed + charDed + trad401 + tradIRA + hsaCont + fsaCont
        
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

# Itemized 
itemStateDed = loanDed + charDed + trad401 + tradIRA + hsaCont + fsaCont

## Exemptions
# Personal Exemption
persStateEx = np.zeros((main.years,1))
childStateEx = np.zeros((main.years,len(main.numChild)))

for n in range(main.years):  
    if sal.salary[n] < 150000:
        persStateEx[n] = 3200 * 2
        for m in range(len(main.numChild)):
            if n >= main.numChild[m] and n <= (main.numChild[m] + 22):
                childStateEx[n,m] = 3200
    elif sal.salary[n] < 175000:
        persStateEx[n] = 1600 * 2
        for m in range(len(main.numChild)):
            if n >= main.numChild[m] and n <= (main.numChild[m] + 22):
                childStateEx[n,m] = 1600
    elif sal.salary[n] < 200000:
        persStateEx[n] = 800 * 2
        for m in range(len(main.numChild)):
            if n >= main.numChild[m] and n <= (main.numChild[m] + 22):
                childStateEx[n,m] = 800
    else:
        persStateEx[n] = 0
        for m in range(len(main.numChild)):
            childStateEx[n,m] = 0
            
childStateEx = childStateEx.sum(axis=1).reshape(main.years,1)            
totalStateEx = persStateEx + childStateEx