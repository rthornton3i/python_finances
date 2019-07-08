from varsDict import var
from taxDict import rates

from setup import Setup
from loans import Loans
from expenses import Expenses
from taxes import Taxes
from savings import Savings

import numpy as np
import matplotlib.pyplot as plt

###############################################################################

loops = 10
totalSavings = []

for i in range(loops):
    ##General Setup
    #==============================================================================
    
    setup = Setup(var)
    setup.setupRun()
    
    var['salary']['salary'] = setup.salary
    var['children']['childAges'] = setup.childAges
    var['numInd'] = setup.numInd
    
    ##Loans/Housing
    #==============================================================================
    
    loans = Loans(var)
    
    [rentPay] = loans.rentCalc(basePerc=0.175)
    
    for n in range(len(var['housing']['house']['purYr'])):
        house = [var['housing']['house']['purYr'][n],
                 var['housing']['house']['term'][n],
                 var['housing']['house']['int'][n],
                 var['housing']['house']['prin'][n],
                 var['housing']['house']['down'][n]]
        
        [houseCosts] = loans.mortgageCalc(house)
    #    houseCosts  = [Bal,Pay,Int,Wth,Tax,Dwn]
        
    for n in range(len(var['cars']['purYr'])):
        car = [var['cars']['purYr'][n],
               var['cars']['sellYr'][n],
               var['cars']['amt'][n],
               var['cars']['down'][n]]
                 
        [carCosts] = loans.carCalc(car)
    #    carCosts  = [Pay,Wth,Dwn]
    
    [colLoanPay,colLoanBal,colLoanInt] = loans.genLoanCalc(var['loans']['collegeLoan'])
    #[lawLoanPay,lawLoanBal,lawLoanInt] = loans.genLoanCalc(var['lawLoan'])
    
    var['housing']['houseCosts'] = houseCosts
    var['cars']['carCosts'] = carCosts
    var['loans']['totalLoan'] = colLoanPay
    
    ##Expenses
    #==============================================================================
    
    exps = Expenses(var)
    [totalExp,totalItem] = exps.expRun()
    #         totalItem  = [totalChar]
    #         totalExp   = [totalHol,totalEnt,totalMisc,totalHouse,totalAuto,totalCollege,totalWed,totalVac,totalChar,totalRand,totalLoan]
    
    var['totalExp'] = totalExp
    var['totalItem'] = totalItem
    
    ##Taxes
    #==============================================================================
    
    taxes = Taxes(var,rates)
    [netIncome,netCash,netRet] = taxes.taxRun()
    
    var['netCash'] = netCash
    var['netRet'] = netRet
    
    ##Savings/Investments
    #==============================================================================
    
    savs = Savings(var)
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

#==============================================================================
print(np.sum(totalSavings[-1]))

plt.clf()
#plt.plot(excSpend[:10])
#plt.plot(emergFunds[:10])
#plt.plot(shortTerm[:10])
plt.plot(longTerm[:10])
#plt.plot(np.zeros((var['years'],1)))
plt.legend(('Excess','Emergency','Short','Long'))
#
#plt.clf()
#plt.plot(hiDiv)
#plt.plot(ltLowVol)
#plt.plot(largeCap)
#plt.plot(stHiVol)
#plt.legend(('High Div','LT Low Vol','Large Cap','ST High Vol'))
#
#plt.clf()
#plt.plot(retRoth401)
#plt.plot(retTrad401)
#
#print(np.sum(var['allocations'],axis=0))