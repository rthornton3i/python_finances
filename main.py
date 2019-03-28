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
    
var['houseCosts'] = houseCosts
var['carCosts'] = carCosts

[colLoanPay,colLoanBal,colLoanInt] = loans.genLoanCalc(var['collegeLoan'])
#[lawLoanPay,lawLoanBal,lawLoanInt] = loans.genLoanCalc(var['lawLoan'])

##Expenses
#==============================================================================

exps = exp.Expenses(var)
[totalExp,totalItem] = exps.expRun()
#         totalItem  = [totalChar]

var['totalExp'] = totalExp
var['totalItem'] = totalItem

##Taxes
#==============================================================================

taxes = txs.Taxes(var,rates)
[netIncome,netCash] = taxes.taxRun()

##Savings/Investments
#==============================================================================

savs = sav.Savings(var)
savs.savRun()

[annualSavings,savings] = sav.savingsCalc(years,netCash,totalExpenses)

savingsAlloc = sav.savingsAllocations(years,allocations)
earningsAlloc = sav.investAllocations(years,allocations)

[savingsTotal,savingsCont] = sav.savingsContributions(years,savingsAlloc,earningsAlloc,netCash,totalExpenses,ret401,ageChild,baseSavings)

#    hiDiv = savingsTotal[:,0]
#    ltLowVol = savingsTotal[:,1]
#    largeCap = savingsTotal[:,2]
#    stHiVol = savingsTotal[:,3]
#    
#    retRoth401 = savingsTotal[:,4]
#    retTrad401 = savingsTotal[:,5]
#    
#    col529 = savingsTotal[:,6]
#    emergFunds = savingsTotal[:,7]
#    medTerm = savingsTotal[:,8]
#    shortTerm = savingsTotal[:,9]
#    excSpend = savingsTotal[:,10]
#    
#    m = 20
#    n = 35
#    
#    plt.clf()
#    plt.plot(emergFunds[m:n])
#    plt.plot(medTerm[m:n])
#    plt.plot(shortTerm[m:n])
#    plt.plot(excSpend[m:n])
#    plt.legend(('emergFunds','medTerm','shortTerm','excSpend'))
#    
#    plt.clf()
#    plt.plot(col529)
#    
#    plt.clf()
#    plt.plot(savingsTotal)
#    plt.legend(('hiDiv','ltLowVol','largeCap','stHiVol','retRoth401','retTrad401','col529','emergFunds','medTerm','shortTerm','excSpend'))

earningsAlloc_iter[:,:,x] = earningsAlloc[:,:]
savingsTotal_iter[:,:,x] = savingsTotal[:,:]
    
savingsTotal_iter = np.mean(savingsTotal_iter,axis=2)
earningsAlloc_iter = np.mean(earningsAlloc_iter,axis=2)

netWorth = np.sum(savingsTotal_iter,axis=1)

#0) hiDiv
#1) ltLowVol
#2) largeCap
#3) stHiVol

#4) retRoth401
#5) retTrad401

#6) col529

#7) emergFunds
#8) medTerm
#9) shortTerm
#10) excSpend

m = 0
n = 40
x = 8

#plt.clf()
#plt.plot(savingsTotal_iter[m:n,x])
#plt.legend(('emerg','med','short','exc'))

plt.clf()
plt.plot(netWorth)

print(netWorth[-1])