import setup
import loans as ln
import expenses as exp
import taxes as tax

import numpy as np

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

loan = np.array([[0 , 7 , 4.0 , 36700]])

# house# = [purchase year, mortgage period (yr), interest rate (%), purchase cost, down payment (%)]
house = np.array([[6  , 30 , 4.25 , 450000  , 20 ],
                  [20 , 30 , 4    , 700000  , 20 ],
                  [33 , 10 , 3.25 , 7500000 , 20 ]])

salary = setup.salaryCalc(salaryBase,years,growthRate=0.028,growthType=1)
ageChild = setup.childCalc(years,numChild)

loanPaySum = ln.genLoanCalc(loan)

[houseWorthSum,housePaySum,housePropSum,houseIntSum] = ln.mortgageCalc(house,years,salary)

[totalExpenses,charExpense] = exp.expensesCalc(salary,years,numChild,ageChild,house,houseWorthSum,loanPaySum)