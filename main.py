import setup
import loans as ln
import expenses as exp
import taxes as tax
import savings as sav

import numpy as np
import matplotlib.pyplot as plt

years = 40

startAge = 23
yearsRef = np.arange(startAge,startAge+years).reshape((years,1))
yrs = np.arange(years).reshape((years,1))

salaryBase = 77000 + 86000

# Number of Children
#==============================================================================
numChild = [6,8]

# Salary Growth  
#==============================================================================
#  1) Logistic
#  2) Linear 
#  3) Exponential Growth
#  4) Exponential CDF
#==============================================================================
growthType = 1

# Tax Filing
#==============================================================================
#  1) Married Filing Jointly
#  2) Single
#==============================================================================
filing = 1

salary = setup.salaryCalc(salaryBase,years,growthRate=0.028,growthType=1)
ageChild = setup.childCalc(years,numChild)

# Loans
#==============================================================================

collegeLoan = np.array([0,7,4.0,36700])
[colLoanPay,colLoanBal,colLoanInt] = ln.genLoanCalc(collegeLoan,years,compType='daily')

# Housing/Rent
#==============================================================================

house = np.array([8,30,4.25,450000,20])
[totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,curBal=None,curPay=None,curInt=None,curWth=None,curTax=None,curDwn=None,app=0.0375)

house = np.array([18,20,4,900000,20])
[totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,totalBal,totalPay,totalInt,houseWth,propTax,totalDwn,app=0.0375)

house = np.array([30,10,3.25,2000000,20])
[totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,totalBal,totalPay,totalInt,houseWth,propTax,totalDwn,app=0.0375)

#plt.clf()
#plt.plot(totalPay)

# Expenses
#==============================================================================

kids = [6,8,10,10,12,13,14]

# carYears = [purchase Yr, sell Yr, amount ($), down payment ($)]
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
                     
totalHol = exp.holidayExp(years,numChild,ageChild,addKid=kids)
totalEnt = exp.entExp(years,numChild)
totalMisc = exp.miscExp(years,numChild,growthFactor=0.5,childFactor=0.25)

totalRand = exp.randExp(years,maxExp=25000,decayFactor=3,binWid=4)
totalVac = exp.vacExp(years,numChild,ageChild,baseVac=3000,growthFactor=1,childFactor=0.35)
totalChar = exp.charExp(salary,years,baseChar=0.005)

totalRent = exp.rentExp(salary,years,0,8,basePerc=0.15,percDec=0.01,percSal=None)
totalHouse = exp.housingExp(years,totalRent,totalPay,houseWth,totalDwn)
totalAuto = exp.carExp(years,carYears,insRate=0.075,repRate=0.025)

totalWed = exp.wedExp(years,marYr=4)
totalCollege = exp.collegeExp(years,numChild,ageChild,baseCol=50000)

totalExpenses = np.hstack((totalHol,totalEnt,totalMisc,totalRand,totalVac,totalChar,totalHouse,totalAuto,totalWed,totalCollege))

minExpPlot = np.hstack((totalHol,totalEnt,totalMisc))
minExpLabels = ['totalHol','totalEnt','totalMisc']

medExpPlot = np.hstack((totalRand,totalVac,totalChar))
medExpLabels = ['totalRand','totalVac','totalChar']

maxExpPlot = np.hstack((totalHouse,totalAuto,totalWed,totalCollege))
maxExpLabels = ['totalHouse','totalAuto','totalWed','totalCollege']

#plt.clf()
#plt.plot(minExpPlot)
#plt.legend(minExpLabels)

#plt.clf()
#plt.plot(totalAuto)

# Taxes/Deductions/Withholdings
#==============================================================================

#Pretax Benefits
healthDed = tax.healthDedCalc(years,hsa=0,fsa=0,hra=0)  
trad401 = tax.trad401Calc(salary,years,base401Perc=0,growth401Perc=0)
   
#Deductions
[stdDedFed,stdDedState] = tax.stdDedCalc(salary,years)
[totalExState,totalExFed] = tax.exemptCalc(salary,years,numChild)

[grossIncState,grossIncFed] = tax.grossIncCalc(salary,trad401,healthDed,totalExFed,totalExState)

#SS & Medicare Taxes
miscTaxes = tax.miscTaxCalc(salary,years)

#State Taxes
[itemDedFed,itemDedState] = tax.itemDedCalc(years,totalInt,totalChar)
stateLocalTax = tax.slTaxCalc(grossIncState,years,itemDedState,stdDedState)

#Federal Taxes
slpTax = stateLocalTax + propTax
[itemDedFed,itemDedState] = tax.itemDedCalc(years,totalInt,totalChar,slpTax)
fedTax = tax.fedTaxCalc(grossIncFed,years,itemDedFed,stdDedFed)  

#Posttax Benefits
roth401 = tax.roth401Calc(salary,years,base401Perc=0.04,growth401Perc=0.01)
benefits = tax.benefitsCalc(years,healthPrem=200,visPrem=10,denPrem=20)

[netIncome,netCash] = tax.netIncCalc(salary,fedTax,stateLocalTax,propTax,miscTaxes,roth401,trad401,benefits,healthDed)
effTaxRate = np.asarray([(salary[n] - netIncome[n]) / salary[n] for n in range(years)])

#plt.clf()
#plt.subplot(121),plt.plot(salary),plt.plot(netIncome),plt.plot(netCash),plt.legend(('Gross Income','Net Income','Net Benefits'))
#bt,tp = plt.ylim()
#plt.ylim((0,tp))
#plt.subplot(122),plt.plot(effTaxRate)

#plt.clf()
#plt.plot(itemDedFed)

# Savings/Investments
#==============================================================================

baseSavings = np.asarray([[700],    #hiDiv      (VYM)
                          [700],    #ltLowVol   (VTI)
                          [700],    #largeCap   (MGK)
                          [5500],   #stHiVol    (Robinhood)
                          [3300],   #retRoth401 (Fidelity)
                          [0],      #retTrad401 (Fidelity)
                          [400],    #col529     (Fidelity)
                          [1000],   #emergFunds (PNC Short)
                          [6500],   #medTerm    (Goldman Sach's)
                          [1800],   #shortTerm  (PNC Growth)
                          [1000]])  #excSpend   (PNC Spend)
                          

#                         [yr 0 , yr 10 , yr 20 , yr 30 , yr 40 ]
allocations = np.asarray([[2.5  , 5     , 5     , 10    , 5     ],     #hiDiv
                          [2.5  , 7.5   , 7.5   , 12.5  , 5     ],     #ltLowVol
                          [2.5  , 7.5   , 7.5   , 12.5  , 5     ],     #largeCap
                          [7.5  , 12.5  , 7.5   , 5     , 5     ],     #stHiVol
                          [0    , 0     , 0     , 0     , 0     ],     #retRoth401
                          [0    , 0     , 0     , 0     , 0     ],     #retTrad401
                          [0    , 5     , 12.5  , 0     , 0     ],     #col529
                          [5    , 2.5   , 2.5   , 2.5   , 15    ],     #emergFunds
                          [35   , 27.5  , 35    , 32.5  , 30    ],     #medTerm
                          [25   , 22.5  , 12.5  , 15    , 20    ],     #shortTerm
                          [20   , 10    , 10    , 10    , 15    ]])    #excSpend

savingsCheck = np.sum(allocations,axis=0)
print(savingsCheck)

[annualSavings,savings] = sav.savingsCalc(years,netCash,totalExpenses)

savingsAlloc = sav.savingsAllocations(years,allocations)
earningsAlloc = sav.investAllocations(years,allocations)

[savingsTotal,savingsCont] = sav.savingsContributions(years,savingsAlloc,earningsAlloc,netCash,totalExpenses,ageChild,baseSavings)

hiDiv = savingsTotal[:,0]
ltLowVol = savingsTotal[:,1]
largeCap = savingsTotal[:,2]
stHiVol = savingsTotal[:,3]

retRoth401 = savingsTotal[:,4]
retTrad401 = savingsTotal[:,5]

col529 = savingsTotal[:,6]
emergFunds = savingsTotal[:,7]
medTerm = savingsTotal[:,8]
shortTerm = savingsTotal[:,9]
excSpend = savingsTotal[:,10]
            
plt.clf()
plt.plot(shortTerm[:10])
#plt.legend(('hiDiv','ltLowVol','largeCap','stHiVol','retRoth401','retTrad401','col529','emergFunds','medTerm','shortTerm','excSpend'))

#print(savingsTotal)