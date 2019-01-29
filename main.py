import setup
import loans

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

salary = setup.salaryCalc(salaryBase,years,growthRate=0.028,growthType=1)
ageChild = setup.childCalc(years,numChild)

loanPaySum = loans.genLoanCalc(loan)