import numpy as np
import random as rand

class Setup():
    
    def __init__(self,salaryBase,years,childYrs,growthRate=0.028,growthDev=[0.5,2],growthType='compound',maxChildYr=22):
        self.childYrs = childYrs
        self.maxChildYr = maxChildYr        
        
        self.salaryBase = salaryBase
        self.years = years
        self.growthRate = growthRate
        self.growthDev = growthDev
        self.growthType = growthType
        
        self.salaryCalc()
        self.childCalc()
        
    def salaryCalc(self):
        salary = []
        for base in self.salaryBase:
            sal = np.zeros((self.years,1))
            sal[0] = base
            
            for n in range(1,self.years):
                if self.growthType == 'compound':
                    sal[n] = sal[n-1] * (1 + (self.growthRate * rand.uniform(self.growthDev[0],self.growthDev[1])))
                elif self.growthType == 'linear':
                    salaryMax = base * (1 + self.growthRate) ** (self.years - 1)
                    sal[n] = sal[n-1] + (((n / (self.years - 1)) * rand.uniform(self.growthDev[0],self.growthDev[1])) * (salaryMax - base))
                else:
                    raise Exception('ERROR: Invalid salary growth type specified.')
                    
            salary.append(sal)
        
        self.salary = salary
    
    def childCalc(self):
        ageChild = np.zeros((self.years,len(self.childYrs)))
        
        for n in range(self.years):
            for m in range(len(self.childYrs)):
                if n >= self.childYrs[m] and n <= (self.childYrs[m] + self.maxChildYr):
                    ageChild[n,m] = n - self.childYrs[m]
                    
        self.ageChild = ageChild
        
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