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
totalConts = []
totalSavings = []
totalExpenses = []

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
    
    loans.rentCalc()
    
    for n in range(len(var['housing']['house']['purYr'])):
        house = [var['housing']['house']['purYr'][n],
                 var['housing']['house']['term'][n],
                 var['housing']['house']['int'][n],
                 var['housing']['house']['prin'][n],
                 var['housing']['house']['down'][n]]
        
        loans.mortgageCalc(house)
        
    for n in range(len(var['cars']['purYr'])):        
        car = [var['cars']['purYr'][n],
               var['cars']['sellYr'][n],
               var['cars']['amt'][n],
               var['cars']['down'][n]]
        
        if var['cars']['purYr'][n] == 0:
            loans.carCalc(car,term=50)
        else:
            loans.carCalc(car)
    
    [colLoan] = loans.genLoanCalc(var['loans']['collegeLoan'])
   #[lawLoan] = loans.genLoanCalc(var['loans']['lawLoan'])
    
    var['housing']['rentCosts'] = loans.rentCosts
    var['housing']['houseCosts'] = loans.houseCosts
    var['cars']['carCosts'] = loans.carCosts
    var['loans']['totalLoan'] = colLoan[1]
    
    ##Expenses
    #==============================================================================
    
    exps = Expenses(var)
    exps.expRun()
    
    var['totalExp'] = exps.totalExp
    var['totalItem'] = exps.totalItem
    
    ##Taxes
    #==============================================================================
    
    taxes = Taxes(var,rates)
    taxes.taxRun()
    
    var['netIncome'] = taxes.netIncome
    var['netCash'] = taxes.netCash
    var['netRet'] = taxes.netRet
    
    ##Savings/Investments
    #==============================================================================
    
    savs = Savings(var)
    savs.savRun()
    
    totalConts.append(savs.savCont)
    totalSavings.append(savs.savTotal)
    totalExpenses.append(exps.totalExp)
    
totalConts = np.mean(totalConts,axis=0)
totalSavings = np.mean(totalSavings,axis=0)
totalExpenses = np.mean(totalExpenses,axis=0)
    
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
print(np.sum(var['allocations'],axis=0))

earn = np.zeros((var['years'],1))
for n in range(var['years']):
    cont = np.sum(totalConts,axis=1)[n]
    exp = np.sum(totalExpenses,axis=0)[n][0]
    
    earn[n] = cont - exp    

yr = 0

print('Monthly contributions: ${:,.2f}'.format(np.sum(totalConts,axis=1)[yr]/12))
print('Monthly expenses: ${:,.2f}'.format(np.sum(totalExpenses,axis=0)[yr][0]/12))
print('')
print('Net worth: ${:,.0f}'.format(round(np.sum(totalSavings[-1])/1e5)*1e5))

#plt.clf()
#plt.plot(earn)
#plt.plot(np.zeros((var['years'],1)))

#===================================

n = 0
m = 40

plt.clf()
plt.plot(excSpend[n:m])
plt.plot(emergFunds[n:m])
plt.plot(shortTerm[n:m])
plt.plot(longTerm[n:m])
#plt.plot(np.sum((excSpend,emergFunds,shortTerm,longTerm),axis=0)[n:m])
plt.plot(np.zeros((m,1)))
plt.legend(('Excess','Emergency','Short','Long','Cash'))
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
