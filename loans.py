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

def mortgageCalc(house,years,salary):    
    numHouse = np.size(house,axis = 0)
    
    ## Rent
    rentPay = np.zeros((years,1))
    
    for n in range(int(house[0,0])):
        rentPay[n] = 0.175 * salary[n]
        
    rentPay[0] = 1700 * 12
    
    ## Property 
    houseWorth = np.zeros((years,numHouse))
    houseProp = np.zeros((years,numHouse))
    app = 0.0375
    
    for n in range(numHouse):
        for m in range(years):
            if m >= house[n,0]:
                houseWorth[m,n] = house[n,3] * ((1 + app) ** (m - house[n,0]))
                houseProp[m,n] = 0.015 * houseWorth[m,n]
    
    for n in range(numHouse-1):
        for m in range(years):
            if m >= house[n+1,0]:
                houseWorth[m,n] = 0
                houseProp[m,n] = 0
    
    houseWorthSum = np.sum(houseWorth, axis=1).reshape((years,1))
    housePropSum = np.sum(houseProp, axis=1).reshape((years,1))
    
    ## Mortgage
    mortPeriod = np.zeros((numHouse,2))
    
    housePay = np.zeros((years * 12,numHouse))
    houseBal = np.zeros((years * 12,numHouse))
    housePrin = np.zeros((years * 12,numHouse))
    houseInt = np.zeros((years * 12,numHouse)) 
        
    for n in range(numHouse):
        startMort = int(house[n,0] * 12)
        endMort = int((house[n,0] + house[n,1]) * 12) - 1
        
        if endMort > (years * 12) - 1:
            endMort = (years * 12) - 1
        
        mortDown = (house[n,4]/100) * house[n,3]  
        
        rateInt = house[n,2] / (100 * 12)     #r - interest rate, monthly
        termLength = house[n,1] * 12          #n - number of months
        termCount = 0
        
        if n == 0:
            mortPrin = house[n,3] - mortDown
        else:
            mortPrin = house[n,3] - mortDown - houseWorthSum[int(house[n-1,0])]
            
            if mortPrin < 0:
                mortPrin = 0
        
        for m in range(startMort,endMort):
            termCount += 1 
            
            housePay[m,n] = mortPrin * (rateInt * (1 + rateInt) ** termLength) / ((1 + rateInt) ** termLength - 1)
            houseBal[m,n] = mortPrin * ((1 + rateInt) ** termLength - (1 + rateInt) ** termCount) / ((1 + rateInt) ** termLength - 1)
            
            if m > startMort:
                housePrin[m,n] = houseBal[m-1,n] - houseBal[m,n]                
            else:
                housePrin[m,n] = mortPrin - houseBal[m,n]
            
            houseInt[m,n] = housePay[m,n] - housePrin[m,n]
    
    houseBalSum = np.zeros((years,numHouse))
    housePrinSum =  np.zeros((years,numHouse)) 
    houseIntSum =  np.zeros((years,numHouse)) 
    
    for n in range(years):
        for m in range(numHouse):
            houseBalSum[n,m] = houseBal[n*12,m]
        
        tempHousePrin = np.zeros((12,numHouse))
        tempHousePrin = housePrin[n*12:(n*12)+11]
        housePrinSum[n] = np.sum(tempHousePrin,axis=0)
        
        tempHouseInt = np.zeros((12,numHouse))
        tempHouseInt = houseInt[n*12:(n*12)+11]
        houseIntSum[n] = np.sum(tempHouseInt,axis=0)
    
    housePrinSum = np.sum(housePrinSum,axis=1).reshape((years,1))
    houseIntSum = np.sum(houseIntSum,axis=1).reshape((years,1))
    
    houseBalSum = np.sum(houseBalSum,axis=1).reshape((years,1))
    housePaySum = housePrinSum + houseIntSum + housePropSum + rentPay
    
    percMortSal = np.zeros((years,1))
    
    for n in range(years):
        percMortSal[n] = housePaySum[n] / salary[n]
    
    return [houseWorthSum,housePaySum,housePropSum,houseIntSum]