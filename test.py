import numpy as np
import matplotlib.pyplot as plt

import taxes as tax
import loans as ln
import setup

years = 40
salary = setup.salaryCalc(160000,years)

a = np.arange(10)
b = np.asarray([(index,value) if index != 4 else 20 for index,value in enumerate(a)])
print(b)