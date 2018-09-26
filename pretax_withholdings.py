import main
import salary as sal

import numpy as np

## Deductions
# Standard
if main.filing == 1:
    stdDed = np.full((main.years,1),24000)
elif main.filing == 2:
    stdDed = np.full((main.years,1),12000)

## Itemized
# State, Local, & Property
#try:
#    stateTaxes
#except NameError:
stateTaxes = np.zeros((main.years,1))

for n in range(main.years):
    stateTaxes[n] = 0.05 * sal.salary[n]
    
slDed = stateTaxes

print(stateTaxes)

#==============================================================================
# propDed = zeros(year,1);
# if exist('houseProp','var')
#     propDed = houseProp;
# end
# 
# slpDed = slDed + propDed;
# 
# for n = 1:year
#     if slpDed(n) > 10000
#         slpDed(n) = 10000;
#     end
# end
# 
# # Mortgage & Loan Interest
# 
# loanDed = zeros(year,1);
# if exist('houseInt','var')
#     loanDed = houseInt;
# end
# 
# # [slDed propDed loanDed];
# 
# # Charitable Donations
# 
# charDed = zeros(year,1);
# if exist('charExpense','var')
#     charDed = -charExpense(:,10);
# end
# 
# ## Traditional 401k & IRA
# 
# trad401 = 0;
# 
# tradIRA = 0;
# 
# ## HSA & FSA
# 
# hsaCont = 0;
# 
# fsaCont = 0;
# 
# ## Total Pretax
# 
# itemDed = slpDed + loanDed + charDed;
# 
# # [slpDed loanDed charDed];
# 
# totalDed = zeros(year,1);
# 
# for n = 1:year
#     if itemDed(n) > stdDed(n)
#         totalDed(n) = itemDed(n);
#     else
#         totalDed(n) = stdDed(n);
#     end
# end
# 
# totalDed = totalDed + trad401 + tradIRA + hsaCont + fsaCont;
#==============================================================================
