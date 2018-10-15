import main
import salary as sal
import children as ch
import allocations as al
import withholdings as wh
import deductions as deds
import expenses as ex
import investments as inv

import importlib as il
import numpy as np
import matplotlib.pyplot as plt

loopLen = 100
tempTotalWorth, tempNetWorth, contInv, contSav = [], [], [], []

for i in range(loopLen):
    il.reload(sal)
    il.reload(ex)
    il.reload(inv)
    
    hiDiv = np.zeros((main.years,1))
    ltLowVol = np.zeros((main.years,1))
    largeCap = np.zeros((main.years,1))
    stHiVol = np.zeros((main.years,1))
    retRoth401 = np.zeros((main.years,1))
    retTrad401 = np.zeros((main.years,1))
    col529 = np.zeros((main.years,1))
    emergFunds = np.zeros((main.years,1))
    medTerm = np.zeros((main.years,1))
    shortTerm = np.zeros((main.years,1))
    excSpend = np.zeros((main.years,1))
    
    hiDiv[0] = 0
    ltLowVol[0] = 0
    largeCap[0] = 0
    stHiVol[0] = 4000
    retRoth401[0] = 0
    retTrad401[0] = 0
    col529[0] = 0
    emergFunds[0] = 0
    medTerm[0] = 4000 + 27000 + 15000
    shortTerm[0] = 0
    excSpend[0] = 0
    
    for n in range(main.years):
        # Contributions
        if n == 0:
            hiDiv[n] = hiDiv[n] + al.savingsCont[n,0]
            ltLowVol[n] = ltLowVol[n] + al.savingsCont[n,1]
            largeCap[n] = largeCap[n] + al.savingsCont[n,2]
            stHiVol[n] = stHiVol[n] + al.savingsCont[n,3]
            col529[n] = col529[n] + al.savingsCont[n,6]
            emergFunds[n] = emergFunds[n] + al.savingsCont[n,7]
            medTerm[n] = medTerm[n] + al.savingsCont[n,8]
            shortTerm[n] = shortTerm[n] + al.savingsCont[n,9]
            excSpend[n] = excSpend[n] + al.savingsCont[n,10]
            
            retRoth401[n] = wh.roth401[n] + wh.roth401Match[n]
            retTrad401[n] = deds.trad401[n] + deds.trad401Match[n]
        else:
            hiDiv[n] = hiDiv[n-1] + al.savingsCont[n,0]
            ltLowVol[n] = ltLowVol[n-1] + al.savingsCont[n,1]
            largeCap[n] = largeCap[n-1] + al.savingsCont[n,2]
            stHiVol[n] = stHiVol[n-1] + al.savingsCont[n,3]
            col529[n] = col529[n-1] + al.savingsCont[n,6]
            emergFunds[n] = emergFunds[n-1] + al.savingsCont[n,7]
            medTerm[n] = medTerm[n-1] + al.savingsCont[n,8]
            shortTerm[n] = shortTerm[n-1] + al.savingsCont[n,9]
            excSpend[n] = excSpend[n-1] + al.savingsCont[n,10]
            
            retRoth401[n] = retRoth401[n-1] + wh.roth401[n] + wh.roth401Match[n]
            retTrad401[n] = retTrad401[n-1] + deds.trad401[n] + deds.trad401Match[n]
    
        # Expenses
        col529[n] = col529[n] - ex.colExpense[n]
        emergFunds[n] = emergFunds[n] - ex.miscExpense[n]
        medTerm[n] = medTerm[n] - ex.totalHouse[n] - ex.totalAuto[n] - ex.downHomeExpense[n] - ex.downCarExpense[n] - ex.loanExpense[n]
        shortTerm[n] = shortTerm[n] - ex.totalHol[n] - ex.totalSub[n] - ex.totalEnt[n] - ex.totalMisc[n]
        excSpend[n] = excSpend[n] - ex.wedExpense[n] - ex.vacExpense[n] - ex.charExpense[n]
        
        # Earnings
        hiDiv[n] = (1 + inv.meanEarningsAlloc[n,0]) * hiDiv[n]
        ltLowVol[n] = (1 + inv.meanEarningsAlloc[n,1]) * ltLowVol[n]
        largeCap[n] = (1 + inv.meanEarningsAlloc[n,2]) * largeCap[n]
        stHiVol[n] = (1 + inv.meanEarningsAlloc[n,3]) * stHiVol[n]
        retRoth401[n] = (1 + inv.meanEarningsAlloc[n,4]) * retRoth401[n]
        retTrad401[n] = (1 + inv.meanEarningsAlloc[n,5]) * retTrad401[n]
        col529[n] = (1 + inv.meanEarningsAlloc[n,6]) * col529[n]
        emergFunds[n] = (1 + inv.meanEarningsAlloc[n,7]) * emergFunds[n]
        medTerm[n] = (1 + inv.meanEarningsAlloc[n,8]) * medTerm[n]
        shortTerm[n] = (1 + inv.meanEarningsAlloc[n,9]) * shortTerm[n]
        excSpend[n] = (1 + inv.meanEarningsAlloc[n,10]) * excSpend[n]
        
        # Transfers
        if n > 20 and ch.ageChild[n,-1] == 0:
            transferVal = col529[n]
            
            col529[n] = 0
            
            medTerm[n] = medTerm[n] + transferVal
        
        maxVal = 5e6
        if stHiVol[n] > maxVal:
            transferVal = stHiVol[n] - maxVal
            
            stHiVol[n] = maxVal
            
            largeCap[n] = largeCap[n] + transferVal
        
        maxVal = 5e6
        if largeCap[n] > maxVal:
            transferVal = largeCap[n] - maxVal
            
            largeCap[n] = maxVal
            
            ltLowVol[n] = ltLowVol[n] + transferVal
        
        maxVal = 2.5e6
        if ltLowVol[n] > maxVal:
            transferVal = ltLowVol[n] - maxVal
            
            ltLowVol[n] = maxVal
            
            hiDiv[n] = hiDiv[n] + transferVal
        
        maxVal = 2.5e6
        if hiDiv[n] > maxVal:
            transferVal = hiDiv[n] - maxVal
            
            hiDiv[n] = maxVal
            
            medTerm[n] = medTerm[n] + (transferVal * 0.6)
            shortTerm[n] = shortTerm[n] + (transferVal * 0.3)
            excSpend[n] = excSpend[n] + (transferVal * 0.1)
            
    cont = np.concatenate((hiDiv,ltLowVol,largeCap,stHiVol,retRoth401,retTrad401,col529,emergFunds,medTerm,shortTerm,excSpend),axis = 1)
    contInv.append(np.concatenate((hiDiv,ltLowVol,largeCap,stHiVol,retRoth401,retTrad401),axis = 1))
    contSav.append(np.concatenate((col529,emergFunds,medTerm,shortTerm,excSpend),axis = 1))
    
    totalWorthSum = hiDiv + ltLowVol + largeCap + stHiVol + retRoth401 + retTrad401 + col529 + emergFunds + medTerm + shortTerm + excSpend 
    tempTotalWorth.append(list(map(int,totalWorthSum)))

totalInv = np.mean(contInv,axis=0)
totalSav = np.mean(contSav,axis=0)
totalCont = np.mean(cont,axis=0)

for worth in tempTotalWorth:
    tempNetWorth.append(worth[-1])
    
netWorth = np.mean(tempNetWorth)
#netWorth = np.median(tempNetWorth)
totalWorth = np.mean(tempTotalWorth,axis=0)

#print(totalSav[0]/2)
print(netWorth)

plt.clf()

#plt.hist(tempNetWorth,30)

#plt.subplot(211)
plt.plot(totalSav,linewidth=2)
plt.legend(('col529','emergFunds','medTerm','shortTerm','excSpend'))
#plt.yscale('log', basey=10)

#plt.subplot(212)
#plt.plot(totalInv,linewidth=2)
#plt.legend(('hiDiv','ltLowVol','largeCap','stHiVol','retRoth401','retTrad401'))
#plt.yscale('log', basey=10)