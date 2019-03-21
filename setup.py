import numpy as np
import random as rand

class Setup:
    
    def __init__(self,var):
        self.years = var['years']      
        self.childYrs = var['childYrs']
        self.salaryBase = var['salaryBase']
        
    def salaryCalc(self,growthRate=0.028,growthDev=[0.5,1.75],growthType='compound'):
        salary = []
        for base in self.salaryBase:
            sal = np.zeros((self.years,1))
            sal[0] = base
            
            for n in range(1,self.years):
                if growthType == 'compound':
                    sal[n] = sal[n-1] * (1 + (growthRate * rand.uniform(growthDev[0],growthDev[1])))
                elif growthType == 'linear':
                    salaryMax = base * (1 + growthRate) ** (self.years - 1)
                    sal[n] = sal[n-1] + (((n / (self.years - 1)) * rand.uniform(growthDev[0],growthDev[1])) * (salaryMax - base))
                else:
                    raise Exception('ERROR: Invalid salary growth type specified.')
                    
            salary.append(sal)
        
        self.numInd = len(salary)
        self.salary = np.hstack(salary)
        
    def childCalc(self,maxChildYr=22):
        childAges = np.zeros((self.years,len(self.childYrs)))
        
        for n in range(self.years):
            for m in range(len(self.childYrs)):
                if n >= self.childYrs[m] and n <= (self.childYrs[m] + maxChildYr):
                    childAges[n,m] = n - self.childYrs[m]
                    
        self.childAges = childAges
        
    def setupRun(self):
        self.salaryCalc()
        self.childCalc()
        
        return [self.salary,self.childAges,self.numInd]
        
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