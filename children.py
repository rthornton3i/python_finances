import main

import numpy as np

ageChild = np.zeros((main.years,len(main.numChild)))

for n in range(main.years):
    for m in range(len(main.numChild)):
        if n >= main.numChild[m] and n <= (main.numChild[m] + 22):
            ageChild[n,m] = n - main.numChild[m]
            
#print(np.concatenate((main.yrs,main.yearsRef,ageChild), axis=1))