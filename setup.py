import numpy as np
import random as rand

def salaryCalc(salaryBase,years,growthRate=0.028,growthType=1):
    salaryMax = salaryBase * (1 + growthRate) ** years
    
    salary = np.zeros((years,1))
    
    for n in range(years):
        dev = 0.15
        rMin = 1 - dev
        rMax = 1 + dev
        r = rMin + (rMax - rMin) * rand.random()
    
        if growthType == 1:
            randFactor = rand.randint(75,95)/100
            initialValueFactor = (salaryMax / salaryBase) * (years / 5)
            growthFactor = np.log(((1 / .95) - 1) / initialValueFactor) / ((-randFactor) * years)
    
            rMin = rMin * growthFactor
            rMax = rMax * growthFactor
            r = rMin + (rMax - rMin) * rand.random()
    
            salary[n] = (((salaryMax - salaryBase) / (1 + (initialValueFactor * np.exp(-r * n)))) + salaryBase) - (((years - n) / years) * 0.075 * salaryBase)
        elif growthType == 2:
            salary[n] = ((((salaryMax - salaryBase) / years) * r) * n) + salaryBase
        elif growthType == 3:
            salary[n] = salaryBase * (1 + r * growthRate) ** n
        elif growthType == 4:
            salary[n] = (salaryBase + (1 - np.exp(-n * r * growthRate)) * salaryMax)
            
    return salary

def childCalc(years,numChild):
    ageChild = np.zeros((years,len(numChild)))
    
    for n in range(years):
        for m in range(len(numChild)):
            if n >= numChild[m] and n <= (numChild[m] + 22):
                ageChild[n,m] = n - numChild[m]
                
    return ageChild