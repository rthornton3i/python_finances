import numpy as np

import matplotlib.pyplot as plt

class Setup:
    
    def __init__(self,var):
        self.years = var['years'] 
        self.baseAges = var['ages']['baseAges']
        self.childYrs = var['children']['childYrs']
        self.salaryBases = var['salary']['salaryBase']

    def setupRun(self):
        self.salaryCalc()
        self.ageCalc()
        
    def salaryCalc(self,growthRate=[0.015,0.028,0.05]):
        salaries = []
        for salaryBase in self.salaryBases:
            salary = np.zeros((self.years,1))
            salary[0] = salaryBase
            
            for n in range(1,self.years):
                salary[n] = salary[n-1] * (1 + np.random.triangular(growthRate[0],growthRate[1],growthRate[2]))
                    
            salaries.append(salary)
        
        self.numInd = len(salaries)
        self.salary = np.hstack(salaries)
        
    def ageCalc(self,maxChildYr=22):
        ages = np.zeros((self.years,self.numInd))
        childAges = np.zeros((self.years,len(self.childYrs)))
        
        for n in range(self.years):
            for m in range(len(self.baseAges)):
                ages[n,m] = self.baseAges[m] + n
                
            for m in range(len(self.childYrs)):
                if n >= self.childYrs[m] and n <= (self.childYrs[m] + maxChildYr):
                    childAges[n,m] = n - self.childYrs[m]
               
        self.ages = ages
        self.childAges = childAges