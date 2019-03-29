from varsDict import var
from taxDict import rates

import setup as stp
import loans as lns
import expenses as exp
import taxes as txs
import savings as sav

import numpy as np
import matplotlib.pyplot as plt

###############################################################################

loops = 10
totalSavings = []

for i in range(loops):
    ##General Setup
    #==============================================================================
    
    setup = stp.Setup(var)
    [salary,childAges,numInd] = setup.setupRun()
    
    var['salary'] = salary
    var['childAges'] = childAges
    var['numInd'] = numInd
    
    ##Loans/Housing
    #==============================================================================
    
    loans = lns.Loans(var)
    
    [rentPay] = loans.rentCalc(basePerc=0.175)
    
    for house in var['houses']:
        [houseCosts] = loans.mortgageCalc(house)
    #    houseCosts  = [Bal,Pay,Int,Wth,Tax,Dwn]
        
    for car in var['cars']:
        [carCosts] = loans.carCalc(car)
    #    carCosts  = [Pay,Wth,Dwn]
    
    [colLoanPay,colLoanBal,colLoanInt] = loans.genLoanCalc(var['collegeLoan'])
    #[lawLoanPay,lawLoanBal,lawLoanInt] = loans.genLoanCalc(var['lawLoan'])
    
    var['houseCosts'] = houseCosts
    var['carCosts'] = carCosts
    var['totalLoan'] = colLoanPay
    
    ##Expenses
    #==============================================================================
    
    exps = exp.Expenses(var)
    [totalExp,totalItem] = exps.expRun()
    #         totalItem  = [totalChar]
    #         totalExp   = [totalHol,totalEnt,totalMisc,totalHouse,totalAuto,totalCollege,totalWed,totalVac,totalChar,totalRand,totalLoan]
    
    var['totalExp'] = totalExp
    var['totalItem'] = totalItem
    
    ##Taxes
    #==============================================================================
    
    taxes = txs.Taxes(var,rates)
    [netIncome,netCash,netRet] = taxes.taxRun()
    
    var['netCash'] = netCash
    var['netRet'] = netRet
    
    ##Savings/Investments
    #==============================================================================
    
    savs = sav.Savings(var)
    [netWorth,savings] = savs.savRun()
    
    totalSavings.append(savings)
    
totalSavings = np.mean(totalSavings,axis=0)
    
hiDiv = totalSavings[:,0]
ltLowVol = totalSavings[:,1]
largeCap = totalSavings[:,2]
stHiVol = totalSavings[:,3]

retRoth401 = totalSavings[:,4]
retTrad401 = totalSavings[:,5]

col529 = totalSavings[:,6]
emergFunds = totalSavings[:,7]
longTerm = totalSavings[:,8]
shortTerm = totalSavings[:,9]
excSpend = totalSavings[:,10]

plt.clf()
plt.plot(excSpend)
plt.plot(emergFunds)
plt.plot(shortTerm)
plt.plot(longTerm)
plt.plot(np.zeros((var['years'],1)))
plt.legend(('Excess','Emergency','Short','Long'))

plt.clf()
plt.plot(hiDiv)
plt.plot(ltLowVol)
plt.plot(largeCap)
plt.plot(stHiVol)
plt.legend(('High Div','LT Low Vol','Large Cap','ST High Vol'))

plt.clf()
plt.plot(retRoth401)
plt.plot(retTrad401)

print(np.sum(var['allocations'],axis=0))