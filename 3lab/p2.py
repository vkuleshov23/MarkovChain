import random
import math
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt

# 2 Период нормального функционирования
def R_i(_lamda, t, p):
	k = len(p) # количество групп
	res = 1.0
	for i in range(k):
		res *= (math.e**(-_lamda[i]*t))
	return res

def R(time, p, _lamda): # Функция надежности
	res = np.zeros(len(time))
	for i in range(len(time)):
		res[i] = R_i(_lamda, time[i], p);
	return res

def R_i_dif(_lamda, t, p):
	k = len(p) # количество групп
	res = 1.0
	summ = np.sum(_lamda)
	res = -summ * np.exp(-summ*t)
	return res

def R_dif(time, p, _lamda):
	res = np.zeros(len(time))
	for i in range(len(time)):
		res[i] = R_i_dif(_lamda, time[i], p);
	return res

def get_min_time(_lamda):
	random_all_life_time = np.zeros(len(_lamda))
	for i in range(len(_lamda)):
		random_all_life_time[i] = (-np.log(random.random()))/_lamda[i]
	return np.min(random_all_life_time)

def T(_lamda, p, N):
	tau = np.zeros(N)
	for i in range(N):
		tau[i] = get_min_time(_lamda)
	return tau # Время жизни

def intensity_theor(t, p, _lamda):
	r = R(t, p, _lamda)
	rd = R_dif(t, p, _lamda)
	intensity = -(rd/r)
	return intensity, r

def intensity_pract(t, p, _lamda, dt, N):
	r = np.zeros(len(t))
	intensity = np.zeros(len(t))
	tau = T(_lamda, p, N)
	for i in range(len(t)):
		nt = 0
		nt_dt = 0
		for j in range(len(tau)):
			if tau[j] > t[i]:
				nt += 1
			if tau[j] > t[i] and tau[j] < t[i] + dt:
				nt_dt += 1
		r[i] = nt/N
		if nt >0:
			intensity[i] = (nt-(nt-nt_dt))/(nt*dt)
		else:
			intensity[i] = 0
	return intensity, r