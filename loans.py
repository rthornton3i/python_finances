import numpy as np

class Loans:
    
    def __init__(self,var,
                 salary):
        
        self.years = var['years']
        self.salary = sum(salary)
        
        self.curBal = None
        self.curPay = None
        self.curInt = None
        self.curWth = None 
        self.curTax = None
        self.curDwn = None
    
    def mortgageCalc(self,house,sellPrev=True,app=0.0375,propTaxRate=0.015):
        """house = [Start Yr, Term length (Yrs), Interest Rate (%), Amount ($), Down Payment (%)]"""
        
        def curSet(vals):
            vals = np.zeros((self.years,1)) if vals is None else np.vstack((vals[:int(house[0])],np.zeros((self.years,1))[int(house[0]):]))
            return vals
        
        bal = 0 if self.curBal is None else self.curBal[int(house[0]),0]
        worth = 0 if self.curWth is None or sellPrev == False else self.curWth[int(house[0]),0]
        
        self.curBal = curSet(self.curBal)
        self.curPay = curSet(self.curPay)
        self.curInt = curSet(self.curInt)
        self.curDwn = curSet(self.curDwn)
        
        mortPay = np.zeros((self.years * 365,1))
        mortBal = np.zeros((self.years * 365,1))
        mortPrin = np.zeros((self.years * 365,1))
        mortInt = np.zeros((self.years * 365,1))
        
        startHouse = int(house[0])
        endHouse = int(house[0] + house[1]) if house[0] + house[1] < self.years else self.years
        
        rateInt = house[2] / (100 * 365)     #r - interest rate, monthly
        termLength = house[1] * 365          #n - number of months
        down = (house[4] / 100) * house[3]
        prin = house[3] + bal - worth - down
          
        termCount = 0
        for n in range(startHouse*365,endHouse*365):
            if prin > 0: 
                termCount += 1 
                termConst = (1 + rateInt) ** termLength
                
                mortBal[n] = prin * (termConst - (1 + rateInt) ** termCount) / (termConst - 1)            
                mortPay[n] = prin * (rateInt * termConst) / (termConst - 1)
                mortPrin[n] = mortBal[n-1] - mortBal[n] if n > startHouse*365 else prin - mortBal[n]
                mortInt[n] = mortPay[n] - mortPrin[n]
            else:
                mortBal[n] = 0
                mortPay[n] = 0
                mortPrin[n] = 0
                mortInt[n] = 0
        
        mortBal = np.reshape([mortBal[i] for i in range(0,len(mortBal),365)],(self.years,1))
        mortPrin = np.reshape([sum(mortPrin[i:i+365]) for i in range(0,len(mortPrin),365)],(self.years,1))
        mortInt = np.reshape([sum(mortInt[i:i+365]) for i in range(0,len(mortInt),365)],(self.years,1))
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
    
        for n in range(startHouse,endHouse):
            houseWth[n] = house[3] * ((1 + app) ** (n - house[0]))
            propTax[n] = propTaxRate * houseWth[n]
        
        self.curWth = sum((self.curWth,houseWth))
        self.curTax = sum((self.curTax,propTax))
        
        return [self.curBal,self.curPay,self.curInt,self.curWth,self.curTax,self.curDwn]
    
    def rentExp(self,termStart,termEnd,basePerc=0.25,percDec=0.01,rentPerc=None):
        rentPerc = [basePerc * (1-percDec) ** n for n in range(self.years)] if rentPerc is None else rentPerc
        
        rentPay = np.zeros((self.years,1))
        for n in range(termStart,termEnd):
            rentPay[n] = rentPerc[n] * self.salary[n]
        
        return [rentPay] 
        
    def genLoanCalc(self,loan,compType='daily'):
        """loan = [Start Yr, Term Length (Yrs), Interest Rate (%), Amount ($)]"""
    
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
        endLoan = int((loan[0] + loan[1]) * compTime) if int((loan[0] + loan[1]) * compTime) < (self.years * compTime) else (self.years * compTime) - 1
        
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
        
        loanBalSum = np.reshape([loanBal[i] for i in range(0,len(loanBal),compTime)],(self.years,1))
        loanPrinSum = np.reshape([sum(loanPrin[i:i+compTime]) for i in range(0,len(loanPrin),compTime)],(self.years,1))
        loanIntSum = np.reshape([sum(loanInt[i:i+compTime]) for i in range(0,len(loanInt),compTime)],(self.years,1))
        loanPaySum = loanPrinSum + loanIntSum
        
        return [loanPaySum,loanBalSum,loanIntSum]

def genLoanCalc(loan,years,compType='daily'):
#    loan = [Start Yr, Term Length (Yrs), Interest Rate (%), Amount]
    if compType == 'daily':
        compTime = 365
    elif compType == 'monthly':
        compTime = 12
    elif compType == 'annually':
        compTime = 1
        
    loanPay = np.zeros((years * compTime,1))
    loanBal = np.zeros((years * compTime,1))
    loanPrin = np.zeros((years * compTime,1))
    loanInt = np.zeros((years * compTime,1)) 
    
    startLoan = int(loan[0] * compTime)
    endLoan = int((loan[0] + loan[1]) * compTime) if int((loan[0] + loan[1]) * compTime) < (years * compTime) else (years * compTime) - 1
    
    rateInt = loan[2] / (100 * compTime)     #r - interest rate, monthly
    termLength = loan[1] * compTime          #n - number of months
    prin = loan[3]
    
    termCount = 0    
    for n in range(startLoan,endLoan):
        termCount += 1 
        
        loanPay[n] = prin * (rateInt * (1 + rateInt) ** termLength) / ((1 + rateInt) ** termLength - 1)
        loanBal[n] = prin * ((1 + rateInt) ** termLength - (1 + rateInt) ** termCount) / ((1 + rateInt) ** termLength - 1)
        
        if n > startLoan:
            loanPrin[n] = loanBal[n-1] - loanBal[n]                
        else:
            loanPrin[n] = prin - loanBal[n]
        
        loanInt[n] = loanPay[n] - loanPrin[n]
    
    loanBalSum = np.reshape([loanBal[i] for i in range(0,len(loanBal),compTime)],(years,1))
    loanPrinSum = np.reshape([sum(loanPrin[i:i+compTime]) for i in range(0,len(loanPrin),compTime)],(years,1))
    loanIntSum = np.reshape([sum(loanInt[i:i+compTime]) for i in range(0,len(loanInt),compTime)],(years,1))
    loanPaySum = loanPrinSum + loanIntSum
    
    return [loanPaySum,loanBalSum,loanIntSum]

def mortgageCalc(house,years,curBal=None,curPay=None,curInt=None,curWth=None,curTax=None,curDwn=None,sellPrev=True,app=0.0375):        
    bal = 0 if curBal is None else curBal[int(house[0]),0]
    worth = 0 if curWth is None or sellPrev == False else curWth[int(house[0]),0]
    
    curBal = np.zeros((years,1)) if curBal is None else np.vstack((curBal[:int(house[0])],np.zeros((years,1))[int(house[0]):]))
    curPay = np.zeros((years,1)) if curPay is None else np.vstack((curPay[:int(house[0])],np.zeros((years,1))[int(house[0]):]))
    curInt = np.zeros((years,1)) if curInt is None else np.vstack((curInt[:int(house[0])],np.zeros((years,1))[int(house[0]):]))
    curDwn = np.zeros((years,1)) if curDwn is None else np.vstack((curDwn[:int(house[0])],np.zeros((years,1))[int(house[0]):]))
    
    housePay = np.zeros((years * 365,1))
    houseBal = np.zeros((years * 365,1))
    housePrin = np.zeros((years * 365,1))
    houseInt = np.zeros((years * 365,1)) 
    
    startHouse = int(house[0])
    endHouse = int(house[0] + house[1]) if house[0] + house[1] < years else years
    
    rateInt = house[2] / (100 * 365)     #r - interest rate, monthly
    termLength = house[1] * 365          #n - number of months
    down = (house[4] / 100) * house[3]
    prin = house[3] + bal - worth - down
      
    termCount = 0
    for n in range(startHouse*365,endHouse*365):
        if prin > 0: 
            termCount += 1 
            
            houseBal[n] = prin * ((1 + rateInt) ** termLength - (1 + rateInt) ** termCount) / ((1 + rateInt) ** termLength - 1)        
            housePay[n] = prin * (rateInt * (1 + rateInt) ** termLength) / ((1 + rateInt) ** termLength - 1)
            housePrin[n] = houseBal[n-1] - houseBal[n] if n > startHouse*365 else prin - houseBal[n]
            houseInt[n] = housePay[n] - housePrin[n]
        else:
            houseBal[n] = 0
            housePay[n] = 0
            housePrin[n] = 0
            houseInt[n] = 0
        
    mortBal = np.reshape([houseBal[i] for i in range(0,len(houseBal),365)],(years,1))
    mortPrin = np.reshape([sum(housePrin[i:i+365]) for i in range(0,len(housePrin),365)],(years,1))
    mortInt = np.reshape([sum(houseInt[i:i+365]) for i in range(0,len(houseInt),365)],(years,1))
    mortPay = mortPrin + mortInt
        
    totalBal = sum((curBal,mortBal))    
    totalPay = sum((curPay,mortPay))
    totalInt = sum((curInt,mortInt))
    totalDwn = np.asarray([value if index != (int(house[0]),0) else down for index,value in np.ndenumerate(curDwn)]).reshape((years,1))
    
    if sellPrev == True:
        curWth = np.zeros((years,1)) if curWth is None else np.vstack((curWth[:int(house[0])],np.zeros((years,1))[int(house[0]):])) 
        curTax = np.zeros((years,1)) if curTax is None else np.vstack((curTax[:int(house[0])],np.zeros((years,1))[int(house[0]):]))
    else:
        curWth = np.zeros((years,1)) if curWth is None else curWth
        curTax = np.zeros((years,1)) if curTax is None else curTax
    
    houseWorth = np.zeros((years,1)) 
    houseTax = np.zeros((years,1)) 

    for n in range(startHouse,endHouse):
        houseWorth[n] = house[3] * ((1 + app) ** (n - house[0]))
        houseTax[n] = 0.015 * houseWorth[n]
    
    houseWth = sum((curWth,houseWorth))
    propTax = sum((curTax,houseTax))
    
    return [totalBal,totalPay,totalInt,houseWth,propTax,totalDwn]