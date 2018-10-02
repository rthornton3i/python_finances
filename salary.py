import main

import numpy as np
import random as rand
import matplotlib.pyplot as plt

salaryGrowthRate = .028
salaryMax = main.salaryBase * (1 + salaryGrowthRate) ** main.years

salary = np.zeros((main.years,1))

for n in range(main.years):
    dev = 0
    rMin = 1 - dev
    rMax = 1 + dev
    r = rMin + (rMax - rMin) * rand.random()

    if main.growth == 1:
        randFactor = rand.randint(75,95)/100
        initialValueFactor = (salaryMax / main.salaryBase) * (main.years / 5)
        growthFactor = np.log(((1 / .95) - 1) / initialValueFactor) / ((-randFactor) * main.years)

        rMin = rMin * growthFactor
        rMax = rMax * growthFactor
        r = rMin + (rMax - rMin) * rand.random()

        salary[n] = (((salaryMax - main.salaryBase) / (1 + (initialValueFactor * np.exp(-r * n)))) + main.salaryBase) - (((main.years - n) / main.years) * 0.075 * main.salaryBase)
    elif main.growth == 2:
        salary[n] = ((((salaryMax - main.salaryBase) / main.years) * r) * n) + main.salaryBase
    elif main.growth == 3:
        salary[n] = main.salaryBase * (1 + r * salaryGrowthRate) ** n
    elif main.growth == 4:
        salary[n] = (main.salaryBase + (1 - np.exp(-n * r * salaryGrowthRate)) * salaryMax)
        
#plt.clf()
#plt.plot(salary)