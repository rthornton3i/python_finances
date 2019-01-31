import numpy as np
import matplotlib.pyplot as plt

import taxes as tax
import loans as ln
import setup

years = 40
salary = setup.salaryCalc(160000,years)

house = np.array([6  , 30 , 4.25 , 450000  , 20 ])
[totalPay,totalBal,totalInt,totalWth,totalTax] = ln.mortgageCalc(house,years,curPay=None,curBal=None,curInt=None,curWth=None,curTax=None,app=0.0375)

plt.clf()
plt.plot(totalInt[])