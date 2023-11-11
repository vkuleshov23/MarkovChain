from matplotlib import pyplot as plt
import numpy as np
import numpy.random as random

readyToWork = -1
sys_work = 1
sys_broke = 0

def exponential(value):
	return -np.log(random.rand())/value

def repairing(system_index, repair_team):
	for i in range(len(repair_team)):
		if repair_team[i] == system_index:
			return True
	return False

def canTakeTeam(system_index, repair_team):
	for i in range(len(repair_team)):
		if repair_team[i] == readyToWork:
			return True
	return False

def takeTeam(system_index, repair_team):
	for i in range(len(repair_team)):
		if repair_team[i] == readyToWork:
			repair_team[i] = system_index
			break
	return repair_team

def releaseTeam(system_index, repair_team):
	for i in range(len(repair_team)):
		if repair_team[i] == system_index:
			repair_team[i] = readyToWork
	return repair_team

def getState(t, del_ti, failure, recovery, state, system_index, repair_team):
	if(del_ti > t):
		if (state == sys_broke):
			if repairing(system_index, repair_team) == True:
				t += exponential(failure)
				state = sys_work
				repair_team = releaseTeam(system_index, repair_team)
			else:
				if canTakeTeam(system_index, repair_team) == True:
					repair_team = takeTeam(system_index, repair_team)
					t += exponential(recovery)
					state = sys_broke
		elif (state == sys_work):
			state = sys_broke
			if canTakeTeam(system_index, repair_team) == True:
				repair_team = takeTeam(system_index, repair_team)
				t += exponential(recovery)
			else:
				t = del_ti
	return t, state, repair_team

def isWork(systems_state):
	for i in range(len(systems_state)):
		if systems_state[i] == sys_work:
			return 1
	return 0

def repairReservationSystem(failure, recovery, time):
	repair_team = [readyToWork,readyToWork]
	systems_state = [sys_work, sys_work, sys_work]
	t = [exponential(failure), exponential(failure), exponential(failure)]
	states = np.zeros(len(time))
	for i in range(len(time)):
		for x in range(len(systems_state)):
			t[x], systems_state[x], repair_team = getState(t[x], time[i], failure, recovery, systems_state[x], x, repair_team)
		states[i] = isWork(systems_state)
	return states

def calculateCoefRepairSystem(N, time, failure, recovery):
	k = np.zeros(len(time))
	for i in range(N):
		states = repairReservationSystem(failure, recovery, time)
		for j in range(len(time)):
			k[j] += states[j]

	k_pr = k/N
	
	k_11 = m/(l+m)
	k_21 = ( (2*m*l) + (m**2) ) / ( (2*(l**2)) + (2*l*m) +(m**2))

	k_up = 1-((1-k_11)**3)
	k_low1 = (k_21 + k_11) - (k_11*k_21)
	k_low3 = 1-((1-k_21)*(1-k_11))
	k_low2 = 1-((1-k_11)**2)

	return k_pr, [k_up]*(len(k_pr)), [k_low1]*(len(k_pr)), [k_low2]*(len(k_pr))

def plot(pes, p, legends):
	for pe in pes:
		plt.plot(p, pe)
	plt.legend(legends)
	plt.grid(True)
	plt.show()


l = 1.15
m = 1.85
N = 50000


delta_t = 0.01
time = np.arange(0, 10, delta_t)

k_pr, k_up, k_low1, k_low2 = calculateCoefRepairSystem(N, time, l, m)
plot([k_pr, k_up, k_low1, k_low2], range(len(k_pr)), ["Практические результаты", "Верхняя граница", "Нижняя граница 1", "Нижняя граница 2"])