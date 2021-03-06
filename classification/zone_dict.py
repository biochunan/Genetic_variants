def mut_zone(arg1,arg2,arg3):

	# FORMING THE DICTIONARY ELEMENT OF MUTATION ZONE

	"""
	D[$pdbchain] = [($resname(wildtype),$resname(mutant),$resid(wildtype),$resid(mutant) .........]

	"""
	
	f = open("{}".format(arg1),"r")
	ft = f.readlines()
	f.close()

	m = open("{}".format(arg2),"r")
	mt = m.readlines()
	m.close()

	g = open("{}".format(arg3),"r")
	gt = g.readlines()
	g.close()
	
	h = open("zone_dict.txt","w")

	zone = dict()
	k = 234
	while k < 235: #len(ft):
		ft1 = ft[k].split(",")
		t1 = ft1[0]

		mt1 = mt[k].split(",")
	
		print("{} :: {} of {}".format(t1,k,len(ft)))

		k1 = 1
		while k1 < len(ft1):
			list1 = []
			t2 = ft1[k1].strip("\n")
			mut = t2[1:(len(t2)-1)]
	
			# WILDTYPE
			k2 = 0
			gt1 = gt[k2].split(",")
			t3 = gt1[0].strip("\n") # PDB CHAIN
			k2 = k2 + 1
			gt1 = gt[k2].split(",")
			t4 = gt1[0].strip("\n")	# MUTATION POSITION
			count1 = 0
			while t3 != t1 or t4 != mut:
				k2 = k2 + 1
				gt1 = gt[k2].split(",")
				z = gt1[0].strip("\n")
				if k2 >= (len(gt)-1):
					count1 = count1 + 1
					break
				k2 = k2 + 1
				gt1 = gt[k2].split(",")
				t3 = gt1[0].strip("\n")
				k2 = k2 + 1
				gt1 = gt[k2].split(",")
				t4 = gt1[0].strip("\n")

			# MUTANT

			M = mt1[k1].strip("\n")
			k3 = 0
			gt1 = gt[k3].split(",")
			t3 = gt1[0].strip("\n") # PDB CHAIN
			k3 = k3 + 1
			gt1 = gt[k3].split(",")
			t4 = gt1[0].strip("\n")	# MUTATION POSITION
			count2 = 0
			
			while t3 != M or t4 != mut:
				k3 = k3 + 1
				gt1 = gt[k3].split(",")
				z = gt1[0].strip("\n")
				if k3 >= (len(gt)-1):
					count2 = count2 + 1
					break
				k3 = k3 + 1
				gt1 = gt[k3].split(",")
				t3 = gt1[0].strip("\n")
				k3 = k3 + 1
				gt1 = gt[k3].split(",")
				t4 = gt1[0].strip("\n")

			if count1 == 0 and count2 == 0: 
				z1 = gt[k2 + 1].strip("\n") # WILDTYPE
				res1 = gt[k2].strip("\n")
				z2 = gt[k3 + 1].strip("\n")	# MUTANT
				res2 = gt[k3].strip("\n")
				if "{}".format(t1) in zone.keys():
					list1 = (z1,z2,res1,res2)
					zone["{}".format(t1)].append(list1)
				else:
					list1 = [(z1,z2,res1,res2)]
					zone["{}".format(t1)] = list1
			elif count1 == 0 and count2 != 0:
				z1 = gt[k2 + 1].strip("\n") # WILDTYPE
				res1 = gt[k2].strip("\n")
				z2 = "NOT_FOUND"	# MUTANT
				res2 = "NOT_FOUND"
				if "{}".format(t1) in zone.keys():
					list1 = (z1,z2,res1,res2)
					zone["{}".format(t1)].append(list1)
				else:
					list1 = [(z1,z2,res1,res2)]
					zone["{}".format(t1)] = list1
			elif count1 != 0 and count2 == 0:
				z1 = "NOT_FOUND"	# WILDTYPE
				res1 = "NOT_FOUND"
				z2 = gt[k3 + 1].strip("\n") # MUTANT
				res2 = gt[k3].strip("\n")
				if "{}".format(t1) in zone.keys():
					list1 = (z1,z2,res1,res2)
					zone["{}".format(t1)].append(list1)
				else:
					list1 = [(z1,z2,res1,res2)]
					zone["{}".format(t1)] = list1
			elif count1 != 0 and count2 != 0:
				z1 = "NOT_FOUND"	# WILDTYPE
				res1 = "NOT_FOUND"
				z2 = "NOT_FOUND"	# MUTANT
				res2 = "NOT_FOUND"
				if "{}".format(t1) in zone.keys():
					list1 = (z1,z2,res1,res2)
					zone["{}".format(t1)].append(list1)
				else:
					list1 = [(z1,z2,res1,res2)]
					zone["{}".format(t1)] = list1

			k1 = k1 + 1
		k = k + 1

	h.write("{}".format(zone))
	h.close()

mut_zone("number_of_distinct_mutations.csv","number_of_distinct_mutants.csv","zone.txt")

