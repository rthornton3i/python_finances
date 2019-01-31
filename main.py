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
#  House = [Purchase Yr, Mortgage Period (yrs), Interest Rate (%), Purchase Amount, Down Payment (%)]
#==============================================================================
rentPay = ln.rentCalc(salary,years,0,30,basePerc=0.25,percSal=None)

house1 = np.array([6  , 30 , 4.25 , 450000  , 20 ])
house2 = np.array([20 , 30 , 4    , 700000  , 20 ])
house3 = np.array([33 , 10 , 3.25 , 7500000 , 20 ])





#healthDed = tax.healthDedCalc(years,hsa=0,fsa=0,hra=0)  
#trad401 = tax.trad401Calc(salary,years,base401Perc=0,growth401Perc=0)
#    
#itemDed = tax.itemDedCalc(houseIntSum,charExpense,slpTaxes=0)
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

loanPaySum = ln.genLoanCalc(loan,years)

plt.clf()
plt.plot(loanPaySum)

#[houseWorthSum,housePaySum,housePropSum,houseIntSum] = ln.mortgageCalc(house,years,salary)

#[totalExpenses,charExpense] = exp.expensesCalc(salary,years,numChild,ageChild,house,houseWorthSum,loanPaySum)