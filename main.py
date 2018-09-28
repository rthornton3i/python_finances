import numpy as np

years = 40
yearsRef = np.arange(23,23+years).reshape((years,1))
yrs = np.arange(years).reshape((years,1))

salaryBase = 160000

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
growth = 1

# Tax Filing
#==============================================================================
#  1) Married Filing Jointly
#  2) Single
#==============================================================================
filing = 1