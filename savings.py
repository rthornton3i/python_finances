import main
import salary as sal
import allocations as al
import withholdings as wh
import deductions as deds
import expenses as ex
import investments as inv

import importlib as il
import numpy as np
import matplotlib.pyplot as plt

loopLen = 1000
totalWorth, initWorth, contInv, contSav = [], [], [], []

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
    
    for n in range(main.years):
        # Contributions
        if n == 0:
            hiDiv[n] = al.savingsCont[n,0]
            ltLowVol[n] = al.savingsCont[n,1]
            largeCap[n] = al.savingsCont[n,2]
            stHiVol[n] = al.savingsCont[n,3]
            col529[n] = al.savingsCont[n,6]
            emergFunds[n] = al.savingsCont[n,7]
            medTerm[n] = al.savingsCont[n,8]
            shortTerm[n] = al.savingsCont[n,9]
            excSpend[n] = al.savingsCont[n,10]
            
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
        medTerm[n] = medTerm[n] - ex.totalHouse[n] - ex.totalAuto[n] - ex.downHomeExpense[n] - ex.downCarExpense[n] 
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
    
    cont = np.concatenate((hiDiv,ltLowVol,largeCap,stHiVol,retRoth401,retTrad401,col529,emergFunds,medTerm,shortTerm,excSpend),axis = 1)
    contInv.append(np.concatenate((hiDiv,ltLowVol,largeCap,stHiVol,retRoth401,retTrad401),axis = 1))
    contSav.append(np.concatenate((col529,emergFunds,medTerm,shortTerm,excSpend),axis = 1))
    
    tempTotalWorth = hiDiv + ltLowVol + largeCap + stHiVol + retRoth401 + retTrad401 + col529 + emergFunds + medTerm + shortTerm + excSpend 
    
    totalWorth.append(int(tempTotalWorth[-1]))
    initWorth.append(int(tempTotalWorth[0]))

totalInv = np.mean(contInv,axis=0)
totalSav = np.mean(contSav,axis=0)

#print((np.mean(initWorth)/2) - 4000)
#print(totalSav[1]/2)

plt.clf()
#plt.plot(medTerm)

#plt.hist(totalWorth)
print(np.mean(totalWorth))

#plt.subplot(211)
plt.plot(totalSav,linewidth=2)
plt.legend(('col529','emergFunds','medTerm','shortTerm','excSpend'))
#print(contSav)

#plt.subplot(212)
#plt.plot(totalInv,linewidth=2)
#plt.legend(('hiDiv','ltLowVol','largeCap','stHiVol','retRoth401','retTrad401'))