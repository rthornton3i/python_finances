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