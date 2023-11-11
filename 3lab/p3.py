import random
import math
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
from itertools import *

# 3 Период старения
def R_i(_lamda, t, p):
	k = len(p) # количество групп
	res = 1.0
	for i in range(k):
		res *= 1-(math.e**(-_lamda[i]*t))
	return 1-res

def R(time, p, _lamda): # Функция надежности
	res = np.zeros(len(time))
	for i in range(len(time)):
		res[i] = R_i(_lamda, time[i], p);
	return res

def exp_(r, t):
	summ = np.sum(r)
	res = summ * np.exp(-summ*t)
	if(len(r) % 2 != 0):
		res *= -1.0
	return res

def R_i_dif(_lamda, t, p):
	l = k = len(p) # количество групп
	res = 0
	for i in range(k):
		for j in combinations(_lamda, i+1):
			res += exp_(np.array(j), t)
	return res

def R_dif(time, p, _lamda):
	res = np.zeros(len(time))
	for i in range(len(time)):
		res[i] = R_i_dif(_lamda, time[i], p);
	return res

def get_max_time(_lamda):
	random_all_life_time = np.zeros(len(_lamda))
	for i in range(len(_lamda)):
		random_all_life_time[i] = (-np.log(random.random()))/_lamda[i]
	return np.max(random_all_life_time)

def get_sum_time(_lamda):
	random_all_life_time = np.zeros(len(_lamda))
	for i in range(len(_lamda)):
		random_all_life_time[i] = (-np.log(random.random()))/_lamda[i]
	return np.sum(random_all_life_time)

def T(_lamda, p, N):
	tau = np.zeros(N)
	for i in range(N):
		tau[i] = get_max_time(_lamda)
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