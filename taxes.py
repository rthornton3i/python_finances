import numpy as np

def pretaxCalc(housePropSum,houseIntSum):
    ## Itemized
    # Property Taxes
    propDed = housePropSum
    
    # Mortgage & Loan Interest
    loanDed = houseIntSum
     
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
    
    tradIRA = np.full((main.years,1),0)
    
    # HSA & FSA  
    hsaCont = np.full((main.years,1),0)  
    fsaCont = np.full((main.years,1),0)
    
    ### Federal Taxes
    ## Deductions
    # Standard
    stdFedDed = np.full((main.years,1),24000)
    
    # Itemized
    itemDed = loanDed + charDed + trad401 + tradIRA + hsaCont + fsaCont
    
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
    
    return

def taxCalc():
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
    
    ## State, Local, & Property Taxes
    localTaxPercent = 0.025
    stateTaxPercent = np.zeros((main.years,1))
    stateTaxOwed = np.zeros((main.years,1))
    bracketState = np.zeros((main.years,1))
    stateGrossIncome = np.zeros((main.years,1))
    
    for n in range(main.years):
        if deds.itemDed[n] > deds.stdStateDed[n]:
            stateGrossIncome[n] = sal.salary[n] - deds.totalStateEx[n] - deds.itemDed[n]
        else:
            stateGrossIncome[n] = sal.salary[n] - deds.totalStateEx[n] - deds.stdStateDed[n]
    
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
            stateTaxPercent[n] = 0.0575
            stateTaxOwed[n] = 15072.5
            bracketState[n] = bracketState7
    
    stateLocalTaxes = np.zeros((main.years,1))
    
    for n in range(main.years):              
        stateLocalTaxes[n] = stateTaxOwed[n] + ((stateTaxPercent[n] + localTaxPercent) * (stateGrossIncome[n] - bracketState[n]))
    
    propTaxes = deds.propDed
    
    ## Federal Taxes
    fedTaxPercent = np.zeros((main.years,1))
    fedTaxOwed = np.zeros((main.years,1))
    bracketFed = np.zeros((main.years,1))
    fedGrossIncome = np.zeros((main.years,1))
    
    slpDed = stateLocalTaxes + propTaxes
    
    for n in range(main.years):
        if slpDed[n] > 10000:
            slpDed[n] = 10000
            
    deds.itemDed = deds.itemDed + slpDed
    
    for n in range(main.years):
        if deds.itemDed[n] > deds.stdFedDed[n]:
            fedGrossIncome[n] = sal.salary[n] - deds.itemDed[n]
        else:
            fedGrossIncome[n] = sal.salary[n] - deds.stdFedDed[n]
    
    bracketFed1 = 19050
    bracketFed2 = 77400
    bracketFed3 = 165000
    bracketFed4 = 315000
    bracketFed5 = 400000
    bracketFed6 = 600000
    
    for n in range(main.years):
        if sal.salary[n] < bracketFed1:
            fedTaxPercent[n] = 0.1
            fedTaxOwed[n] = 0
            bracketFed[n] = 0
        elif sal.salary[n] < bracketFed2:
            fedTaxPercent[n] = 0.12
            fedTaxOwed[n] = 1905
            bracketFed[n] = bracketFed1
        elif sal.salary[n] < bracketFed3:
            fedTaxPercent[n] = 0.22
            fedTaxOwed[n] = 8907
            bracketFed[n] = bracketFed2
        elif sal.salary[n] < bracketFed4:
            fedTaxPercent[n] = 0.24
            fedTaxOwed[n] = 28179
            bracketFed[n] = bracketFed3
        elif sal.salary[n] < bracketFed5:
            fedTaxPercent[n] = 0.32
            fedTaxOwed[n] = 64179
            bracketFed[n] = bracketFed4
        elif sal.salary[n] < bracketFed6:
            fedTaxPercent[n] = 0.35
            fedTaxOwed[n] = 91379
            bracketFed[n] = bracketFed5
        else:
            fedTaxPercent[n] = 0.37
            fedTaxOwed[n] = 161379
            bracketFed[n] = bracketFed6
    
    fedTaxes = np.zeros((main.years,1))
    
    for n in range(main.years):              
        fedTaxes[n] = fedTaxOwed[n] + (fedTaxPercent[n] * (fedGrossIncome[n] - bracketFed[n]))
        
    totalTaxes = fedTaxes + stateLocalTaxes + propTaxes + miscTaxes
    
    netIncome = sal.salary - totalTaxes
    
    return

def posttaxCalc():
    ## Roth 401k & IRA
    roth401Percent = np.full((main.years,1),0.04)
    roth401MatchPercent = np.zeros((main.years,1))
    
    for n in range(1,main.years):
        if n % 5 == 0:
            roth401Percent[n:main.years] = roth401Percent[n] + 0.01
    
    for n in range(main.years):
        if roth401Percent[n] <= 0.04:
            roth401MatchPercent[n] = roth401Percent[n]
        elif roth401Percent[n] <= 0.1:
            roth401MatchPercent[n] = 0.04 + ((roth401Percent[n] - 0.04) * .5)
        else:
            roth401MatchPercent[n] = 0.07
            
    roth401 = roth401Percent * tx.netIncome
    roth401Match = roth401MatchPercent * tx.netIncome
    
    for n in range(main.years):
        if trad401[n] >= 18500:
            roth401[n] = 0
        elif trad401[n] + roth401[n] > 18500:
            roth401[n] = 18500 - trad401[n]
                
        if trad401Match[n] >= 18500:
            roth401Match[n] = 0
        elif trad401[n] + roth401Match[n] > 18500:
            roth401Match[n] = 18500 - trad401Match[n]
            
    rothIRA = np.full((main.years,1),0)
    
    ## Benefits
    # Medical
    monthlyHealthPrem = 200
    healthCont = np.zeros((main.years,1))
    
    healthCont = monthlyHealthPrem * 12 * 2
    
    # Vision
    visPrem = 10
    visCont = np.zeros((main.years,1))
    
    visCont = visPrem * 12 * 2
    
    # Dental
    denPrem = 20
    denCont = np.zeros((main.years,1))
    
    denCont = denPrem * 12 * 2
    
    ## Total Posttax
    totalWithheld = roth401 + rothIRA + healthCont + visCont + denCont
    
    return