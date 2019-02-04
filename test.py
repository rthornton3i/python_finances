import numpy as np
import random as rand
import math
import matplotlib.pyplot as plt

import setup

years = 40
salaryBase = 77000+86000
salary = setup.salaryCalc(salaryBase,years,growthRate=0.028,growthType=1)

def randExp(years,maxExp,decayFactor=3,binWid=5):
    totalRand = np.zeros((years,1))
    
    x = np.arange(maxExp)
    y = math.e**(-x/(len(x)/decayFactor))
    expWid = maxExp * binWid / years
    
    for n in range(years):
        curBin = math.floor(n / binWid)
        
        while True:
            randFactor = rand.random()
            expense = -(len(x)/decayFactor) * math.log(randFactor,math.e)
            expBin = math.floor(expense / expWid)
            
            if expBin <= curBin:
                totalRand[n] = expense
                break
    
    return [totalRand,y]
    
#for n in range(1000):
[totalRand,y] = randExp(years,maxExp=25000,decayFactor=3,binWid=5)

plt.clf()
plt.plot(totalRand)