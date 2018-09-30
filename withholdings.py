import main
import taxes as tx

import numpy as np
import matplotlib.pyplot as plt

## Roth 401k & IRA
roth401Percent = np.full((main.years,1),0.04)
roth401MatchPercent = np.zeros((main.years,1))

for n in range(1,main.years):
    if n % 5 == 0:
        roth401Percent[n:main.years] = roth401Percent[n] + 0.01

#for n in range(main.years):
#    if roth401Percent:
        
roth401 = roth401Percent * tx.netIncome
#roth401Match = roth401MatchPercent * tx.netIncome

rothIRA = 0

## Benefits
# Medical
monthlyHealthPrem = 200
healthCont = np.zeros((main.years,1))

healthCont = monthlyHealthPrem * 12 * 2

# Vision
visPrem = 0
visCont = np.zeros((main.years,1))

visCont = visPrem * 12 * 2

# Dental
denPrem = 0
denCont = np.zeros((main.years,1))

denCont = denPrem * 12 * 2

## Total Posttax
totalWithheld = roth401 + rothIRA + healthCont + visCont + denCont