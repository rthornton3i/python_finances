import numpy as np
from math import inf

class Taxes:
    
    def __init__(self,var):
        self.var = var
        
        self.years = var['years']
        self.filing = self.var['filing']
        self.numInd = self.var['numInd']
        
        self.houseBal = var['houseCosts'][0]
        self.houseInt = var['houseCosts'][2]
        self.propTax = var['houseCosts'][4]
        
        self.totalChar = var['totalItem'][0]
    
    def healthCalc(self,hsa=0,fsa=0,hra=0):
        hsa = np.full((self.years,1),0) if hsa == 0 else hsa
        fsa = np.full((self.years,1),0) if fsa == 0 else fsa
        hra = np.full((self.years,1),0) if hra == 0 else hra
        
        healthDed = hsa + fsa + hra
        
        self.healthDed = healthDed   
    
    def benefitsCalc(self,healthPrem=200*12,visPrem=10*12,denPrem=20*12,growthFactor=0.025):    
        healthPrem = healthPrem * self.iters
        visPrem = visPrem * self.iters
        denPrem = denPrem * self.iters
        
        health = np.zeros((self.years,1))    
        vision = np.zeros((self.years,1))
        dental = np.zeros((self.years,1))
        
        for n in range(self.years):
            health[n] = healthPrem * (1 + growthFactor) ** n
            vision[n] = visPrem  * (1 + growthFactor) ** n
            dental[n] = denPrem * (1 + growthFactor) ** n
            
        benefits = health + vision + dental
        
        self.benefits = benefits
    
    def trad401Calc(self,basePerc=0,growthPerc=0):
        trad401Perc = np.full((self.years,self.iters),basePerc)
        
        for m in range(self.iters):
            for n in range(1,self.years):
                if n % 5 == 0:
                    trad401Perc[n:self.years,m] = trad401Perc[n,m] + growthPerc
                
        self.perc401 = sum((self.perc401,trad401Perc))  
        
        trad401 = trad401Perc * self.salary
        print(trad401)
        
        for n in range(self.years):
            trad401[n] = 19000 if trad401[n] > 19000 else trad401[n]
        
        self.trad401 = trad401
        
    def roth401Calc(self,basePerc=0.04,growthPerc=0.01):
        roth401Perc = np.full((self.years,1),basePerc)
        
        for n in range(1,self.years):
            if n % 5 == 0:
                roth401Perc[n:self.years] = roth401Perc[n] + growthPerc
        
        self.perc401 = sum((self.perc401,roth401Perc))
        
        roth401 = roth401Perc * self.salary
        
        for n in range(self.years):
            roth401[n] = 19000 if roth401[n] > 19000 else roth401[n]
        
        self.roth401 = roth401

    def match401Calc(self):
        matchPerc = np.zeros((self.years,1))        
        
        for n in range(self.years):
            if self.perc401[n] <= 0.04:
                matchPerc[n] = self.perc401[n]
            elif self.perc401[n] <= 0.1:
                matchPerc[n] = 0.04 + ((self.perc401[n] - 0.04) * .5)
            else:
                matchPerc[n] = 0.07
                
        match401 = matchPerc * self.salary
        
        cont401 = np.zeros((self.years,1))
        for n in range(self.years):
            cont401[n] = 19000 if self.roth401[n] + self.trad401[n] > 19000 else self.roth401[n] + self.trad401[n]
            match401[n] = 37000 if match401[n] > 37000 else match401[n]
        
        self.cont401 = cont401
        self.match401 = match401
        
    def itemDedCalc(self):
        #SLP Taxes
        slpDed = np.zeros((self.years,1))
        if self.slpTax is not None :
            for n in range(self.years):
                slpDed[n] = 10000 if self.slpTax[n] > 10000 else self.slpTax[n]
        
        #Mortgage Interest
        mortInt = np.zeros((self.years,1))
        for n in range(self.years):
            if self.houseBal[n] < 750000:
                mortInt[n] = self.houstInt[n]
            else:
                mortInt[n] = (self.houseInt[n] / self.houseBal[n]) * 750000
            
        #Charitable Donations
        charDon = self.totalChar  
                
        itemDedState = mortInt + charDon
        itemDedFed = itemDedState + slpDed
        
        self.itemDed = [itemDedFed,itemDedState]
    
    def stdDedCalc(self):
        if self.filing == 'SINGLE':
            stdDedFed = np.full((self.years,1),12000)
        elif self.filing == 'JOINT':
            stdDedFed = np.full((self.years,1),24000)
        elif self.filing == 'SEPARATE':
            stdDedFed = np.full((self.years,2),12000)
        else:
            raise Exception('Invalid filing option.')
    
        stdDedState = np.zeros((self.years,1))
        for n in range(self.years):
            stdDedState[n] = 0.15 * self.salary[n]
            
            if stdDedState[n] < 3000:
                stdDedState[n] = 3000
            elif stdDedState[n] > 4000:
                stdDedState[n] = 4000
                
        self.stdDed = [stdDedFed,stdDedState]
    
    def exemptCalc(self,numChild):
        persStateEx = np.zeros((self.years,1))
        childStateEx = np.zeros((self.years,len(numChild)))
        
        for n in range(self.years):  
            if self.salary[n] < 150000:
                persStateEx[n] = 3200 * 2
                for m in range(len(numChild)):
                    if n >= numChild[m] and n <= (numChild[m] + 22):
                        childStateEx[n,m] = 3200
            elif self.salary[n] < 175000:
                persStateEx[n] = 1600 * 2
                for m in range(len(numChild)):
                    if n >= numChild[m] and n <= (numChild[m] + 22):
                        childStateEx[n,m] = 1600
            elif self.salary[n] < 200000:
                persStateEx[n] = 800 * 2
                for m in range(len(numChild)):
                    if n >= numChild[m] and n <= (numChild[m] + 22):
                        childStateEx[n,m] = 800
            else:
                persStateEx[n] = 0
                for m in range(len(numChild)):
                    childStateEx[n,m] = 0
                    
        childStateEx = childStateEx.sum(axis=1).reshape(self.years,1)    
            
        totalExState = persStateEx + childStateEx
        totalExFed = np.zeros((self.years,1))
        
        return [totalExState,totalExFed]
    
    def grossIncCalc(self,trad401,healthDed,totalExFed,totalExState):
        grossIncState = self.salary - (trad401 + healthDed + totalExState)
        grossIncFed = self.salary - (trad401 + healthDed + totalExFed)
        
        return [grossIncState,grossIncFed]
    
    def miscTaxCalc(self):
        socialSecurity = .062
        medicare = .0145
        medicareAdditional = .009
        
        maxTaxSS = 127200
        minTaxAM = 250000
        
        # Social Security
        ssTax = np.zeros((self.years,1))
        
        for n in range(self.years):
            if self.salary[n] < maxTaxSS: 
                ssTax[n] = self.salary[n] * socialSecurity 
            else:
                ssTax[n] = maxTaxSS * socialSecurity
        
        # Medicare
        mTax = np.zeros((self.years,1))
        
        for n in range(self.years):  
            mTax[n] = self.salary[n] * medicare
        
        # Additional Medicare
        amTax = np.zeros((self.years,1))
        
        for n in range(self.years):
            if self.salary[n] > minTaxAM:
                amTax[n] = self.salary[n] * medicareAdditional 
        
        miscTaxes = ssTax + mTax + amTax
        
        return miscTaxes
    
    def slTaxCalc(self,grossIncState,itemDedState,stdDedState):
        localTaxPerc = 0.025
        stateTax = np.zeros((self.years,1))
        stateLocalTax = np.zeros((self.years,1))
        
        for n in range(self.years):
            if itemDedState[n] > stdDedState[n]:
                grossIncState[n] = grossIncState[n] - itemDedState[n]
            else:
                grossIncState[n] = grossIncState[n] - stdDedState[n]
        
        brackets = np.asarray([[0,1000,0.02],
                               [1001,2000,0.03],
                               [2001,3000,0.04],
                               [3001,150000,0.0475],
                               [150001,175000,0.05],
                               [175001,225000,0.0525],
                               [225001,300000,0.055],
                               [300001,inf,0.0575]])
                    
        for n in range(self.years):
            for bracket in brackets:
                if grossIncState[n] > bracket[1]:
                    stateTax[n] = stateTax[n] + ((bracket[1] - bracket[0]) * bracket[2])
                elif grossIncState[n] > bracket[0]:
                    stateTax[n] = stateTax[n] + ((grossIncState[n] - bracket[0]) * bracket[2])
                               
            stateLocalTax[n] = stateTax[n] + (grossIncState[n] * localTaxPerc)
    
        return stateLocalTax
        
    def fedTaxCalc(self,grossIncFed,itemDedFed,stdDedFed):
        fedTax = np.zeros((self.years,1))
        
        for n in range(self.years):
            if itemDedFed[n] > stdDedFed[n]:
                grossIncFed[n] = grossIncFed[n] - itemDedFed[n]
            else:
                grossIncFed[n] = grossIncFed[n] - stdDedFed[n]
        
        brackets = np.asarray([[0,19050,0.1],
                               [19051,77400,0.12],
                               [77401,165000,0.22],
                               [165001,315000,0.24],
                               [315001,400000,0.32],
                               [400001,600000,0.35],
                               [600001,inf,0.37]])
                    
        for n in range(self.years):
            for bracket in brackets:
                if grossIncFed[n] > bracket[1]:
                    fedTax[n] = fedTax[n] + ((bracket[1] - bracket[0]) * bracket[2])
                elif grossIncFed[n] > bracket[0]:
                    fedTax[n] = fedTax[n] + ((grossIncFed[n] - bracket[0]) * bracket[2])
        
        return fedTax    
    
    def netIncCalc(self,fedTax,stateLocalTax,propTax,miscTaxes,roth401,trad401,benefits,healthDed):
        totalTaxes = fedTax + stateLocalTax + propTax + miscTaxes
        totalWithheld = roth401 + trad401 + benefits + healthDed
        
        netIncome = self.salary - totalTaxes
        netCash = netIncome - totalWithheld
        
        return [netIncome,netCash]
        
    def taxRun(self):        
        if self.filing == 'SINGLE' or self.filing == 'SEPARATE':
            self.iters = self.numInd
            
            self.salary = self.var['salary']
            self.perc401 = np.zeros((self.years,self.numInd))
        elif self.filing == 'JOINT':
            self.iters = 1
            
            self.salary = sum(self.salary)
            self.perc401 = np.zeros((self.years,1))            
        else:
            raise Exception('Invalid filing option.')
            
        self.healthCalc()
        self.benefitsCalc()
        
        self.trad401Calc()
#        self.roth401Calc()
#        self.match401Calc()  
#        
#        self.itemDedCalc()
#        self.stdDedCalc()
#        
#        self.healthDed  
#        self.benefits      
#        
#        self.cont401
#        self.match401
#        
#        self.itemDed
#        self.stdDed
        
#        #Pretax Benefits
#        healthDed = tax.healthDedCalc(years,hsa=0,fsa=0,hra=0)  
#        [trad401,trad401Match] = tax.trad401Calc(salary,years,base401Perc=0,growth401Perc=0)
#           
#        #Deductions
#        [stdDedFed,stdDedState] = tax.stdDedCalc(salary,years)
#        [totalExState,totalExFed] = tax.exemptCalc(salary,years,numChild)
#        
#        [grossIncState,grossIncFed] = tax.grossIncCalc(salary,trad401,healthDed,totalExFed,totalExState)
#        
#        #SS & Medicare Taxes
#        miscTaxes = tax.miscTaxCalc(salary,years)
#        
#        #State Taxes
#        [itemDedFed,itemDedState] = tax.itemDedCalc(years,totalInt,totalChar)
#        stateLocalTax = tax.slTaxCalc(grossIncState,years,itemDedState,stdDedState)
#        
#        #Federal Taxes
#        slpTax = stateLocalTax + propTax
#        [itemDedFed,itemDedState] = tax.itemDedCalc(years,totalInt,totalChar,slpTax)
#        fedTax = tax.fedTaxCalc(grossIncFed,years,itemDedFed,stdDedFed)  
#        
#        #Posttax Benefits
#        [roth401,roth401Match] = tax.roth401Calc(salary,years,base401Perc=0.04,growth401Perc=0.01)
#        benefits = tax.benefitsCalc(years,healthPrem=200,visPrem=10,denPrem=20)
#        
#        [netIncome,netCash] = tax.netIncCalc(salary,fedTax,stateLocalTax,propTax,miscTaxes,roth401,trad401,benefits,healthDed)
#        effTaxRate = np.asarray([(salary[n] - netIncome[n]) / salary[n] for n in range(years)])
#        ret401 = np.hstack((roth401,roth401Match,trad401,trad401Match))
                    
        return 
        
        
def healthDedCalc(years,hsa=0,fsa=0,hra=0):
    hsa = np.full((years,1),0) if hsa == 0 else hsa
    fsa = np.full((years,1),0) if fsa == 0 else fsa
    hra = np.full((years,1),0) if hra == 0 else hra
    
    healthDed = hsa + fsa + hra
    
    return healthDed        
    
def trad401Calc(salary,years,base401Perc=0,growth401Perc=0):
    trad401Perc = np.full((years,1),base401Perc)
    trad401MatchPerc = np.zeros((years,1))
    
    for n in range(1,years):
        if n % 5 == 0:
            trad401Perc[n:years] = trad401Perc[n] + growth401Perc
    
    for n in range(years):
        if trad401Perc[n] <= 0.04:
            trad401MatchPerc[n] = trad401Perc[n]
        elif trad401Perc[n] <= 0.1:
            trad401MatchPerc[n] = 0.04 + ((trad401Perc[n] - 0.04) * .5)
        else:
            trad401MatchPerc[n] = 0.07
            
    trad401 = trad401Perc * salary
    trad401Match = trad401MatchPerc * salary
    
    for n in range(years):
        trad401[n] = 19000 if trad401[n] > 19000 else trad401[n]
        trad401Match[n] = 37000 if trad401Match[n] > 37000 else trad401Match[n]
    
    return [trad401,trad401Match]
    
def itemDedCalc(years,houseInt,charExp,slpTax=None):
    if slpTax is not None :
        for n in range(years):
            slpTax[n] = 10000 if slpTax[n] > 10000 else slpTax[n]
    else:
        slpTax = np.zeros((years,1))
            
    itemDedState = houseInt + charExp
    itemDedFed = itemDedState + slpTax
    
    return [itemDedFed,itemDedState]

def stdDedCalc(salary,years):
    stdDedFed = np.full((years,1),24000)

    stdDedState = np.zeros((years,1))
    for n in range(years):
        stdDedState[n] = 0.15 * salary[n]
        
        if stdDedState[n] < 3000:
            stdDedState[n] = 3000
        elif stdDedState[n] > 4000:
            stdDedState[n] = 4000
            
    return [stdDedFed,stdDedState]

def exemptCalc(salary,years,numChild):
    persStateEx = np.zeros((years,1))
    childStateEx = np.zeros((years,len(numChild)))
    
    for n in range(years):  
        if salary[n] < 150000:
            persStateEx[n] = 3200 * 2
            for m in range(len(numChild)):
                if n >= numChild[m] and n <= (numChild[m] + 22):
                    childStateEx[n,m] = 3200
        elif salary[n] < 175000:
            persStateEx[n] = 1600 * 2
            for m in range(len(numChild)):
                if n >= numChild[m] and n <= (numChild[m] + 22):
                    childStateEx[n,m] = 1600
        elif salary[n] < 200000:
            persStateEx[n] = 800 * 2
            for m in range(len(numChild)):
                if n >= numChild[m] and n <= (numChild[m] + 22):
                    childStateEx[n,m] = 800
        else:
            persStateEx[n] = 0
            for m in range(len(numChild)):
                childStateEx[n,m] = 0
                
    childStateEx = childStateEx.sum(axis=1).reshape(years,1)    
        
    totalExState = persStateEx + childStateEx
    totalExFed = np.zeros((years,1))
    
    return [totalExState,totalExFed]

def grossIncCalc(salary,trad401,healthDed,totalExFed,totalExState):
    grossIncState = salary - (trad401 + healthDed + totalExState)
    grossIncFed = salary - (trad401 + healthDed + totalExFed)
    
    return [grossIncState,grossIncFed]

def miscTaxCalc(salary,years):
    socialSecurity = .062
    medicare = .0145
    medicareAdditional = .009
    
    maxTaxSS = 127200
    minTaxAM = 250000
    
    # Social Security
    ssTax = np.zeros((years,1))
    
    for n in range(years):
        if salary[n] < maxTaxSS: 
            ssTax[n] = salary[n] * socialSecurity 
        else:
            ssTax[n] = maxTaxSS * socialSecurity
    
    # Medicare
    mTax = np.zeros((years,1))
    
    for n in range(years):  
        mTax[n] = salary[n] * medicare
    
    # Additional Medicare
    amTax = np.zeros((years,1))
    
    for n in range(years):
        if salary[n] > minTaxAM:
            amTax[n] = salary[n] * medicareAdditional 
    
    miscTaxes = ssTax + mTax + amTax
    
    return miscTaxes

def slTaxCalc(grossIncState,years,itemDedState,stdDedState):
    localTaxPerc = 0.025
    stateTax = np.zeros((years,1))
    stateLocalTax = np.zeros((years,1))
    
    for n in range(years):
        if itemDedState[n] > stdDedState[n]:
            grossIncState[n] = grossIncState[n] - itemDedState[n]
        else:
            grossIncState[n] = grossIncState[n] - stdDedState[n]
    
    brackets = np.asarray([[0,1000,0.02],
                           [1001,2000,0.03],
                           [2001,3000,0.04],
                           [3001,150000,0.0475],
                           [150001,175000,0.05],
                           [175001,225000,0.0525],
                           [225001,300000,0.055],
                           [300001,inf,0.0575]])
                
    for n in range(years):
        for bracket in brackets:
            if grossIncState[n] > bracket[1]:
                stateTax[n] = stateTax[n] + ((bracket[1] - bracket[0]) * bracket[2])
            elif grossIncState[n] > bracket[0]:
                stateTax[n] = stateTax[n] + ((grossIncState[n] - bracket[0]) * bracket[2])
                           
        stateLocalTax[n] = stateTax[n] + (grossIncState[n] * localTaxPerc)

    return stateLocalTax
    
def fedTaxCalc(grossIncFed,years,itemDedFed,stdDedFed):
    fedTax = np.zeros((years,1))
    
    for n in range(years):
        if itemDedFed[n] > stdDedFed[n]:
            grossIncFed[n] = grossIncFed[n] - itemDedFed[n]
        else:
            grossIncFed[n] = grossIncFed[n] - stdDedFed[n]
    
    brackets = np.asarray([[0,19050,0.1],
                           [19051,77400,0.12],
                           [77401,165000,0.22],
                           [165001,315000,0.24],
                           [315001,400000,0.32],
                           [400001,600000,0.35],
                           [600001,inf,0.37]])
                
    for n in range(years):
        for bracket in brackets:
            if grossIncFed[n] > bracket[1]:
                fedTax[n] = fedTax[n] + ((bracket[1] - bracket[0]) * bracket[2])
            elif grossIncFed[n] > bracket[0]:
                fedTax[n] = fedTax[n] + ((grossIncFed[n] - bracket[0]) * bracket[2])
    
    return fedTax    

def roth401Calc(salary,years,base401Perc=0.04,growth401Perc=0.01):
    roth401Perc = np.full((years,1),base401Perc)
    roth401MatchPerc = np.zeros((years,1))
    
    for n in range(1,years):
        if n % 5 == 0:
            roth401Perc[n:years] = roth401Perc[n] + growth401Perc
    
    for n in range(years):
        if roth401Perc[n] <= 0.04:
            roth401MatchPerc[n] = roth401Perc[n]
        elif roth401Perc[n] <= 0.1:
            roth401MatchPerc[n] = 0.04 + ((roth401Perc[n] - 0.04) * .5)
        else:
            roth401MatchPerc[n] = 0.07
            
    roth401 = roth401Perc * salary
    roth401Match = roth401MatchPerc * salary
    
    for n in range(years):
        roth401[n] = 19000 if roth401[n] > 19000 else roth401[n]
        roth401Match[n] = 37000 if roth401Match[n] > 37000 else roth401Match[n]
    
    return [roth401,roth401Match]
    
def benefitsCalc(years,healthPrem=200,visPrem=10,denPrem=20):    
    health = np.zeros((years,1))    
    vision = np.zeros((years,1))
    dental = np.zeros((years,1))
    
    for n in range(years):
        health[n] = (healthPrem * 12 * 2) * 1.025 ** n
        vision[n] = (visPrem * 12 * 2) * 1.025 ** n
        dental[n] = (denPrem * 12 * 2) * 1.025 ** n
        
    benefits = health + vision + dental
    
    return benefits

def netIncCalc(salary,fedTax,stateLocalTax,propTax,miscTaxes,roth401,trad401,benefits,healthDed):
    totalTaxes = fedTax + stateLocalTax + propTax + miscTaxes
    totalWithheld = roth401 + trad401 + benefits + healthDed
    
    netIncome = salary - totalTaxes
    netCash = netIncome - totalWithheld
    
    return [netIncome,netCash]