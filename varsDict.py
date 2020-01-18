import numpy as np

var = {
    'filing':{
        'filingType':'SEPARATE',
        'filingState':['NJ','NJ']},
    
    'years':36,
    'ages':{
        'baseAges':[25,25]},
    'salary':{
        'salaryBase':[79460,95000]},
    
    'children':{
        'childYrs':[5,7],
        'familyKids':[4,6,8,8,10,11,13]},
    
    'loans':{},
    
    'cars':{
        'purYr': [0,    0,    8,    10,   16,   18,   23,   25,   26,   27],#,   33,   35],
        'sellYr':[5,    6,    14,   16,   24,   25,   25,   27,   31,   33],#,   40,   40],
        'amt':   [10000,11000,25000,25000,30000,30000,22500,22500,40000,40000],#,45000,45000],
        'down':  [0,    0,    5000, 7500, 10000,12500,5000, 5000, 15000,15000]},#,17500,20000]},
        #Rich, Becca, Crossover1, Sedan1, Crossover2, Sedan2, Child1, Child2, Sedan3a, Sedan3b, Sedan4a, Sedan4b
    
    'housing':{
        'rent':{
            'rentYr':[0,3],
            'rentPerc':None},
        'house':{
            'purYr':[4,18,33],
            'term': [30,30,10],
            'int':  [4.25,4,3.25],
            'prin': [450e3,750e3,3e6],
            'down': [20,20,20]}},
    
    'baseSavings':np.asarray([[1700],                   #hiDiv      (VYM)
                              [800],                    #ltLowVol   (VTI)
                              [500+1100],               #largeCap   (MGK)
                              [8000],                   #stHiVol    (Robinhood)
                              [17500 + 5800],           #retRoth401 (Fidelity, TRowe)
                              [25000],                  #retTrad401 (Vanguard)
                              [900],                    #col529     (Fidelity)
                              [1800],                   #emergFunds (PNC Reserve)
                              [7500 + 56000 + 1300],    #longTerm   (Goldman Sach's, BoA, Vanguard)
                              [3300],                   #shortTerm  (PNC Growth)
                              [12000 + 6000]]),         #excSpend   (PNC Spend, BoA)
                              
    
                             #[yr 0 , yr 10, yr 20, yr 30, yr 40]
    'allocations':np.asarray([[2.5  , 2.5  , 2.5  , 7.5  , 5    ],     #hiDiv
                              [2.5  , 2.5  , 5    , 7.5  , 5    ],     #ltLowVol
                              [5    , 2.5  , 5    , 7.5  , 2.5  ],     #largeCap
                              [7.5  , 5    , 2.5  , 2.5  , 2.5  ],     #stHiVol
                              [0    , 0    , 0    , 0    , 0    ],     #retRoth401
                              [0    , 0    , 0    , 0    , 0    ],     #retTrad401
                              [0    , 2.5  , 12.5 , 0    , 0    ],     #col529
                              [5    , 5    , 5    , 2.5  , 15   ],     #emergFunds
                              [25   , 35   , 15   , 32.5 , 30   ],     #longTerm
                              [22.5 , 17.5 , 22.5 , 25   , 25   ],     #shortTerm
                              [30   , 27.5 , 30   , 15   , 15   ]])    #excSpend
}