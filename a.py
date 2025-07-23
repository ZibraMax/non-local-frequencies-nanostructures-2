import numpy as np
import matplotlib.pyplot as plt

l = 1


def af(rho):
    xx = rho*l
    return 1/(4*np.pi*l*(xx)**0.5)*np.exp(-(xx/l)**0.5)


def af2(rho):
    return (1/(8*np.pi*l**3))*np.exp(-rho)


# plo
x = np.linspace(0.1, 10, 100)
y = af(x)
y2 = af2(x)
plt.plot(x, y, label=r'3D Attenuation function Eringen, 1983')
plt.plot(x, y2, label=r'Bi-exponential')
plt.xlabel(r'$\rho$')
plt.ylabel(r'$A(|x-x\'|)$')
plt.legend()
plt.grid()
plt.show()
