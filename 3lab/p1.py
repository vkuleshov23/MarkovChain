import random
import math
import numpy as np
import numpy.random as random

# 1 Период приработки
def R_i(_lamda, t, p):
	k = len(p) # количество групп
	res = 0
	for i in range(k):
		res += (math.e**(-_lamda[i]*t))*p[i]
	return res

def R(time, p, _lamda): # Функция надежности
	res = np.zeros(len(time))
	for i in range(len(time)):
		res[i] = R_i(_lamda, time[i], p);
	return res

def R_i_dif(_lamda, t, p):
	k = len(p) # количество групп
	res = 0
	for i in range(k):
		res += (math.e**(-_lamda[i]*t))*p[i]*(-_lamda[i])
	return res

def R_dif(time, p, _lamda):
	res = np.zeros(len(time))
	for i in range(len(time)):
		res[i] = R_i_dif(_lamda, time[i], p);
	return res

def sum_propability(p):
	ps = np.zeros(len(p))
	for i in range(1, len(p)):
		ps[i] = ps[i-1]+p[i-1]
	return ps

def get_index(ps, rand_i):
	for i in range(1,len(ps)):
		if rand_i < ps[i]:
			return i-1
	return len(ps)-1

def T(_lamda, p, N):
	tau = np.zeros(N)
	rand = random.random_sample(N)
	ps = sum_propability(p)
	for i in range(N):
		index = get_index(ps, rand[i])
		tau[i] = -np.log(random.random())/_lamda[index]
	print("Srednee time: ", (np.sum(tau)/N)	)
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