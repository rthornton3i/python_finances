import setup as stp
import loans as lns
import expenses as exp
import taxes as tax
import savings as sav

import numpy as np
import matplotlib.pyplot as plt

years = 40
childYrs = [7,9]
salaryBase = [77000,83000]

familyKids = [6,8,10,10,12,13,14]

#                    [Purchase Yr, Sell Yr, Amount ($), Down Payment ($)]
carYears = np.array([[0  , 8  , 23500 , 5000  ],   #Rich
                     [0  , 10 , 19500 , 4000  ],   #Becca
                     [8  , 16 , 25000 , 5000  ],   #Crossover1
                     [10 , 18 , 25000 , 7500  ],   #Sedan1
                     [16 , 26 , 30000 , 10000 ],   #Crossover2
                     [18 , 27 , 30000 , 12500 ],   #Sedan2
                     [23 , 27 , 22500 , 5000  ],   #Child1
                     [25 , 29 , 22500 , 5000  ],   #Child2
                     [26 , 33 , 40000 , 15000 ],   #Sedan3a
                     [27 , 35 , 40000 , 15000 ],   #Sedan3b
                     [33 , 40 , 45000 , 17500 ],   #Sedan4a
                     [35 , 40 , 45000 , 20000 ]])  #Sedan4b

baseSavings = np.asarray([[700],            #hiDiv      (VYM)
                          [700],            #ltLowVol   (VTI)
                          [700],            #largeCap   (MGK)
                          [5500],           #stHiVol    (Robinhood)
                          [3300 + 40000],   #retRoth401 (Fidelity, TBD)
                          [0],              #retTrad401 (Fidelity)
                          [400],            #col529     (Fidelity)
                          [1000],           #emergFunds (PNC Short)
                          [6500 + 35000],   #medTerm    (Goldman Sach's, BoA)
                          [1800 + 2000],    #shortTerm  (PNC Growth, BoA)
                          [1000]])          #excSpend   (PNC Spend)
                          

#                         [yr 0 , yr 10 , yr 20 , yr 30 , yr 40 ]
allocations = np.asarray([[2.5  , 2.5   , 5     , 12.5  , 5     ],     #hiDiv
                          [2.5  , 2.5   , 5     , 12.5  , 5     ],     #ltLowVol
                          [2.5  , 5     , 10    , 12.5  , 5     ],     #largeCap
                          [7.5  , 7.5   , 12.5  , 5     , 5     ],     #stHiVol
                          [0    , 0     , 0     , 0     , 0     ],     #retRoth401
                          [0    , 0     , 0     , 0     , 0     ],     #retTrad401
                          [0    , 2.5   , 12.5  , 0     , 0     ],     #col529
                          [5    , 2.5   , 5     , 5     , 15    ],     #emergFunds
                          [35   , 50    , 10    , 32.5  , 30    ],     #medTerm
                          [25   , 10    , 20    , 10    , 20    ],     #shortTerm
                          [20   , 17.5  , 20    , 10    , 15    ]])    #excSpend

#allocations = np.asarray([[2.5  , 0     , 2.5   , 12.5  , 5     ],     #hiDiv
#                          [2.5  , 0     , 2.5   , 12.5  , 5     ],     #ltLowVol
#                          [2.5  , 0     , 2.5   , 12.5  , 5     ],     #largeCap
#                          [7.5  , 2.5   , 5     , 5     , 5     ],     #stHiVol
#                          [0    , 0     , 0     , 0     , 0     ],     #retRoth401
#                          [0    , 0     , 0     , 0     , 0     ],     #retTrad401
#                          [0    , 2.5   , 12.5  , 0     , 0     ],     #col529
#                          [5    , 2.5   , 5     , 2.5   , 15    ],     #emergFunds
#                          [25   , 45    , 10    , 32.5  , 30    ],     #medTerm
#                          [30   , 27.5  , 35    , 10    , 20    ],     #shortTerm
#                          [25   , 20    , 25    , 12.5  , 15    ]])    #excSpend

#savingsCheck = np.sum(allocations,axis=0)
#print(savingsCheck)

###############################################################################
#plt.clf()

setup = stp.Setup(salaryBase,years,childYrs)
[salary,childAges] = setup.setupRun()

##Loans/Housing
#==============================================================================


loans = lns.Loans(years)

house = np.array([6,30,4.25,450000,20])
[houseBal,housePay,houseInt,houseWth,propTax,houseDwn] = loans.mortgageCalc(house)

house = np.array([18,30,4,900000,20])
[houseBal,housePay,houseInt,houseWth,propTax,houseDwn] = loans.mortgageCalc(house)

house = np.array([32,10,3.25,3500000,20])
[houseBal,housePay,houseInt,houseWth,propTax,houseDwn] = loans.mortgageCalc(house)

house = np.array([35,10,3.25,1500000,20])
[houseBal,housePay,houseInt,houseWth,propTax,houseDwn] = loans.mortgageCalc(house)

collegeLoan = np.array([0,8,4.0,36700])
[colLoanPay,colLoanBal,colLoanInt] = loans.genLoanCalc(collegeLoan)

#    
## Housing/Rent
##==============================================================================
#
#    if lawSchool is True:
#        rentPerc = np.vstack((np.full((lawYears[0],1),0.125),np.full((3,1),0.225),np.full((1,1),0.125)))
#        totalRent = exp.rentExp(salary,years,0,lawYears[1]+2,basePerc=0.15,percDec=0.01,percSal=rentPerc)
#        
#        house = np.array([lawYears[1]+2,30,4.25,400000,20])
#        [totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,curBal=None,curPay=None,curInt=None,curWth=None,curTax=None,curDwn=None,sellPrev=False,app=0.0375)
#        
#        house = np.array([22,30,4,750000,20])
#        [totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,curBal=totalBal,curPay=totalPay,curInt=totalInt,curWth=houseWth,curTax=propTax,curDwn=totalDwn,sellPrev=True,app=0.0375)
#    else:
#        totalRent = exp.rentExp(salary,years,0,6,basePerc=0.15,percDec=0.01,percSal=None)
#    
#        house = np.array([6,30,4.25,450000,20])
#        [totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,curBal=None,curPay=None,curInt=None,curWth=None,curTax=None,curDwn=None,sellPrev=False,app=0.0375)
#        
#        house = np.array([18,30,4,900000,20])
#        [totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,curBal=totalBal,curPay=totalPay,curInt=totalInt,curWth=houseWth,curTax=propTax,curDwn=totalDwn,sellPrev=True,app=0.0375)
#        
#        house = np.array([32,10,3.25,3500000,20])
#        [totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,curBal=totalBal,curPay=totalPay,curInt=totalInt,curWth=houseWth,curTax=propTax,curDwn=totalDwn,sellPrev=True,app=0.0375)
#        
#        house = np.array([35,10,3.25,1500000,20])
#        [totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,curBal=totalBal,curPay=totalPay,curInt=totalInt,curWth=houseWth,curTax=propTax,curDwn=totalDwn,sellPrev=False,app=0.0375)
#    
##    plt.clf()
##    plt.plot(totalRent/12)
#    
## Expenses
##==============================================================================
#                         
#    totalHol = exp.holidayExp(years,numChild,ageChild,addKid=familyKids)
#    totalEnt = exp.entExp(years,numChild)
#    totalMisc = exp.miscExp(years,numChild,growthFactor=0.5,childFactor=0.25)
#    
#    totalRand = exp.randExp(years,maxExp=25000,decayFactor=3,binWid=4)
#    totalVac = exp.vacExp(years,numChild,ageChild,baseVac=3000,growthFactor=1,childFactor=0.35)
#    totalChar = exp.charExp(salary,years,baseChar=0.005)
#    
#    totalHouse = exp.housingExp(years,totalRent,totalPay,houseWth,totalDwn)
#    totalAuto = exp.carExp(years,carYears,insRate=0.075,repRate=0.025)
#    
#    totalWed = exp.wedExp(years,marYr=4,wed=30000,hm=12500,ring=6000)
#    totalCollege = exp.collegeExp(years,numChild,ageChild,baseCol=50000)
#    totalLoan = colLoanPay
#    
#    if lawSchool is True:
#        totalVac[lawYears[0]:lawYears[1]+1] = totalVac[lawYears[0]:lawYears[1]+1] / 2
#        totalChar = exp.charExp(salary,years,baseChar=0.0025)
#        totalWed = exp.wedExp(years,marYr=4,wed=15000,hm=10000,ring=6000)
#        totalLoan = colLoanPay + lawLoanPay
#    
#    totalExpenses = np.hstack((totalHol,totalEnt,totalMisc,totalRand,totalVac,totalChar,totalHouse,totalAuto,totalWed,totalCollege,totalLoan))
#    
#    minExpPlot = np.hstack((totalHol,totalEnt,totalMisc))
#    minExpLabels = ['totalHol','totalEnt','totalMisc']
#    
#    medExpPlot = np.hstack((totalRand,totalVac,totalChar))
#    medExpLabels = ['totalRand','totalVac','totalChar']
#    
#    maxExpPlot = np.hstack((totalHouse,totalAuto,totalWed,totalCollege,totalLoan))
#    maxExpLabels = ['totalHouse','totalAuto','totalWed','totalCollege','totalLoan']
#    
##    plt.clf()
##    plt.plot(medExpPlot)
##    plt.legend(medExpLabels)
#    
##    plt.clf()
##    plt.plot(totalExpenses[:10,:])
#    
## Taxes/Deductions/Withholdings
##==============================================================================
#    
#    #Pretax Benefits
#    healthDed = tax.healthDedCalc(years,hsa=0,fsa=0,hra=0)  
#    [trad401,trad401Match] = tax.trad401Calc(salary,years,base401Perc=0,growth401Perc=0)
#       
#    #Deductions
#    [stdDedFed,stdDedState] = tax.stdDedCalc(salary,years)
#    [totalExState,totalExFed] = tax.exemptCalc(salary,years,numChild)
#    
#    [grossIncState,grossIncFed] = tax.grossIncCalc(salary,trad401,healthDed,totalExFed,totalExState)
#    
#    #SS & Medicare Taxes
#    miscTaxes = tax.miscTaxCalc(salary,years)
#    
#    #State Taxes
#    [itemDedFed,itemDedState] = tax.itemDedCalc(years,totalInt,totalChar)
#    stateLocalTax = tax.slTaxCalc(grossIncState,years,itemDedState,stdDedState)
#    
#    #Federal Taxes
#    slpTax = stateLocalTax + propTax
#    [itemDedFed,itemDedState] = tax.itemDedCalc(years,totalInt,totalChar,slpTax)
#    fedTax = tax.fedTaxCalc(grossIncFed,years,itemDedFed,stdDedFed)  
#    
#    #Posttax Benefits
#    [roth401,roth401Match] = tax.roth401Calc(salary,years,base401Perc=0.04,growth401Perc=0.01)
#    benefits = tax.benefitsCalc(years,healthPrem=200,visPrem=10,denPrem=20)
#    
#    [netIncome,netCash] = tax.netIncCalc(salary,fedTax,stateLocalTax,propTax,miscTaxes,roth401,trad401,benefits,healthDed)
#    effTaxRate = np.asarray([(salary[n] - netIncome[n]) / salary[n] for n in range(years)])
#    ret401 = np.hstack((roth401,roth401Match,trad401,trad401Match))
#    
##    plt.clf()
##    plt.subplot(121),plt.plot(salary),plt.plot(netIncome),plt.plot(netCash),plt.legend(('Gross Income','Net Income','Net Benefits'))
##    bt,tp = plt.ylim()
##    plt.ylim((0,tp))
##    plt.subplot(122),plt.plot(effTaxRate)
#    
##    plt.clf()
##    plt.plot(itemDedFed)
#    
## Savings/Investments
##==============================================================================
#    
#    [annualSavings,savings] = sav.savingsCalc(years,netCash,totalExpenses)
#    
#    savingsAlloc = sav.savingsAllocations(years,allocations)
#    earningsAlloc = sav.investAllocations(years,allocations)
#    
#    [savingsTotal,savingsCont] = sav.savingsContributions(years,savingsAlloc,earningsAlloc,netCash,totalExpenses,ret401,ageChild,baseSavings)
#    
##    hiDiv = savingsTotal[:,0]
##    ltLowVol = savingsTotal[:,1]
##    largeCap = savingsTotal[:,2]
##    stHiVol = savingsTotal[:,3]
##    
##    retRoth401 = savingsTotal[:,4]
##    retTrad401 = savingsTotal[:,5]
##    
##    col529 = savingsTotal[:,6]
##    emergFunds = savingsTotal[:,7]
##    medTerm = savingsTotal[:,8]
##    shortTerm = savingsTotal[:,9]
##    excSpend = savingsTotal[:,10]
##    
##    m = 20
##    n = 35
##    
##    plt.clf()
##    plt.plot(emergFunds[m:n])
##    plt.plot(medTerm[m:n])
##    plt.plot(shortTerm[m:n])
##    plt.plot(excSpend[m:n])
##    plt.legend(('emergFunds','medTerm','shortTerm','excSpend'))
##    
##    plt.clf()
##    plt.plot(col529)
##    
##    plt.clf()
##    plt.plot(savingsTotal)
##    plt.legend(('hiDiv','ltLowVol','largeCap','stHiVol','retRoth401','retTrad401','col529','emergFunds','medTerm','shortTerm','excSpend'))
#    
#    earningsAlloc_iter[:,:,x] = earningsAlloc[:,:]
#    savingsTotal_iter[:,:,x] = savingsTotal[:,:]
#    
#savingsTotal_iter = np.mean(savingsTotal_iter,axis=2)
#earningsAlloc_iter = np.mean(earningsAlloc_iter,axis=2)
#
#netWorth = np.sum(savingsTotal_iter,axis=1)
#
##0) hiDiv
##1) ltLowVol
##2) largeCap
##3) stHiVol
#
##4) retRoth401
##5) retTrad401
#
##6) col529
#
##7) emergFunds
##8) medTerm
##9) shortTerm
##10) excSpend
#
#m = 0
#n = 40
#x = 8
#
##plt.clf()
##plt.plot(savingsTotal_iter[m:n,x])
##plt.legend(('emerg','med','short','exc'))
#
#plt.clf()
#plt.plot(netWorth)
#
#print(netWorth[-1])