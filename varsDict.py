import numpy as np

var = {
    'filing':{
        'filingType':'SEPARATE',
        'filingState':['NJ','MD']},

    'years':40,
    'salary':{
        'salaryBase':[77000,83000]},
    
    'children':{
        'childYrs':[7,9],
        'familyKids':[6,8,10,10,12,13,14]},
    
    'loans':{
        'collegeLoan':np.array([0,8,4.0,36700]),
        'lawLoan':np.array([0,8,4.0,150000])},
    
    'cars':{
        'purYr':[0,0,8,10,16,18,23,25,26,27,33,35],
        'sellYr':[8,10,16,18,26,27,27,29,33,35,40,40],
        'amt':[23500,19500,25000,25000,30000,30000,22500,22500,40000,40000,45000,45000],
        'down':[5000,4000,5000,7500,10000,12500,5000,5000,15000,15000,17500,20000]},
        #Rich, Becca, Crossover1, Sedan1, Crossover2, Sedan2, Child1, Child2, Sedan3a, Sedan3b, Sedan4a, Sedan4b
    
    'housing':{
        'rent':{
            'rentYr':[0,6],
            'rentPerc':[0.12,0.15,0.15,0.15,0.175,0.175,0.175]},
        'house':{
            'purYr':[7,18,33],
            'term': [30,30,10],
            'int':  [4.25,4,3.25],
            'prin': [400e3,850e3,3e6],
            'down': [20,20,20]}},
    
    'baseSavings':np.asarray([[700],                    #hiDiv      (VYM)
                              [700],                    #ltLowVol   (VTI)
                              [700],                    #largeCap   (MGK)
                              [5500],                   #stHiVol    (Robinhood)
                              [3300 + 20000],           #retRoth401 (Fidelity, TBD, Vanguard)
                              [0],                      #retTrad401 (Fidelity)
                              [400],                    #col529     (Fidelity)
                              [1000],                   #emergFunds (PNC Short)
                              [6500 + 20000 + 20000],   #longTerm   (Goldman Sach's, BoA, Vanguard)
                              [1500 + 5000],            #shortTerm  (PNC Growth, BoA)
                              [1000]]),                 #excSpend   (PNC Spend)
                              
    
                             #[yr 0 , yr 10 , yr 20 , yr 30 , yr 40 ]
    'allocations':np.asarray([[2.5  , 2.5  , 2.5  , 7.5  , 5    ],     #hiDiv
                              [2.5  , 2.5  , 5    , 7.5  , 5    ],     #ltLowVol
                              [2.5  , 2.5  , 5    , 7.5  , 2.5  ],     #largeCap
                              [5    , 5    , 10   , 2.5  , 2.5  ],     #stHiVol
                              [0    , 0    , 0    , 0    , 0    ],     #retRoth401
                              [0    , 0    , 0    , 0    , 0    ],     #retTrad401
                              [0    , 2.5  , 12.5 , 0    , 0    ],     #col529
                              [5    , 5    , 5    , 2.5  , 15   ],     #emergFunds
                              [37.5 , 52.5 , 7.5  , 32.5 , 30   ],     #longTerm
                              [25   , 10   , 22.5 , 25   , 25   ],     #shortTerm
                              [20   , 17.5 , 30   , 15   , 15   ]])    #excSpend
}