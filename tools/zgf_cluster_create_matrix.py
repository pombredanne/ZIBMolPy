#!/usr/bin/python
# -*- coding: utf-8 -*-


from ZIBMolPy.pool import Pool
from ZIBMolPy.node import Node
from ZIBMolPy.phi  import get_phi
from ZIBMolPy.ui import userinput, Option, OptionsList

import sys

import os

import numpy as np


#===============================================================================
def main():
	
	pool = Pool()
	
	# check if create_neighbours was executed before
	assert(os.path.exists(pool.analysis_dir+"instruction-cluster.txt"))

	try:
		f = open(pool.analysis_dir+"instruction-cluster.txt")
		command = f.read()
		instructions = eval(command)
		
	except:			
		raise(Exception("Could not parse: "+pool.analysis_dir+"instruction.txt"))

	default_cluster_threshold = instructions['power']

	npz_file = np.load(pool.chi_mat_fn)
	chi_matrix = npz_file['matrix']
	node_names = npz_file['node_names']
	n_clusters = npz_file['n_clusters']
	active_nodes = [Node(nn) for nn in node_names]

	npz_file = np.load(pool.analysis_dir+"core_set_cluster.npz")
	cluster = npz_file['clustering']

	# transition matrix
	P = np.zeros(shape=(len(cluster),len(cluster)))

	
	#start calculating matrix	
	for i in range(len(cluster)):
			continue
			counter = 0
			cluster_index_i=0
			for node_index in cluster[i]:

				node = active_nodes[node_index]	

				# go through at least 3 nodes
				# and ignore nodes which have a higher chi value then default_cluster_threshold					
				if( chi_matrix[node_index][i] > default_cluster_threshold and couter>2):
					P
					continue
			
				ready_nodes = pool.where("state == 'ready' and parent!=None and parent.name=='%s'"%node_i.name)
				frameweights_of_node_i= node_i.frameweights

				for ready_node in ready_nodes:	
					weight = frameweights_of_node_i[ready_node.parent_frame_num]
					#frame_value = pool.converter.read_pdb(ready_node.pdb_fn)
					#temp_dist=(frame_value - node_i.internals).norm2()
			
					#iterate pdb files			
					for fn in os.listdir(ready_node.dir):
						if(re.match(".+.pdb",fn)):
							# add radius feature in future 
							frame_value = pool.converter.read_pdb(ready_node.dir+"/"+fn)
							#calculate distances
							temp_val=np.zeros(len(active_nodes))
							index_temp=0
							for node_temp in active_nodes:
								temp_val[index_temp]=(frame_value - node_temp.internals).norm2()
								index_temp=index_temp +1

							# which node has closest distance?
							index_j=np.argsort(temp_val)[0]
							
							#which node has highest chi value?
							cluster_index_j = np.argsort(chi_matrix[index_j][:])[len(clusters)]

							#calc P entry
							#if(temp_val[index_j] <= p_radius):	
							P[cluster_index_i,cluster_index_j] += weight*node.weight_corrected*chi_matrix[node_index][index_i]*chi_matrix[index_j][cluster_index_j]
			
					
			cluster_index_i=cluster_index_i+1
		
			
	for i in range(0,len(cluster)):
		factor = sum(P[i,:])
		P[i,:] = (1/factor) * P[i,:]

	print "Cluster :" + str(cluster)
	print "Transitionmatrix :" + str(P)
	
	np.savez(pool.analysis_dir+"p_pdb.npz", matrix=P)
		
#===============================================================================
if(__name__ == "__main__"):
	main()

#EOF

