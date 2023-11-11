import p1
import p2
import p3
import numpy as np
import matplotlib.pyplot as plt

def Plot(time, practice, theory, label1, label2):
	fig, ax = plt.subplots()
	ax.plot(time, practice,marker = 'x', label = label1)
	ax.plot(time, theory, label = label2)
	plt.legend()
	plt.grid(True)
	plt.show()



p = [0.4, 0.35, 0.25]
_lamda = [0.7, 0.75, 0.8]
N = 200000
time = 5
step = time/50
dt = 0.1*step
t = np.arange(0, time, step)

it, rt = p1.intensity_theor(t, p, _lamda)
ip, rp = p1.intensity_pract(t, p, _lamda, dt, N)
Plot(t, ip, it, "practice I1", "theor I1")
Plot(t, rp, rt, "practice R1", "theor R2")

it, rt = p2.intensity_theor(t, p, _lamda)
ip, rp = p2.intensity_pract(t, p, _lamda, dt, N)
Plot(t, ip, it, "practice I2", "theor I2")
Plot(t, rp, rt, "practice R2", "theor R2")

it, rt = p3.intensity_theor(t, p, _lamda)
ip, rp = p3.intensity_pract(t, p, _lamda, dt, N)
Plot(t, ip, it, "practice I3", "theor I3")
Plot(t, rp, rt, "practice R3", "theor R3")