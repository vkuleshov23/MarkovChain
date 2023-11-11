import numpy as np
import numpy.random as random
from matplotlib import pyplot as plt

def exp_(l):
	return -np.log(random.rand())/l

def getState(t, del_ti, failure, recovery, state):
	if(del_ti > t):
		if state == 1:
			t += exp_(recovery) #  до окончания этого времени система будет восстанавливаться
			state = 0
		else:
			t += exp_(failure) #  до окончания этого времени система будет работать
			state = 1
	return t, state

def repairSystemWithoutReservation(failure, recovery, time):
	state = 1
	states = np.zeros(len(time))
	t = exp_(failure) # до окончания этого времени система будет работать
	for i in range(len(time)):
		t, state = getState(t, time[i], failure, recovery, state)
		states[i] = state
	return states

def calculateCoefRepairSystemWithoutReservation(N, time, failure, recovery):
	k = np.zeros(len(time))
	for i in range(N):
		states = repairSystemWithoutReservation(failure, recovery, time)
		for j in range(len(time)):
			k[j] = k[j] + states[j]
	k_pr = k/N
	k_th = m/(l+m)
	return k_pr, [k_th]*(len(k_pr))

def plot(pes, p, legends):
	for pe in pes:
		plt.plot(p, pe)
	plt.legend(legends)
	plt.grid(True)
	plt.show()


l = 1.3
m = 1.7
delta_t = 0.01
time = np.arange(0, 10, delta_t)
N = 5000


k_pr, k_th = calculateCoefRepairSystemWithoutReservation(N, time, l, m)
plot([k_pr, k_th], range(len(k_pr)), ["k_pr", "k_th"])