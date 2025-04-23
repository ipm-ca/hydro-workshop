import numpy as np
import matplotlib.pyplot as plt


file0 = np.loadtxt("inp")
l0    = file0[:,0]
x0    = file0[:,1]
d0    = file0[:,2]


file = np.loadtxt("out")
l2    = file[:,0]
x2    = file[:,1]
d2    = file[:,2]


plt.plot(x0,d0, '--',label='t=0')
plt.plot(x1,d1, label='t=0.2 s')
plt.plot(x2,d2, label='t=0.1 s')
plt.xlabel('x [cm]')
plt.ylabel('Density [g/cm^3]')


plt.legend()
plt.savefig('density.jpeg')
