import main
import allocations as al
import expenses as ex
import withholdings as wh
import investments as inv

import numpy as np
import matplotlib.pyplot as plt

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
        retRoth401[n] = al.savingsCont[n,4]
        retTrad401[n] = al.savingsCont[n,5]
        col529[n] = al.savingsCont[n,6]
        emergFunds[n] = al.savingsCont[n,7]
        medTerm[n] = al.savingsCont[n,8]
        shortTerm[n] = al.savingsCont[n,9]
        excSpend[n] = al.savingsCont[n,10]
    else:
        hiDiv[n] = hiDiv[n-1] + al.savingsCont[n,0]
        ltLowVol[n] = ltLowVol[n-1] + al.savingsCont[n,1]
        largeCap[n] = largeCap[n-1] + al.savingsCont[n,2]
        stHiVol[n] = stHiVol[n-1] + al.savingsCont[n,3]
        retRoth401[n] = retRoth401[n-1] + al.savingsCont[n,4]
        retTrad401[n] = retTrad401[n-1] + al.savingsCont[n,5]
        col529[n] = col529[n-1] + al.savingsCont[n,6]
        emergFunds[n] = emergFunds[n-1] + al.savingsCont[n,7]
        medTerm[n] = medTerm[n-1] + al.savingsCont[n,8]
        shortTerm[n] = shortTerm[n-1] + al.savingsCont[n,9]
        excSpend[n] = excSpend[n-1] + al.savingsCont[n,10]

    # Witholdings
    retRoth401[n] = retRoth401[n] + wh.roth401[n] + wh.roth401Match[n]
    
    # Earnings
    

    # Expenses
    col529[n] = col529[n] - ex.colExpense[n]
    emergFunds[n] = emergFunds[n] - ex.miscExpense[n]
    medTerm[n] = medTerm[n] - ex.totalHouse[n] - ex.totalAuto[n] - ex.downHomeExpense[n] - ex.downCarExpense[n] 
    shortTerm[n] = shortTerm[n] - ex.totalHol[n] - ex.totalSub[n] - ex.totalEnt[n] - ex.totalMisc[n]
    excSpend[n] = excSpend[n] - ex.wedExpense[n] - ex.vacExpense[n] - ex.charExpense[n]

#contributions = np.concatenate((hiDiv,ltLowVol,largeCap,stHiVol,retRoth401,retTrad401,col529,emergFunds,medTerm,shortTerm,excSpend),axis = 1)
#contributions = np.concatenate((hiDiv,ltLowVol,largeCap,stHiVol,retRoth401,retTrad401),axis = 1)
contributions = np.concatenate((emergFunds,medTerm,shortTerm,excSpend),axis = 1)
totalCont = hiDiv + ltLowVol + largeCap + stHiVol + retRoth401 + retTrad401 + col529 + emergFunds + medTerm + shortTerm + excSpend

plt.plot(contributions)