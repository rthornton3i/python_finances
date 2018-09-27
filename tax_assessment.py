import main
import salary as sal

import numpy as np

## Miscellaneous Taxes
socialSecurity = .062
medicare = .0145
medicareAdditional = .009

maxTaxSS = 127200
minTaxAM = 250000

# Social Security
ssTax = np.zeros((main.years,1))

for n in range(main.years):
    if sal.salary[n] < maxTaxSS: 
        ssTax[n] = sal.salary[n] * socialSecurity 
    else:
        ssTax[n] = maxTaxSS * socialSecurity

# Medicare
mTax = np.zeros((main.years,1))

for n in range(main.years):  
    mTax[n] = sal.salary[n] * medicare

# Additional Medicare
amTax = np.zeros((main.years,1))

for n in range(main.years):
    if sal.salary[n] > minTaxAM:
        amTax[n] = sal.salary[n] * medicareAdditional 

miscTaxes = ssTax + mTax + amTax

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
totalEx = persStateEx + childStateEx


## State Taxes
stateTaxPercent = np.zeros((main.years,1))
stateTaxOwed = np.zeros((main.years,1))
bracketState = np.zeros((main.years,1))

bracketState1 = 1000
bracketState2 = 2000
bracketState3 = 3000
bracketState4 = 150000
bracketState5 = 175000
bracketState6 = 225000
bracketState7 = 300000

for n in range(main.years):
    if sal.salary[n] < bracketState1:
        stateTaxPercent[n] = 0.02
        stateTaxOwed[n] = 0
        bracketState[n] = 0
    elif sal.salary[n] < bracketState2:
        stateTaxPercent[n] = 0.03
        stateTaxOwed[n] = 20
        bracketState[n] = bracketState1
    elif sal.salary[n] < bracketState3:
        stateTaxPercent[n] = 0.04
        stateTaxOwed[n] = 50
        bracketState[n] = bracketState2
    elif sal.salary[n] < bracketState4:
        stateTaxPercent[n] = 0.0475
        stateTaxOwed[n] = 90
        bracketState[n] = bracketState3
    elif sal.salary[n] < bracketState5:
        stateTaxPercent[n] = 0.05
        stateTaxOwed[n] = 7072.5
        bracketState[n] = bracketState4
    elif sal.salary[n] < bracketState6:
        stateTaxPercent[n] = 0.0525
        stateTaxOwed[n] = 8322.5
        bracketState[n] = bracketState5
    elif sal.salary[n] < bracketState7:
        stateTaxPercent[n] = 0.055
        stateTaxOwed[n] = 10947.5
        bracketState[n] = bracketState6
    else:
        stateTaxPercent[n] = .0575
        stateTaxOwed[n] = 15072.5
        bracketState[n] = bracketState7

stateTaxes = np.zeros((main.years,1))

for n in range(main.years):              
    stateTaxes[n] = stateTaxOwed[n] + (stateTaxPercent[n] * (sal.salary[n] - bracketState[n]))

## Local Taxes
localTaxPercent = 0.025

## Property Taxes
propTax = 0.015

### Federal Taxes
## Deductions
# Standard
stdFedDed = np.full((main.years,1),24000)

for n in range(main.years):
    if slpDed[n] > 10000:
        slpDed[n] = 10000
        
#grossDedEarnings = sal.salary - totalDed
#
#fedTaxPercent = np.zeros((main.years,1))
#fedTaxOwed = np.zeros((main.years,1))
#bracketFed = np.zeros((main.years,1))
#
#if filing == 1:
#    bracketFed1 = 77400
#    bracketFed2 = 165000
#    bracketFed3 = 315000
#    bracketFed4 = 400000
#    bracketFed5 = 600000
#
#    for n in range(main.years):
#        if grossDedEarnings[n] < bracketFed1:
#            fedTaxPercent[n] = 0
#            fedTaxOwed[n] = 0
#            bracketFed[n] = 0
#        elif (grossDedEarnings[n] > bracketFed1) and (grossDedEarnings[n] < bracketFed2):
#            fedTaxPercent[n] = .22
#            fedTaxOwed[n] = 10452.5
#            bracketFed[n] = bracketFed1
#        elif (grossDedEarnings[n] > bracketFed2) and (grossDedEarnings[n] < bracketFed3):
#            fedTaxPercent[n] = .24
#            fedTaxOwed[n] = 29752.5
#            bracketFed[n] = bracketFed2
#        elif (grossDedEarnings[n] > bracketFed3) and (grossDedEarnings[n] < bracketFed4):
#            fedTaxPercent[n] = .32
#            fedTaxOwed[n] = 52222.5
#            bracketFed[n] = bracketFed3
#        elif (grossDedEarnings[n] > bracketFed4) and (grossDedEarnings[n] < bracketFed5):
#            fedTaxPercent[n] = .35
#            fedTaxOwed[n] = 112728
#            bracketFed[n] = bracketFed4
#        elif grossDedEarnings[n] > bracketFed5:
#            fedTaxPercent[n] = .37
#            fedTaxOwed[n] = 131628
#            bracketFed[n] = bracketFed5  
#    
#elif filing ==2:
#    bracketFed1 = 38700
#    bracketFed2 = 82500
#
#    for n in range(main.years):
#        if grossDedEarnings[n] < bracketFed1:
#            fedTaxPercent[n] = 0
#            fedTaxOwed[n] = 0
#            bracketFed[n] = 0
#        elif (grossDedEarnings[n] > bracketFed1) and (grossDedEarnings[n] < bracketFed2):
#            fedTaxPercent[n] = .22
#            fedTaxOwed[n] = 4453.5
#            bracketFed[n] = bracketFed1
#        elif grossDedEarnings[n] > bracketFed2:
#            fedTaxPercent[n] = .24
#            fedTaxOwed[n] = 14090
#            bracketFed[n] = bracketFed2
#
#fedTaxes = np.zeros((main.years,1))
#
#for n in range(main.years):
#    fedTaxes[n] = fedTaxOwed[n] + (fedTaxPercent[n] * (grossDedEarnings[n] - bracketFed[n]))
#    if fedTaxes[n] < 0:
#        fedTaxes[n] = 0