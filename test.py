import numpy as np
import matplotlib.pyplot as plt

import taxes as tax

years = 40
benefits = tax.benefitsCalc(years,healthPrem=200,visPrem=10,denPrem=20)

plt.clf()
plt.plot(benefits)