import numpy as np

var = {
    'filing':'SEPARATE',
    'filingState':['NJ','MD'],

    'years':40,
    'childYrs':[7,9],
    'salaryBase':[77000,83000],
    
    'familyKids':[6,8,10,10,12,13,14],

    'collegeLoan':np.array([0,8,4.0,36700]),
    'lawLoan':np.array([0,8,4.0,150000]),
    
    'cars':np.array([[0  , 8  , 23500 , 5000  ],        #Rich
                     [0  , 10 , 19500 , 4000  ],        #Becca
                     [8  , 16 , 25000 , 5000  ],        #Crossover1
                     [10 , 18 , 25000 , 7500  ],        #Sedan1
                     [16 , 26 , 30000 , 10000 ],        #Crossover2
                     [18 , 27 , 30000 , 12500 ],        #Sedan2
                     [23 , 27 , 22500 , 5000  ],        #Child1
                     [25 , 29 , 22500 , 5000  ],        #Child2
                     [26 , 33 , 40000 , 15000 ],        #Sedan3a
                     [27 , 35 , 40000 , 15000 ],        #Sedan3b
                     [33 , 40 , 45000 , 17500 ],        #Sedan4a
                     [35 , 40 , 45000 , 20000 ]]),      #Sedan4b
    
    'rent':[0,6],
    'houses':np.array([[6,30,4.25,450000,20],
                       [18,30,4,850000,20],
                       [33,10,3.25,3000000,20]]),
    
    'baseSavings':np.asarray([[700],                #hiDiv      (VYM)
                              [700],                #ltLowVol   (VTI)
                              [700],                #largeCap   (MGK)
                              [5500],               #stHiVol    (Robinhood)
                              [3300 + 40000],       #retRoth401 (Fidelity, TBD)
                              [0],                  #retTrad401 (Fidelity)
                              [400],                #col529     (Fidelity)
                              [1000],               #emergFunds (PNC Short)
                              [6500 + 35000],       #longTerm   (Goldman Sach's, BoA)
                              [1800 + 2000],        #shortTerm  (PNC Growth, BoA)
                              [1000]]),             #excSpend   (PNC Spend)
                              
    
                             #[yr 0 , yr 10 , yr 20 , yr 30 , yr 40 ]
    'allocations':np.asarray([[2.5  , 2.5   , 2.5   , 7.5   , 5     ],     #hiDiv
                              [5    , 2.5   , 2.5   , 7.5   , 5     ],     #ltLowVol
                              [5    , 2.5   , 2.5   , 7.5   , 2.5   ],     #largeCap
                              [7.5  , 5     , 2.5   , 2.5   , 2.5   ],     #stHiVol
                              [0    , 0     , 0     , 0     , 0     ],     #retRoth401
                              [0    , 0     , 0     , 0     , 0     ],     #retTrad401
                              [0    , 2.5   , 12.5  , 0     , 0     ],     #col529
                              [5    , 5     , 5     , 2.5   , 15    ],     #emergFunds
                              [15   , 42.5  , 22.5  , 32.5  , 30    ],     #medTerm
                              [40   , 17.5  , 25    , 25    , 25    ],     #shortTerm
                              [20   , 20    , 25    , 15    , 15    ]])    #excSpend
}