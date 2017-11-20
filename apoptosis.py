from random import random

SIM_ITERS = 10000
NUM_STEPS = 200
APOP_THRESH = 20
def simulate_bn (adj_dict, num_nodes, init_state_old, tnf, gf): #adj_dict : node -> [[key,[(innode, state, value)]]]
	init_state = init_state_old[:]
	init_state[37] = 0
	init_state[38] = tnf
	init_state[39] = gf
	last_cas3 = 0
	dna_damage_run = 0
	max_run = 0
	new_state = [0 for i in range(num_nodes)]
	t = 0
	while t<NUM_STEPS:
		for i in range(num_nodes-3):
			if i in adj_dict:
				keys = adj_dict[i]
				pos = 0
				neg = 0
				for j in range(len(keys)):
					regulation = keys[j]
					if (regulation[0]>0):
						flag = True
						for k in regulation[1]:
							if (init_state[k[0]]^k[1]==1):
								flag = False
								break
						if (flag):
							pos += regulation[1][0][2]
					elif (regulation[0]<0):
						flag = True
						for k in regulation[1]:
							if (init_state[k[0]]^k[1]==1):
								flag = False
								break
						if (flag):
							neg += regulation[1][0][2]
				if (pos==neg):
					new_state[i] = init_state[i]
				elif (pos>neg):
					new_state[i] = 1
				else:
					new_state[i] = 0
		if (last_cas3==1 and init_state[21]==1):
			new_state[37] = 1
			dna_damage_run += 1
		else:
			if (dna_damage_run>max_run):
				max_run = dna_damage_run
			new_state[37] = 0
			dna_damage_run = 0
		last_cas3 = new_state[21]
		new_state[38] = tnf
		new_state[39] = gf
		init_state = new_state[:]
		new_state = [0 for i in range(num_nodes)]
		if (dna_damage_run>=APOP_THRESH):
			max_run = dna_damage_run
			return (1, max_run)
		t += 1
	return (0, max_run)

def apoptosis_bn (network, num_nodes, removed_edges, num_iters): #network : [(node, innode, +/-, 1/0, contribution)]
	for i in removed_edges:
		network[i][2] = 0
	adj_dict = {}
	for i in network:
		if i[0] in adj_dict:
			curr = adj_dict[i[0]]
			notfound = True
			for j in range(len(curr)):
				if (curr[j][0]==i[2]):
					curr[j][1] += [(i[1],i[3],i[4])]
					notfound = False
					break
			if(notfound):
				curr += [[i[2],[(i[1],i[3],i[4])]]]
			adj_dict[i[0]] = curr
		else:
			adj_dict[i[0]] = [[i[2],[(i[1],i[3],i[4])]]]
	num_apoptosis = [0, 0, 0, 0]
	num_apop_nolethal = [0, 0, 0, 0]
	avg_nonapop_dnadamage = [0, 0, 0, 0]
	max_nonapop_dnadamage = [0, 0, 0, 0]
	num_nonapop_signal = [0, 0, 0, 0]
	p_on_lethalstates = [0 for i in range(num_nodes)]
	num_lethalstates = 0
	for i in range(num_iters):
		init_state = [0 for i in range(num_nodes)]
		for j in range(num_nodes-3):
			rd = random()
			if (rd<0.5):
				init_state[j] = 0
			else:
				init_state[j] = 1
		d00 = simulate_bn(adj_dict, num_nodes, init_state, 0, 0)
		d01 = simulate_bn(adj_dict, num_nodes, init_state, 0, 1)
		d10 = simulate_bn(adj_dict, num_nodes, init_state, 1, 0)
		d11 = simulate_bn(adj_dict, num_nodes, init_state, 1, 1)
		num_apoptosis[0] += d00[0]
		num_apoptosis[1] += d01[0]
		num_apoptosis[2] += d10[0]
		num_apoptosis[3] += d11[0]
		if (d00[0]==0):
			avg_nonapop_dnadamage[0] += d00[1]
			num_nonapop_signal[0] += 1
			if (max_nonapop_dnadamage[0]<d00[1]):
				max_nonapop_dnadamage[0] = d00[1]
		if (d01[0]==0):
			avg_nonapop_dnadamage[1] += d01[1]
			num_nonapop_signal[1] += 1
			if (max_nonapop_dnadamage[1]<d01[1]):
				max_nonapop_dnadamage[1] = d01[1]
		if (d10[0]==0):
			avg_nonapop_dnadamage[2] += d10[1]
			num_nonapop_signal[2] += 1
			if (max_nonapop_dnadamage[2]<d10[1]):
				max_nonapop_dnadamage[2] = d10[1]
		if (d11[0]==0):
			avg_nonapop_dnadamage[3] += d11[1]
			num_nonapop_signal[3] += 1
			if (max_nonapop_dnadamage[3]<d11[1]):
				max_nonapop_dnadamage[3] = d11[1]
		if (d00[0]==1 and d01[0]==1 and d10[0]==1 and d11[0]==1):
			num_lethalstates += 1
			for k in range(num_nodes):
				if(init_state[k]==1):
					p_on_lethalstates[k] += 1
		else:
			num_apop_nolethal[0] += d00[0]
			num_apop_nolethal[1] += d01[0]
			num_apop_nolethal[2] += d10[0]
			num_apop_nolethal[3] += d11[0]
	for i in range(4):	
		num_apoptosis[i] = (num_apoptosis[i]*100.0)/num_iters
		num_apop_nolethal[i] = (num_apop_nolethal[i]*100.0)/(num_iters-num_lethalstates)
		avg_nonapop_dnadamage[i] = float(avg_nonapop_dnadamage[i])/num_nonapop_signal[i]
	for i in range(num_nodes):
		p_on_lethalstates[i] = (i+1,float(p_on_lethalstates[i])/num_lethalstates)
	return (num_apoptosis, num_apop_nolethal, num_lethalstates, avg_nonapop_dnadamage, max_nonapop_dnadamage, p_on_lethalstates)
#main

network = []
with open('network.csv') as fileobj:
    for line in fileobj:
        listing = line.split('\t')
	network += [[int(listing[0])-1, int(listing[1])-1, int(listing[2]), int(listing[3]), int(listing[4])]]
print apoptosis_bn(network, 40, [], SIM_ITERS)
