import numpy as np

class Taxes:
    
    def __init__(self,var,rates,
                 maxChildYr=22):
        self.var = var
        self.rates = rates
        
        self.years = var['years']        
        self.filing = self.var['filing']['filingType']
        self.filingState = self.var['filing']['filingState']
        self.numInd = self.var['numInd']
        
        self.childAges = var['children']['childAges'] 
        self.childYrs = var['children']['childYrs']  
        
        self.houseBal = var['housing']['houseCosts'][0]
        self.houseInt = var['housing']['houseCosts'][2]
        self.propTax = var['housing']['houseCosts'][4]
        
        self.totalChar = var['totalItem'][0]
        
        self.maxChildYr= maxChildYr
    
    def healthCalc(self,hsa=0*12,fsa=0*12,hra=0*12,growthFactor=0.025):        
        hsa = hsa * (self.numInd/self.iters)
        fsa = fsa * (self.numInd/self.iters)
        hra = hra * (self.numInd/self.iters)
        
        healthSav = np.zeros((self.years,self.iters))    
        flexSav = np.zeros((self.years,self.iters))
        healthRe = np.zeros((self.years,self.iters))
        
        for n in range(self.years):
            for m in range(self.iters): 
                healthSav[n,m] = hsa * (1 + growthFactor) ** n
                flexSav[n,m] = fsa  * (1 + growthFactor) ** n
                healthRe[n,m] = hra * (1 + growthFactor) ** n
        
        healthDed = healthSav + flexSav + healthRe
        
        self.healthDed = healthDed   
    
    def benefitsCalc(self,healthPrem=200*12,visPrem=10*12,denPrem=20*12,growthFactor=0.025):    
        healthPrem = healthPrem * (self.numInd/self.iters)
        visPrem = visPrem * (self.numInd/self.iters)
        denPrem = denPrem * (self.numInd/self.iters)
        
        health = np.zeros((self.years,self.iters))    
        vision = np.zeros((self.years,self.iters))
        dental = np.zeros((self.years,self.iters))
        
        for n in range(self.years):
            for m in range(self.iters): 
                health[n,m] = healthPrem * (1 + growthFactor) ** n
                vision[n,m] = visPrem  * (1 + growthFactor) ** n
                dental[n,m] = denPrem * (1 + growthFactor) ** n
            
        benefits = health + vision + dental
        
        self.benefits = benefits
    
    def trad401Calc(self,basePerc=0,growthPerc=0,binWid=5):
        trad401Perc = np.full((self.years,self.numInd),basePerc)
        
        for n in range(1,self.years):
            if n % binWid == 0:
                for m in range(self.numInd):    
                    trad401Perc[n:,m] = trad401Perc[n,m] + growthPerc
                
        self.perc401 = sum((self.perc401,trad401Perc))  
        
        trad401 = np.multiply(trad401Perc,self.salary)
        
        for n in range(self.years):
            for m in range(self.numInd):    
                trad401[n,m] = 19000 if trad401[n,m] > 19000 else trad401[n,m]
        
        self.trad401 = trad401
        
    def roth401Calc(self,basePerc=0.08,growthPerc=0.01,binWid=5):
        roth401Perc = np.full((self.years,self.numInd),basePerc)
        
        for n in range(1,self.years):
            if n % binWid == 0:
                for m in range(self.numInd):  
                    roth401Perc[n:,m] = roth401Perc[n,m] + growthPerc
                
        self.perc401 = sum((self.perc401,roth401Perc))  
        
        roth401 = np.multiply(roth401Perc,self.salary)
        
        for n in range(self.years):
            for m in range(self.numInd):    
                roth401[n,m] = 19000 - self.trad401[n,m] if roth401[n,m] + self.trad401[n,m] > 19000 else roth401[n,m]
        
        self.roth401 = roth401

    def match401Calc(self):
        matchPerc = np.zeros((self.years,self.numInd))        
        
        for n in range(self.years):
            for m in range(self.numInd):    
                if self.perc401[n,m] <= 0.04:
                    matchPerc[n,m] = self.perc401[n,m]
                elif self.perc401[n,m] <= 0.1:
                    matchPerc[n,m] = 0.04 + ((self.perc401[n,m] - 0.04) * .5)
                else:
                    matchPerc[n,m] = 0.07
                
        match401 =  np.multiply(matchPerc,self.salary)
        
        for n in range(self.years):
            for m in range(self.numInd):
                match401[n,m] = 37000 if match401[n,m] > 37000 else match401[n,m]
        
        self.match401 = match401
        
    def itemDedCalc(self,slpTax=None):
        #SLP Taxes
        slpDed = np.zeros((self.years,self.iters))
        if slpTax is not None:
            for n in range(self.years):
                for m in range(self.iters):
                    slpDed[n,m] = 10000/self.iters if slpTax[n,m] > 10000/self.iters else slpTax[n,m]
        
        #Mortgage Interest
        mortInt = np.zeros((self.years,self.iters))
        for n in range(self.years):
            for m in range(self.iters):
                if self.houseBal[n] < 750000/self.iters:
                    mortInt[n,m] = self.houseInt[n]
                else:
                    mortInt[n,m] = (self.houseInt[n] / self.houseBal[n]) * 750000/self.iters
            
        #Charitable Donations
        charDon = np.zeros((self.years,self.iters))
        for n in range(self.years):
            for m in range(self.iters): 
                charDon[n,m] = self.totalChar[n]/self.iters
                
        itemDedState = mortInt + charDon
        itemDedFed = itemDedState + slpDed
        
        self.itemDed = [itemDedFed,itemDedState]
    
    def stdDedCalc(self):
        stdDedFed = np.full((self.years,self.iters),24000/self.iters)
    
        stdDedState = np.zeros((self.years,self.iters))
        for n in range(self.years):
            for m in range(self.iters): 
                if self.filingState[m] == 'MD':
                    stdDedState[n,m] = 0.15 * self.salary[n,m]
                    
                    if stdDedState[n,m] < 3000/self.iters:
                        stdDedState[n,m] = 3000/self.iters
                    elif stdDedState[n,m] > 4500/self.iters:
                        stdDedState[n,m] = 4500/self.iters
                
        self.stdDed = [stdDedFed,stdDedState]
    
    def exemptCalc(self):
        totalExFed = np.zeros((self.years,self.iters))        
        
        persStateEx = np.zeros((self.years,self.iters))
        childStateEx = np.zeros((self.iters,self.years,len(self.childYrs)))
        
        persBrackets = []
        for m in range(self.iters):
            for state in self.rates['persExempt']:
                if state[0] == self.filingState[m]:   
                    for filing in state[1]:
                        if filing[0] == self.filing:
                            bracket = filing[1]
                            persBrackets.append(bracket)
                            
        childBrackets = []
        for m in range(self.iters):
            for state in self.rates['childExempt']:
                if state[0] == self.filingState[m]:   
                    for filing in state[1]:
                        if filing[0] == self.filing:
                            bracket = filing[1]
                            childBrackets.append(bracket)
        
        for n in range(self.years):  
            for m in range(self.iters):
                for bracket in persBrackets[m]:                    
                    if self.salary[n,m] < bracket[0] and persStateEx[n,m] == 0:
                        persStateEx[n,m] = bracket[1]
            
        for n in range(self.years):  
            for m in range(len(self.childYrs)):
                for x in range(self.iters):
                    if self.childAges[n,m] > 0:
                        for bracket in childBrackets[x]: 
                            if self.salary[n,x] < bracket[0] and childStateEx[x,n,m] == 0:
                                childStateEx[x,n,m] = bracket[1]
                            
                for x in range(self.iters):
                    if childStateEx[x,n,m] == np.mean(childStateEx[:,n,m]):
                        if self.salary[n,x] != np.max(self.salary[n,:]):
                            childStateEx[x,n,m] = 0
                    elif childStateEx[x,n,m] != np.max(childStateEx[:,n,m]):
                        childStateEx[x,n,m] = 0
        
        
        childStateEx = np.sum(childStateEx,axis=2).reshape(self.iters,self.years).transpose()
        
        totalExState = persStateEx + childStateEx
        
        self.totalEx = [totalExFed,totalExState]
    
    def grossEarnCalc(self):
        grossIncFed = np.zeros((self.years,self.iters))
        grossIncState = np.zeros((self.years,self.iters))
        
        for n in range(self.years):  
            for m in range(self.iters):
                grossIncFed[n,m] = self.salary[n,m] - (self.trad401[n,m] + self.healthDed[n,m] + self.totalEx[0][n,m])
                grossIncState[n,m] = self.salary[n,m] - (self.trad401[n,m] + self.healthDed[n,m] + self.totalEx[1][n,m])
                    
                if self.itemDed[0][n,m] > self.stdDed[0][n,m]:
                    grossIncFed[n,m] = grossIncFed[n,m] - self.itemDed[0][n,m]
                else:
                    grossIncFed[n,m] = grossIncFed[n,m] - self.stdDed[0][n,m]
                    
                if self.itemDed[1][n,m] > self.stdDed[1][n,m]:
                    grossIncState[n,m] = grossIncState[n,m] - self.itemDed[1][n,m]
                else:
                    grossIncState[n,m] = grossIncState[n,m] - self.stdDed[1][n,m]
        
        self.grossInc =  [grossIncFed,grossIncState]
    
    def slTaxCalc(self):
        slTax = np.zeros((self.years,self.iters))
        
        localRates = []
        for m in range(self.iters):
            for state in self.rates['incomeLocal']:
                if state[0] == self.filingState[m]:   
                    localRate = state[1]
                    localRates.append(localRate)
        
        brackets = []
        for m in range(self.iters):
            for state in self.rates['incomeState']:
                if state[0] == self.filingState[m]:   
                    for filing in state[1]:
                        if filing[0] == self.filing:
                            bracket = filing[1]
                            brackets.append(bracket)
        
        for n in range(self.years):
            for m in range(self.iters):                
                maxBracket = 0
                for bracket in brackets[m]:
                    minBracket = maxBracket
                    maxBracket = bracket[0]
                    rateBracket = bracket[1]
                    
                    if self.grossInc[1][n,m] > maxBracket:
                        slTax[n,m] = slTax[n,m] + ((maxBracket - minBracket) * rateBracket)
                    elif self.grossInc[1][n,m] > minBracket:
                        slTax[n,m] = slTax[n,m] + ((self.grossInc[1][n,m] - minBracket) * rateBracket)
                                   
                slTax[n,m] = slTax[n,m] + (self.grossInc[1][n,m] * localRates[m])
    
        self.slTax = slTax
        
    def fedTaxCalc(self):
        fedTax = np.zeros((self.years,self.iters))
        
        brackets = []
        for m in range(self.iters): 
            for filing in self.rates['incomeFed']:
                if filing[0] == self.filing:
                    bracket = filing[1]
                    brackets.append(bracket)
        
        for n in range(self.years):
            for m in range(self.iters):
                maxBracket = 0
                for bracket in brackets[m]:
                    minBracket = maxBracket
                    maxBracket = bracket[0]
                    rateBracket = bracket[1]
                    
                    if self.grossInc[0][n,m] > maxBracket:
                        fedTax[n,m] = fedTax[n,m] + ((maxBracket - minBracket) * rateBracket)
                    elif self.grossInc[0][n,m] > minBracket:
                        fedTax[n,m] = fedTax[n,m] + ((self.grossInc[0][n,m] - minBracket) * rateBracket)
    
        self.fedTax = fedTax 
    
    def miscTaxCalc(self,ssRate=0.062,mRate=0.0145,amRate=0.009):        
        ssTax = np.zeros((self.years,self.iters))
        mTax = np.zeros((self.years,self.iters))
        
        for fica in self.rates['ficaRates']:
            if fica[0] == 'SS':
                for filing in fica[1]:
                    if filing[0] == self.filing:
                        maxSS = filing[1]
        
        for fica in self.rates['ficaRates']:
            if fica[0] == 'MED':
                for filing in fica[1]:
                    if filing[0] == self.filing:
                        maxMed = filing[1]
                
        for n in range(self.years):
            for m in range(self.iters):
                # Social Security
                if self.grossInc[0][n,m] < maxSS: 
                    ssTax[n,m] = self.grossInc[0][n,m] * ssRate 
                else:
                    ssTax[n,m] = maxSS * ssRate
        
                # Medicare
                if self.grossInc[0][n,m] < maxMed: 
                    mTax[n,m] = self.grossInc[0][n,m] * mRate
                else:
                    mTax[n,m] = (self.grossInc[0][n,m] - maxMed) * (mRate + amRate)
        
        miscTax = ssTax + mTax
        
        self.miscTax = miscTax
    
    def netIncCalc(self):
        totalTaxes = self.fedTax + self.slTax + self.miscTax + self.propTax
        totalDeducted = self.trad401 + self.healthDed
        totalWithheld = self.roth401 + self.benefits
        
        netIncome = self.salary - totalTaxes
        netCash = netIncome - totalDeducted - totalWithheld
        
        netRet = [self.trad401,self.roth401,self.match401]
        
        self.netEarn = [netIncome,netCash,netRet]
        
    def taxRun(self):        
        if self.filing == 'SINGLE' or self.filing == 'SEPARATE':
            self.iters = self.numInd
            self.salary = self.var['salary']['salary']
        elif self.filing == 'JOINT':
            self.iters = 1
            self.salary = np.sum(self.var['salary'],axis=1).reshape(np.shape(self.var['salary']['salary'])[0],1)         
        else:
            raise Exception('Invalid filing option.')
        
        self.perc401 = np.zeros((self.years,self.numInd))
        
        #Benefits
        self.healthCalc()
        self.benefitsCalc()
        
        #Retirement
        self.trad401Calc()
        self.roth401Calc()
        self.match401Calc()  
        
        #Deduction/Exemptions
        self.itemDedCalc()
        self.stdDedCalc()        
        self.exemptCalc()
        
        #State Taxes
        self.grossEarnCalc()
        self.slTaxCalc() 
        
        slpTaxes = self.propTax + self.slTax
        self.itemDedCalc(slpTaxes)
        
        #Federal Taxes
        self.grossEarnCalc()
        self.fedTaxCalc()
        
        #FICA Taxes
        self.miscTaxCalc()
        
        #Net Income    
        self.netIncCalc()
        
        netIncome = self.netEarn[0]
        netCash = self.netEarn[1]
        netRet = self.netEarn[2]
        
        return [netIncome,netCash,netRet]