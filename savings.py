import numpy as np
import math
import random as rand
    
#      0        1        2         3         4        5         6          7         8         9    
#((totalHol,totalEnt,totalMisc,totalRand,totalVac,totalChar,totalHouse,totalAuto,totalWed,totalCollege)) 
    
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

def savingsAllocations(years,allocations):
    binWid = years / (np.shape(allocations)[1] - 1)
    accounts = np.shape(allocations)[0]
    savingsAlloc = np.zeros((years,accounts))
    
    for n in range(years):
        for m in range(accounts):
            if n == 0:
                savingsAlloc[n,m] = allocations[m][0]
            elif n > 0 and n < years:
                curBin = math.floor(n / binWid)
                savingsAlloc[n,m] = allocations[m][curBin] + (((n % binWid) / binWid) * (allocations[m][curBin+1] - allocations[m][curBin]))
            else:
                savingsAlloc[n,m] = allocations[m][-1]
    
    savingsAlloc = savingsAlloc / 100
            
    return savingsAlloc
    
def savingsContributions(years,savingsAlloc,earningsAlloc,netCash,totalExpenses,ageChild,baseSavings=None):
    accounts = np.shape(savingsAlloc)[1]
    savingsCont= np.zeros((years,accounts))
    savingsTotal = np.zeros((years,accounts))
    baseSavings = np.zeros((accounts,1)) if baseSavings is None else baseSavings
    
    for n in range(years):
        for m in range(accounts):
            savingsCont[n,m] = savingsAlloc[n,m] * netCash[n]
            
            if n == 0:
                savingsTotal[n,m] = savingsCont[n,m] + baseSavings[m]
            else:
                savingsTotal[n,m] = savingsTotal[n-1,m] + savingsCont[n,m]
                
            if m == 6:
                savingsTotal[n,m] = savingsTotal[n,m] - totalExpenses[n,9]
            elif m == 7:
                savingsTotal[n,m] = savingsTotal[n,m] - totalExpenses[n,3]
            elif m == 8:
                savingsTotal[n,m] = savingsTotal[n,m] - totalExpenses[n,6] - totalExpenses[n,8]
            elif m == 9:
                savingsTotal[n,m] = savingsTotal[n,m] - totalExpenses[n,4] - totalExpenses[n,5] - totalExpenses[n,7]
            elif m == 10:
                savingsTotal[n,m] = savingsTotal[n,m] - totalExpenses[n,0] - totalExpenses[n,1] - totalExpenses[n,2]    
            
            savingsTotal[n,m] = savingsTotal[n,m] * (1 + earningsAlloc[n,m])
    

        if n > 20 and ageChild[n,-1] == 0:
            transferVal = savingsTotal[n,6]
            savingsTotal[n,6] = 0
            
            savingsTotal[n,8] = savingsTotal[n,8] + transferVal
        
#        if n <= 35:
#            maxVal = 5e6
#            if stHiVol[n] > maxVal:
#                transferVal = stHiVol[n] - maxVal
#                
#                stHiVol[n] = maxVal
#                
#                largeCap[n] = largeCap[n] + transferVal
#            
#            maxVal = 5e6
#            if largeCap[n] > maxVal:
#                transferVal = largeCap[n] - maxVal
#                
#                largeCap[n] = maxVal
#                
#                ltLowVol[n] = ltLowVol[n] + transferVal
#        
#        maxVal = 2.5e6
#        if ltLowVol[n] > maxVal:
#            transferVal = ltLowVol[n] - maxVal
#            
#            ltLowVol[n] = maxVal
#            
#            hiDiv[n] = hiDiv[n] + transferVal
#        
#        maxVal = 2.5e6
#        if hiDiv[n] > maxVal:
#            transferVal = hiDiv[n] - maxVal
#            
#            hiDiv[n] = maxVal
#            
#            medTerm[n] = medTerm[n] + (transferVal * 0.7)
#            shortTerm[n] = shortTerm[n] + (transferVal * 0.1)
#            excSpend[n] = excSpend[n] + (transferVal * 0.1)
#            emergFunds[n] = excSpend[n] + (transferVal * 0.1)
    
    return [savingsTotal,savingsCont]

def investAllocations(years,allocations):
    accounts = np.shape(allocations)[0]
    earningsAlloc = np.zeros((years,accounts))
    
    for n in range(years):
        for m in range(accounts):
            if m == 0:
                earningsAlloc[n,m] = rand.normalvariate(4.0,0.5)
            elif m == 1:
                earningsAlloc[n,m] = rand.normalvariate(8.0,2.5)
            elif m == 2:
                earningsAlloc[n,m] = rand.normalvariate(12.0,4.5)
            elif m == 3:
                earningsAlloc[n,m] = rand.normalvariate(16.0,8.0)
                if earningsAlloc[n,m] > 30:
                    earningsAlloc[n,m] = 30
            elif m == 4 or m == 5:
                mu = np.zeros((years,1))
                sigma = np.zeros((years,1))
                
                muStart = 8.0
                muEnd = 4.0
                
                mu[n] = muStart - ((n / years) * (muStart - muEnd))
                sigma[n] = 0.25 * mu[n]
                
                earningsAlloc[n,m] = rand.normalvariate(mu[n],sigma[n])
            elif m == 6:
                mu = np.zeros((years,1))
                sigma = np.zeros((years,1))
                
                muStart = 7.0
                muEnd = 5.0
                
                mu[n] = muStart - ((n / years) * (muStart - muEnd))
                sigma[n] = 0.35 * mu[n]
                
                earningsAlloc[n,m] = rand.normalvariate(mu[n],sigma[n])
            elif m == 7:
                earningsAlloc[n,m] = 0.05
            elif m == 8:
                earningsAlloc[n,m] = 2.15
            elif m == 9:
                earningsAlloc[n,m] = 1.0
            elif m == 10:
                earningsAlloc[n,m] = 0.05
            
    earningsAlloc = earningsAlloc / 100
    
    return earningsAlloc

def savingsCalc(years,netCash,totalExpenses):
    totalExpenses = np.sum(totalExpenses,axis=1).reshape((years,1))
    savings = np.zeros((years,1))
    annualSavings = netCash - totalExpenses
    
    for n in range(years):
        if n == 0:
            savings[n] = annualSavings[n]
        else:
            savings[n] = savings[n-1] + annualSavings[n]
            
    return [annualSavings,savings]