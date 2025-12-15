import numpy as np
import math
import matplotlib.pyplot as plt
import random as rnd
#from scipy.stats import pearsonr

# data generation
n_sample =100
dt = np.linspace(0,10,n_sample)
y1 = np.zeros((n_sample,1),float)
y2 = np.zeros((n_sample,1),float)
for i in range(n_sample):
    y1[i] = math.exp(-5*dt[i])+0.1*rnd.random()
    if(i<40):
        y2[i] = math.exp(-10*dt[i])+0.1*rnd.random()
    else:
        y2[i] = 0.1*rnd.random()

plt.plot(y1)
plt.plot(y2)


def x_corr_moving(x,y,n_shift):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    if (n_shift>0):
        x = x[n_shift::]
        y = y[0:len(y)-n_shift]
    else:
        x = x[0:len(x)-n_shift]
        y = y[n_shift::]
    
    corr_numerator = sum((a-x_mean)*(b-y_mean) for a,b in zip(x,y))
    
    xsq = sum((a-x_mean)**2 for a in x)
    ysq = sum((a-y_mean)**2 for a in y)
    
    corr_denominator = math.sqrt(xsq*ysq)
    c_coeft = corr_numerator/corr_denominator
    print(c_coeft)
    return c_coeft

c = np.zeros((20,1),float)
for a in range(20):
    c[a]= x_corr_moving(y1,y2,a)
    
print(c)
plt.plot(c)

# scipy_corr,_ = pearsonr(y1, y2)
# print(scipy_corr)