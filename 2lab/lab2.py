import networkx as nx
from matplotlib import pyplot as plt
from itertools import combinations 
import random

R = 7 # вершины
R1 = 10 # ребра
vb = 3 # начало
ve = 6 # конец
lmin = 2
lmax = 8

def graph(N):
	G = nx.Graph()
	G.add_nodes_from(N)
	G.add_edge(1,2)
	G.add_edge(1,3)
	G.add_edge(2,4)
	G.add_edge(2,7)
	G.add_edge(3,4)
	G.add_edge(3,5)
	G.add_edge(4,5)
	G.add_edge(4,6)
	G.add_edge(5,6)
	G.add_edge(6,7)
	# nx.draw(G)
	return(G)

def calculate_prop(k):
	x1 = 2*k**2 - 2*k**6 + k**8
	x2 = k**4 + ((2*k-k**2)**2) - (k**4)*((2*k-k**2)**2)
	x3 = (k**2)+(k+k**2-k**3)**2 - (k**2)*(k+k**2-k**3)**2
	x4 = (k+k+k**2-k**3 - k*(k+k**2-k**3))**2
	return (x1*(1-k) + x2*k)*(1-k) + (x3*(1-k) +x4*k)*k

def create_all_combinaties(G):
	spisok = []
	for i in range(R1 + 1):
		spisok.append(list(combinations(list(G.edges), i)))
	return spisok

def create_random_combinates(G, count, p):
	spisok = []
	for i in range(int(count)):
		spisok.append(random_comb(G, p))
	return spisok

def random_comb(G, p):
	comb = []
	for edge in G.edges:
		if random.random() < p:
			comb.append(edge)
	return comb

def getPG(g_from_all_combinates, edge, N):
	pG = nx.Graph()
	pG.add_nodes_from(N)
	for l in range(len(g_from_all_combinates[edge])):
		pG.add_edge(g_from_all_combinates[edge][l][0], g_from_all_combinates[edge][l][1])
	return pG

def getPG_model(g_from_all_combinates, N):
	pG = nx.Graph()
	pG.add_nodes_from(N)
	for l in range(len(g_from_all_combinates)):
		pG.add_edge(g_from_all_combinates[l][0], g_from_all_combinates[l][1])
	return pG

def calculate_sum(k, pG, start, end):
	sum1 = 0
	if nx.has_path(pG, vb, ve):
		sum1 = k**pG.number_of_edges() * (1 - k)**(R1 - pG.number_of_edges())
	return sum1

def has_way(k, pG, start, end, mod):
	global s_win
	sum1 = 0
	if mod == True:
		if(pG.number_of_edges() > lmax):
			return 0.5
		if(pG.number_of_edges() < lmin):
			return 0.0
	if nx.has_path(pG, vb, ve):
		s_win += 1
		sum1 = k**pG.number_of_edges() * (1 - k)**(R1 - pG.number_of_edges())
	return sum1

def broot_force(k, start, end):
	N = [i + 1 for i in range(R)]
	G = graph(N)
	combinaties = create_all_combinaties(G)
	sum1 = 0
	for combination in combinaties:
		for edge in range(len(combination)):
			pG = getPG(combination,edge,N)
			sum1 += calculate_sum(k, pG, vb, ve)
	return sum1

def getWins(win):
	if win == 0:
		return float('inf')
	return (9/(e**2 * 4))/win

def modeling(k, start, end, e, p, mod):
	global s_win
	s_win = 0
	N = [i + 1 for i in range(R)]
	G = graph(N)
	count = 9/(e**2 * 4)
	combinaties = create_random_combinates(G, count, p)
	sum1 = 0
	for combination in combinaties:
		pG = getPG_model(combination,N)
		if has_way(k, pG, vb, ve, mod) > 0.0:
			sum1 += 1
	return sum1/count

if __name__ =="__main__":
	summ_bf = []
	summ_m = []
	summ_m_fast = []
	wins = []
	e = 0.01
	P = []
	p = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
	# p = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
	for k in p:
		P.append(calculate_prop(k))
		summ_bf.append(broot_force(k, vb, ve))
		summ_m.append(modeling(k, vb, ve, e, k, False))
		summ_m_fast.append(modeling(k, vb, ve, e, k, True))
		wins.append(getWins(s_win))
	for o in range(len(p)):
		print(str(p[o]) + " : " + str(P[o]) + " : " + str(summ_bf[o]) + " : " + str(summ_m[o]) + " : " + str(summ_m_fast[o]))

	_, ax = plt.subplots()
	ax.plot(p, P)
	ax.plot(p, summ_bf)
	ax.plot(p, summ_m)
	ax.plot(p, summ_m_fast)
	plt.show()
	_, ax = plt.subplots()
	ax.plot(p, wins)
	plt.show()