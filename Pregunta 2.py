import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def FunctionInstance():
    return (np.random.uniform(0,1)*(7/4))**(4/7)


N = 1000000
x = np.zeros(N)
for i in range(N):
    x[i] = FunctionInstance()

sns.distplot(x, hist=True, kde=True, 
             bins=int(180/5), color = 'darkblue', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4})

plt.xlabel("Values")

plt.ylabel("Frequency")
plt.title("Histogram")
plt.show()

           
