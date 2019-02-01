import setup
import loans as ln
import expenses as exp
import taxes as tax

import numpy as np
import matplotlib.pyplot as plt

years = 40

startAge = 23
yearsRef = np.arange(startAge,startAge+years).reshape((years,1))
yrs = np.arange(years).reshape((years,1))

salaryBase = 77000 + 86000

# Number of Children
#==============================================================================
# [Yr @ Kid1 (+1), Yr @ Kid2 (+1),...]
# Children in year 7 and 9, ages 29 and 31
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
#  Loan = [Start Yr, End Yr, Interest Rate (%), Loan Amount]
#==============================================================================

collegeLoan = np.array([0,7,4.0,36700])
[colLoanPay,colLoanBal,colLoanInt] = ln.genLoanCalc(collegeLoan,years,compType='daily')

# Housing/Rent
#==============================================================================
#  Rent  = [Salary, Years, Start Yr, End Yr, Base Salary Percentage (%), Yearly Salary Percentage (%)]
#  House = [Purchase Yr, Mortgage Period (yrs), Interest Rate (%), Purchase Amount, Down Payment (%)]
#==============================================================================

rentPay = ln.rentCalc(salary,years,0,5,basePerc=0.25,percSal=None)

house = np.array([6,30,4.25,450000,20])
[totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,curBal=None,curPay=None,curInt=None,curWth=None,curTax=None,curDwn=None,app=0.0375)

house = np.array([18,20,4,900000,20])
[totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,totalBal,totalPay,totalInt,houseWth,propTax,totalDwn,app=0.0375)

house = np.array([30,10,3.25,2000000,20])
[totalBal,totalPay,totalInt,houseWth,propTax,totalDwn] = ln.mortgageCalc(house,years,totalBal,totalPay,totalInt,houseWth,propTax,totalDwn,app=0.0375)

plt.clf()
plt.plot(totalDown)

# Expenses
#==============================================================================

kids = [6,8,10,10,12,13,14]
totalHol = exp.holidayExp(years,numChild,ageChild,addKid=kids)

totalEnt = exp.entExp(years,numChild)

totalMisc = exp.miscExp(years,numChild)

totalCollege = exp.collegeExp(years,numChild,ageChild)

totalWed = exp.wedExp(years,4)

totalHouse = exp.housingExp(years,houseWth)

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

totalAuto = exp.carExp(years,carYears)



# Taxes/Deductions/Withholdings
#==============================================================================
#  Rent  = [Salary, Years, Start Yr, End Yr, Base Salary Percentage (%), Yearly Salary Percentage (%)]
#  House = [Purchase Yr, Mortgage Period (yrs), Interest Rate (%), Purchase Amount, Down Payment (%)]
#==============================================================================

#healthDed = tax.healthDedCalc(years,hsa=0,fsa=0,hra=0)  
#trad401 = tax.trad401Calc(salary,years,base401Perc=0,growth401Perc=0)
#    
#itemDed = tax.itemDedCalc(totalInt,charExpense,slpTaxes=0)
#[stdDedFed,stdDedState] = tax.stdDedCalc(salary,years)
#[totalExState,totalExFed] = tax.exemptCalc(salary,years,numChild)
#
#[grossIncState,grossIncFed] = tax.grossIncCalc(salary,trad401,healthDed,totalExFed,totalExState)
#
#miscTaxes = tax.miscTaxCalc(salary,years)
#stateLocalTax = tax.slTaxCalc(grossIncState,years,itemDed,stdDedState)
#fedTax = tax.fedTaxCalc(grossIncFed,years,itemDed,stdDedFed,stateLocalTax,propTax)  
#
#roth401 = tax.roth401Calc(salary,years,base401Perc=0.04,growth401Perc=0.01)
#benefits = tax.benefitsCalc(years,healthPrem=200,visPrem=10,denPrem=20)
#
#netIncome = tax.netIncCalc(salary,fedTax,stateLocalTax,propTax,miscTaxes,roth401,benefits)