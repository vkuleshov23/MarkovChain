import networkx as nx
from matplotlib import pyplot as plt
from itertools import combinations 


R = 7 # вершины
R1 = 10 # ребра
vb = 3 # начало
ve = 6 # конец

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
	return (x1*(1-k) + x2*k)*(1-k) + (x3*(1-k)+x4*k)*k

def create_all_combinaties(G):
	spisok = []
	for i in range(R1 + 1):
		spisok.append(list(combinations(list(G.edges), i)))
	return spisok

def getPG(g_from_all_combinates, edge, N):
	pG = nx.Graph()
	pG.add_nodes_from(N)
	for l in range(len(g_from_all_combinates[edge])):
		pG.add_edge(g_from_all_combinates[edge][l][0], g_from_all_combinates[edge][l][1])
	return pG

def calculate_sum(k, pG, start, end):
	sum1 = 0
	if nx.has_path(pG, vb, ve):
		sum1 = k**pG.number_of_edges() * (1 - k)**(R1 - pG.number_of_edges())
	return sum1

def broot_force(k, start, end):
	N = [i + 1 for i in range(R)]
	G = graph(N)
	compinaties = create_all_combinaties(G)
	SUM = 0
	for combination in compinaties:
		for edge in range(len(combination)):
			pG = getPG(combination,edge,N)
			SUM += calculate_sum(k, pG, vb, ve)
	return SUM

if __name__ =="__main__":
	summ = []
	P = []
	p = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
	for k in p:
		P.append(calculate_prop(k))
		summ.append(broot_force(k, vb, ve))
	for o in range(len(p)):
		print(str(p[o]) + " : " + str(P[o]) + " : " + str(summ[o]))

	_, ax = plt.subplots()
	ax.plot(p, P)
	ax.plot(p, summ)
	plt.show()