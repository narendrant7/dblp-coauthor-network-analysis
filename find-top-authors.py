import sys
from urllib.parse import quote
import mysql.connector
import networkx as nx
import pandas as pd
import pylab as plt
import matplotlib.pyplot as plt2
import numpy as np

def get_prolific_aids(items):
        items.sort(reverse=True, key=lambda x: x[1])
        return map(lambda x: x[0], items)

def ego_graph_gen(g, id):
	bet_ego_1 = nx.ego_graph(g, id)
	pos = nx.spring_layout(g)
	nx.draw(bet_ego_1, pos, node_color='b', node_size=50, with_labels=False)
	nx.draw_networkx_nodes(g, pos, nodelist=[id], node_size=100, node_color='r')
	get_name_id = '''SELECT fullname FROM authors where aid = ''' + str(id)
	name = pd.read_sql(sql = get_name_id, con = cnx)
	filepath = './output/graphs/' + str(name.loc[0]['fullname']) + '.png'
	filename = str(name.loc[0]['fullname']) + '.png'
	plt.savefig(filepath)
	plt.close()
	print("Created " + filename)

cnx = mysql.connector.connect(user='username', password='password',
                              host='host.ip.address.here',
                              port=3306,
                              database='database_name')
cursor = cnx.cursor()

year = sys.argv[1]
number = sys.argv[2]
num_of_ego = sys.argv[3]
get_authorPairs = '''SELECT aid, cid FROM coAuthors where publYear <= ''' + year
df = pd.read_sql(sql = get_authorPairs, con = cnx)
g = nx.from_pandas_edgelist(df, 'aid', 'cid')
print("\nCoAuthor Network Created")
dens = nx.density(g)
clus = nx.average_clustering(g)
print("Network Density: %8.4f" % dens)
print("Clustering Coefficient: %8.4f" % clus)
print("No. of nodes: " + str(g.number_of_nodes()))
print("No. of edges: " + str(g.number_of_edges()))
s = sum(dict(g.degree()).values())
nnodes = g.number_of_nodes()
print("Average Degree: %8.4f \n" % (float(s) / float(nnodes)))

clo_cen = nx.closeness_centrality(g)
top_clo_cen = get_prolific_aids(list(clo_cen.items()))
top_clo_cen_list = list(top_clo_cen)[:int(number)]
top_clo_cen_set = set(top_clo_cen_list)
clo_cen_list = " ".join(str(x) for x in top_clo_cen_list).replace(' ', ', ')
get_names_clo_cen = '''SELECT fullname FROM authors where aid in ( ''' + clo_cen_list + ''' ) ORDER BY FIELD ( aid, ''' + clo_cen_list + ''' )'''
clo_cen_top100 = pd.read_sql(sql = get_names_clo_cen, con = cnx)
print("Top " + number + " prolific authors based on Closeness Centrality found")
title1 = './output/names/Closeness_' + number + '.txt'
np.savetxt(title1, clo_cen_top100.values, fmt="%s")

bet_cen = nx.betweenness_centrality(g)
top_bet_cen = get_prolific_aids(list(bet_cen.items()))
top_bet_cen_list = list(top_bet_cen)[:int(number)]
top_bet_cen_set = set(top_bet_cen_list)
bet_cen_list = " ".join(str(x) for x in top_bet_cen_list).replace(' ', ', ')
get_names_bet_cen = '''SELECT fullname FROM authors where aid in ( ''' + bet_cen_list + ''' ) ORDER BY FIELD ( aid, ''' + bet_cen_list + ''' )'''
bet_cen_top100 = pd.read_sql(sql = get_names_bet_cen, con = cnx)
print("Top " + number + " prolific authors based on Betweenness Centrality found")
title2 = './output/names/Betweenness_' + number + '.txt'
np.savetxt(title2, bet_cen_top100.values, fmt="%s")

eig_cen = nx.eigenvector_centrality(g)
top_eig_cen = get_prolific_aids(list(eig_cen.items()))
top_eig_cen_list = list(top_eig_cen)[:int(number)]
top_eig_cen_set = set(top_eig_cen_list)
eig_cen_list = " ".join(str(x) for x in top_eig_cen_list).replace(' ', ', ')
get_names_eig_cen = '''SELECT fullname FROM authors where aid in ( ''' + eig_cen_list + ''' ) ORDER BY FIELD ( aid, ''' + eig_cen_list + ''' )'''
eig_cen_top100 = pd.read_sql(sql = get_names_eig_cen, con = cnx)
print("Top " + number + " prolific authors based on Eigen Vector Centrality found")
title3 = './output/names/Eigen Vector_' + number + '.txt'
np.savetxt(title3, eig_cen_top100.values, fmt="%s")

deg_cen = nx.degree_centrality(g)
top_deg_cen = get_prolific_aids(list(deg_cen.items()))
top_deg_cen_list = list(top_deg_cen)[:int(number)]
top_deg_cen_set = set(top_deg_cen_list)
deg_cen_list = " ".join(str(x) for x in top_deg_cen_list).replace(' ', ', ')
get_names_deg_cen = '''SELECT fullname FROM authors where aid in ( ''' + deg_cen_list + ''' ) ORDER BY FIELD ( aid, ''' + deg_cen_list + ''' )'''
deg_cen_top100 = pd.read_sql(sql = get_names_deg_cen, con = cnx)
print("Top " + number + " prolific authors based on Degree Centrality found")
title4 = './output/names/Degree_' + number + '.txt'
np.savetxt(title4, deg_cen_top100.values, fmt="%s")

prolific_authid = top_bet_cen_set.intersection(top_clo_cen_set, top_eig_cen_set, top_deg_cen_set)
all_cen_list = " ".join(str(x) for x in prolific_authid).replace(' ', ', ')
get_names = '''SELECT fullname FROM authors where aid in ( ''' + all_cen_list + ''' )'''
top_authors = pd.read_sql(sql = get_names, con = cnx)
print("Common prolific authors were found\n")
np.savetxt('./output/names/Common Authors.txt', top_authors.values, fmt="%s")

top_clo_cen_list_ego = list(top_clo_cen_list)[:int(num_of_ego)]
top_bet_cen_list_ego = list(top_bet_cen_list)[:int(num_of_ego)]
top_eig_cen_list_ego = list(top_eig_cen_list)[:int(num_of_ego)]
top_deg_cen_list_ego = list(top_deg_cen_list)[:int(num_of_ego)]
top_all_ego = list(set().union(top_clo_cen_list_ego, top_bet_cen_list_ego, top_eig_cen_list_ego, top_deg_cen_list_ego))
print("No. of ego graphs: " + str(len(top_all_ego)))
[ego_graph_gen(g, x) for x in top_all_ego]
