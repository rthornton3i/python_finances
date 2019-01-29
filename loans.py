import numpy as np

def genLoanCalc(loan,years):    
    numLoan = np.size(loan,axis = 0)
    compTime = 12*30
    
    loanPeriod = np.zeros((numLoan,2))
    
    loanPay = np.zeros((years * compTime,numLoan))
    loanBal = np.zeros((years * compTime,numLoan))
    loanPrin = np.zeros((years * compTime,numLoan))
    loanInt = np.zeros((years * compTime,numLoan)) 
        
    for n in range(numLoan):
        startLoan = int(loan[n,0] * compTime)
        endLoan = int((loan[n,0] + loan[n,1]) * compTime) - 1
        
        if endLoan > (years * compTime) - 1:
            endLoan = (years * compTime) - 1
        
        rateInt = loan[n,2] / (100 * compTime)     #r - interest rate, monthly
        termLength = loan[n,1] * compTime          #n - number of months
        termCount = 0
        
        prin = loan[n,3]
            
        if prin < 0:
            prin = 0
        
        for m in range(startLoan,endLoan):
            termCount += 1 
            
            loanPay[m,n] = prin * (rateInt * (1 + rateInt) ** termLength) / ((1 + rateInt) ** termLength - 1)
            loanBal[m,n] = prin * ((1 + rateInt) ** termLength - (1 + rateInt) ** termCount) / ((1 + rateInt) ** termLength - 1)
            
            if m > startLoan:
                loanPrin[m,n] = loanBal[m-1,n] - loanBal[m,n]                
            else:
                loanPrin[m,n] = prin - loanBal[m,n]
            
            loanInt[m,n] = loanPay[m,n] - loanPrin[m,n]
    
    loanBalSum = np.zeros((years,numLoan))
    loanPrinSum =  np.zeros((years,numLoan)) 
    loanIntSum =  np.zeros((years,numLoan)) 
    
    for n in range(years):
        for m in range(numLoan):
            loanBalSum[n,m] = loanBal[n*compTime,m]
        
        tempLoanPrin = np.zeros((12,numLoan))
        tempLoanPrin = loanPrin[n*compTime:(n*compTime)+(compTime-1)]
        loanPrinSum[n] = np.sum(tempLoanPrin,axis=0)
        
        tempLoanInt = np.zeros((12,numLoan))
        tempLoanInt = loanInt[n*compTime:(n*compTime)+(compTime-1)]
        loanIntSum[n] = np.sum(tempLoanInt,axis=0)
    
    loanPrinSum = np.sum(loanPrinSum,axis=1).reshape((years,1))
    loanIntSum = np.sum(loanIntSum,axis=1).reshape((years,1))
    
    loanBalSum = np.sum(loanBalSum,axis=1).reshape((years,1))
    loanPaySum = loanPrinSum + loanIntSum
    
    return loanPaySum