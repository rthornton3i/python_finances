import main
import salary as sal
import mortgage as mort

import numpy as np
import matplotlib.pyplot as plt

## Itemized
# Property Taxes
propDed = mort.housePropSum

# Mortgage & Loan Interest
loanDed = mort.houseIntSum
 
# Charitable Donations  
charDed = 0 

# Traditional 401k & IRA
trad401 = 0
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