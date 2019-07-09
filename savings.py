import numpy as np
import math
import random as rand

class Savings:
    
    def __init__(self,var):
        self.var = var
        
        self.years = var['years']
        self.childAges = var['children']['childAges']        
        
        self.alloc = var['allocations']    
        self.baseSav = var['baseSavings']
        
        self.totalExp = var['totalExp']
        
    def savingsAllocCalc(self):
        binWid = self.years / (np.shape(self.alloc)[1] - 1)
        savAlloc = np.zeros((self.years,self.numAcc))
        
        for n in range(self.years):
            for m in range(self.numAcc):
                if n == 0:
                    savAlloc[n,m] = self.alloc[m][0]
                else:
                    curBin = math.floor(n / binWid)
                    savAlloc[n,m] = self.alloc[m][curBin] + (((n % binWid) / binWid) * (self.alloc[m][curBin+1] - self.alloc[m][curBin]))
        
        savAlloc = savAlloc / 100
                
        self.savAlloc = savAlloc
    
    def investCalc(self):
        
        #0) hiDiv
        #1) ltLowVol
        #2) largeCap
        #3) stHiVol
        
        #4) retRoth401
        #5) retTrad401
        
        #6) col529      - totalCollege[5]
        
        #7) emergFunds  - totalRand[9]
        #8) longTerm    - totalHouse[3] + totalWed[6] + totalLoan[10]
        #9) shortTerm   - totalAuto[4] + totalVac[7] + totalChar[8]
        #10) excSpend   - totalHol[0] + totalEnt[1] + totalMisc[2]
        
        earnAlloc = np.zeros((self.years,self.numAcc))
        
        for n in range(self.years):
            for m in range(self.numAcc):
                if m == 0:                                                      # High Dividend
                    earnAlloc[n,m] = rand.normalvariate(4.0,0.5)
                elif m == 1:                                                    # Long Term, Low Volatility
                    earnAlloc[n,m] = rand.normalvariate(8.0,2.5)
                elif m == 2:                                                    # Large Capital
                    earnAlloc[n,m] = rand.normalvariate(12.0,4.5)
                elif m == 3:                                                    # Short Term, High Volatility
                    earnAlloc[n,m] = rand.normalvariate(16.0,8.0)
                    if earnAlloc[n,m] > 30:
                        earnAlloc[n,m] = 30
                elif m == 4 or m == 5:                                          # Retirement (Roth/Traditional)                    
                    muStart = 7.0
                    muEnd = 4.0
                    
                    mu = muStart - ((n / self.years) * (muStart - muEnd))
                    sigma = 0.35 * mu
                    
                    earnAlloc[n,m] = rand.normalvariate(mu,sigma)
                elif m == 6:                                                    # College 529
                    muStart = 7.0
                    muEnd = 5.0
                    
                    mu = muStart - ((n / self.years) * (muStart - muEnd))
                    sigma = 0.25 * mu
                    
                    earnAlloc[n,m] = rand.normalvariate(mu,sigma)
                elif m == 7:                                                    # Emergency Funds
                    earnAlloc[n,m] = 0.05
                elif m == 8:                                                    # Long Term Savings
                    earnAlloc[n,m] = 2.25
                elif m == 9:                                                    # Short Term Savings
                    earnAlloc[n,m] = 1.0
                elif m == 10:                                                   # Excess Spending
                    earnAlloc[n,m] = 0.05
                
        earnAlloc = earnAlloc / 100
        
        self.earnAlloc = earnAlloc
        
    def savingsContCalc(self):
        
        #0) hiDiv
        #1) ltLowVol
        #2) largeCap
        #3) stHiVol
        
        #4) retRoth401
        #5) retTrad401
        
        #6) col529      - totalCollege[5]
        
        #7) emergFunds  - totalRand[9]
        #8) longTerm    - totalHouse[3] + totalWed[6] + totalLoan[10]
        #9) shortTerm   - totalAuto[4] + totalVac[7] + totalChar[8]
        #10) excSpend   - totalHol[0] + totalEnt[1] + totalMisc[2]
        
        def overFlow(indFrom,indTo,maxVal):
            """indFrom = Account Index
               indTo = [[Account Index, Percent of Transfer]]
               maxVal = Maximum Savings"""
               
            if savTotal[n,indFrom] > maxVal:
                transferVal = savTotal[n,indFrom] - maxVal
                savTotal[n,indFrom] = maxVal
                
                for ind in indTo:
                    savTotal[n,ind[0]] = savTotal[n,ind[0]] + (transferVal * ind[1])
                
        def underFlow(indUnder,indComp):
            """indUnder = Account Index
               indComp = [[Account Index, Percent of Transfer]]"""
               
            if savTotal[n,indUnder] < 0:
                transferVal = -savTotal[n,indUnder]
                savTotal[n,indUnder] = 0
                
                for ind in indComp:
                    savTotal[n,ind[0]] = savTotal[n,ind[0]] - (transferVal * ind[1])
                    
        savCont= np.zeros((self.years,self.numAcc))
        savTotal = np.zeros((self.years,self.numAcc))
        
        for n in range(self.years):
            for m in range(self.numAcc):
                #Contributions
                savCont[n,m] = self.savAlloc[n,m] * self.netCash[n]
                
                if n == 0:
                    savTotal[n,m] = savCont[n,m] + self.baseSav[m]
                else:
                    savTotal[n,m] = savTotal[n-1,m] + savCont[n,m]
                    
                if m == 4:
                    savTotal[n,m] = savTotal[n,m] + self.netRet[1][n]
                elif m == 5:
                    savTotal[n,m] = savTotal[n,m] + self.netRet[0][n] + self.netRet[2][n]
                
                #Expenses
                if m == 6:
                    savTotal[n,m] = savTotal[n,m] - self.totalExp[5][n]
                elif m == 7: 
                    savTotal[n,m] = savTotal[n,m] - self.totalExp[9][n]
                elif m == 8:
                    savTotal[n,m] = savTotal[n,m] - self.totalExp[3][n] - self.totalExp[6][n] - self.totalExp[10][n]
                elif m == 9:
                    savTotal[n,m] = savTotal[n,m] - self.totalExp[4][n] - self.totalExp[7][n] - self.totalExp[8][n]
                elif m == 10:
                    savTotal[n,m] = savTotal[n,m] - self.totalExp[0][n] - self.totalExp[1][n] - self.totalExp[2][n]
                
                #Earnings
                savTotal[n,m] = savTotal[n,m] * (1 + self.earnAlloc[n,m])
                        
            #Transfers
            overFlow(10,[[9,1]],50e3)                               #Excessive --> Short Term
            overFlow(9,[[8,1]],50e3)                                #Short Term --> Medium Term
            
            overFlow(3,[[2,0.8],[8,0.2]],5e6)                       #Short Term --> Large Capital / Long Term Savings
            overFlow(2,[[1,0.9],[8,0.1]],5e6)                       #Large Capital --> Long Term, Low Volatility / Long Term Savings
            overFlow(1,[[0,0.9],[8,0.1]],2.5e6)                     #Long Term, Low Volatility --> High Dividend / Long Term Savings
            overFlow(0,[[7,0.1],[8,0.4],[9,0.2],[10,0.3]],2.5e6)    #High Dividend --> Emergency Funds / Long Term Savings / Short Term Savings / Excess Spending
            
            underFlow(6,[[8,1]])                                    #College (Negative)    
            if n > 20 and self.childAges[n,-1] == 0:  
                overFlow(6,[[8,1]],0)                               #College (Excess)
        
        self.savTotal = savTotal
        self.savCont = savCont
        
    def savRun(self):
        self.numAcc = np.shape(self.alloc)[0]
        
        self.netCash = np.sum(self.var['netCash'],axis=1)
        
        self.netRet = []
        for ret in self.var['netRet']:
            self.netRet.append(np.sum(ret,axis=1))
        
        self.savingsAllocCalc()
        self.investCalc()
        self.savingsContCalc()
        
        self.netWorth = np.sum(self.savTotal,axis=1)