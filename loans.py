import numpy as np

class Loans:
    
    def __init__(self,var):
        
        self.years = var['years']
        self.salary = np.sum(var['salary'],axis=1)
        
        self.rentStart = var['rent'][0]
        self.rentEnd = var['rent'][1]
        
        self.curBal = None
        self.curPay = None
        self.curInt = None
        self.curWth = None 
        self.curTax = None
        self.curDwn = None
        
        self.carPay = None
        self.carWth = None
        self.carDwn = None
    
    def mortgageCalc(self,house,compType='daily',sellPrev=True,app=0.0375,propTaxRate=0.015):
        """house = [Start Yr, Term length (Yrs), Interest Rate (%), Amount ($), Down Payment (%)]"""
        
        def curSet(vals):
            vals = np.zeros((self.years,1)) if vals is None else np.vstack((vals[:int(house[0])],np.zeros((self.years,1))))[:self.years]
            
            return vals
        
        def catArray(vals,sumOpt=True):
            if sumOpt is True:        
                vals = np.reshape([sum(vals[i:i+compTime]) for i in range(0,len(vals),compTime)],(self.years,1))
            elif sumOpt is False:
                vals = np.reshape([vals[i] for i in range(0,len(vals),compTime)],(self.years,1))
            else:
                raise Exception('Invalid option specified.')
                
            return vals
        
        if compType == 'daily':
            compTime = 365
        elif compType == 'monthly':
            compTime = 12
        elif compType == 'annually':
            compTime = 1
        
        bal = 0 if self.curBal is None else self.curBal[int(house[0]),0]
        worth = 0 if self.curWth is None or sellPrev == False else self.curWth[int(house[0]),0]
        
        self.curBal = curSet(self.curBal)
        self.curPay = curSet(self.curPay)
        self.curInt = curSet(self.curInt)
        self.curDwn = curSet(self.curDwn)
        
        mortPay = np.zeros((self.years * compTime,1))
        mortBal = np.zeros((self.years * compTime,1))
        mortPrin = np.zeros((self.years * compTime,1))
        mortInt = np.zeros((self.years * compTime,1))
        
        startHouse = int(house[0] * compTime)
        endHouse = int(house[0] + house[1] * compTime) if (house[0] + house[1]) * compTime < self.years * compTime else (self.years * compTime)
        
        rateInt = house[2] / (100 * compTime)     #r - interest rate, monthly
        termLength = house[1] * compTime          #n - number of months
        down = (house[4] / 100) * house[3]
        prin = house[3] + bal - worth - down
          
        termCount = 0
        for n in range(startHouse,endHouse):
            if prin > 0: 
                termCount += 1 
                termConst = (1 + rateInt) ** termLength
                
                mortBal[n] = prin * (termConst - (1 + rateInt) ** termCount) / (termConst - 1)            
                mortPay[n] = prin * (rateInt * termConst) / (termConst - 1)
                mortPrin[n] = mortBal[n-1] - mortBal[n] if n > startHouse else prin - mortBal[n]
                mortInt[n] = mortPay[n] - mortPrin[n]
            else:
                mortBal[n] = 0
                mortPay[n] = 0
                mortPrin[n] = 0
                mortInt[n] = 0
        
        mortBal = catArray(mortBal,sumOpt=False) 
        mortPrin = catArray(mortPrin,sumOpt=True) 
        mortInt = catArray(mortInt,sumOpt=True) 
        mortPay = mortPrin + mortInt
            
        self.curBal = sum((self.curBal,mortBal))  
        self.curPay = sum((self.curPay,mortPay))
        self.curInt = sum((self.curInt,mortInt))
        self.curDwn = np.asarray([value if index != (int(house[0]),0) else down for index,value in np.ndenumerate(self.curDwn)]).reshape((self.years,1))
        
        if sellPrev == True:
            self.curWth = curSet(self.curWth)
            self.curTax = curSet(self.curTax)
        else:
            self.curWth = np.zeros((self.years,1)) if self.curWth is None else self.curWth
            self.curTax = np.zeros((self.years,1)) if self.curTax is None else self.curTax
        
        houseWth = np.zeros((self.years,1)) 
        propTax = np.zeros((self.years,1)) 
    
        startHouse = int(house[0])
        endHouse = int(house[0] + house[1]) if house[0] + house[1] < self.years else self.years
        
        for n in range(startHouse,endHouse):
            houseWth[n] = house[3] * ((1 + app) ** (n - house[0]))
            propTax[n] = propTaxRate * houseWth[n]
        
        self.curWth = sum((self.curWth,houseWth))
        self.curTax = sum((self.curTax,propTax))
        
        houseCosts = [self.curBal,self.curPay,self.curInt,self.curWth,self.curTax,self.curDwn]

        return [houseCosts]
    
    def rentCalc(self,basePerc=0.25,percDec=0.01,rentPerc=None):
        rentPerc = [basePerc * (1-percDec) ** n for n in range(self.years)] if rentPerc is None else rentPerc
        
        rentPay = np.zeros((self.years,1))
        for n in range(self.rentStart,self.rentEnd):
            rentPay[n] = rentPerc[n] * self.salary[n]
        
        return [rentPay]
    
    def carCalc(self,car,intRate=0.019/12,term=60):  
        """car = [Purchase Yr, Sell Yr, Amount ($), Down Payment ($)]
           intRate = Loan Interest (%)
           term = Loan Term Length"""
        
        def curSet(vals):
            vals = np.zeros((self.years,1)) if vals is None else vals
            
            return vals
            
        self.carPay = curSet(self.carPay)
        self.carWth = curSet(self.carWth)
        self.carDwn = curSet(self.carDwn)
           
        carWorth = car[2]
        carDown = car[3]
        carPrin = carWorth - carDown
        
        carMonthly = carPrin * (intRate * (1 + intRate) ** term) / ((1 + intRate) ** term - 1)        
        termYr = int(term / 12)
        
        for n in range(car[0],car[0]+termYr):
            self.carPay[n] = self.carPay[n] + (carMonthly * 12)
            
        for n in range(car[0],car[1]):
            self.carWth[n] = self.carWth[n] + carWorth
        
        self.carDwn[car[0]] = self.carDwn[car[0]] + carDown
        
        carCosts = [self.carPay,self.carWth,self.carDwn]

        return [carCosts]
        
    def genLoanCalc(self,loan,compType='daily'):
        """loan = [Start Yr, Term Length (Yrs), Interest Rate (%), Amount ($)]"""
        
        def catArray(vals,sumOpt=True):
            if sumOpt is True:        
                vals = np.reshape([sum(vals[i:i+365]) for i in range(0,len(vals),365)],(self.years,1))
            elif sumOpt is False:
                vals = np.reshape([vals[i] for i in range(0,len(vals),365)],(self.years,1))
            else:
                raise Exception('Invalid option specified.')
                
            return vals
    
        if compType == 'daily':
            compTime = 365
        elif compType == 'monthly':
            compTime = 12
        elif compType == 'annually':
            compTime = 1
            
        loanPay = np.zeros((self.years * compTime,1))
        loanBal = np.zeros((self.years * compTime,1))
        loanPrin = np.zeros((self.years * compTime,1))
        loanInt = np.zeros((self.years * compTime,1)) 
        
        startLoan = int(loan[0] * compTime)
        endLoan = int((loan[0] + loan[1]) * compTime) if (loan[0] + loan[1]) * compTime < self.years * compTime else self.years * compTime
        
        rateInt = loan[2] / (100 * compTime)     #r - interest rate, monthly
        termLength = loan[1] * compTime          #n - number of months
        prin = loan[3]
        
        termCount = 0    
        for n in range(startLoan,endLoan):
            termCount += 1 
            termConst = (1 + rateInt) ** termLength
            
            loanPay[n] = prin * (rateInt * termConst) / (termConst - 1)
            loanBal[n] = prin * (termConst - (1 + rateInt) ** termCount) / (termConst - 1)
            loanPrin[n] = loanBal[n-1] - loanBal[n] if n > startLoan else prin - loanBal[n]
            loanInt[n] = loanPay[n] - loanPrin[n]
        
        loanBalSum = catArray(loanBal,sumOpt=False) 
        loanPrinSum = catArray(loanPrin,sumOpt=True) 
        loanIntSum = catArray(loanInt,sumOpt=True)
        loanPaySum = loanPrinSum + loanIntSum
        
        return [loanPaySum,loanBalSum,loanIntSum]