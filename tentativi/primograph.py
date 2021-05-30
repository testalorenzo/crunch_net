# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 09:49:27 2021

@author: Marco
"""

tot = pd.read_csv('C:/Users/Marco/tot_prova.csv')

startups  = tot[['Organisation', 'org_city_coo']].drop_duplicates()
investors = tot[['Investors', 'inv_city_coo' ]].drop_duplicates()
startups = startups.assign(Name = startups.Organisation, coo=startups.org_city_coo).drop(['Organisation', 'org_city_coo'], axis = 1)
investors = investors.assign(Name = investors.Investors, coo=investors.inv_city_coo).drop(['Investors', 'inv_city_coo'], axis = 1)
nodes = startups.append(investors)

nodes.index = range(len(nodes))

nodes = nodes.assign(coo = nodes.coo.str.replace('(','').str.replace(')',''))
nodes= nodes.assign(coo = nodes.coo.str.split(', '))

lats = [0]*len(nodes)
longs = [0]*len(nodes)
nodes = nodes.replace(np.nan, '-')
for i in range(len(nodes)):
    if nodes.coo[i][0] == '-' or nodes.coo[i][0] =='--': 
        lats[i] = '-'
        longs[i] = '-'
    else :
        lats[i] = nodes.coo[i][0]
        longs[i] = nodes.coo[i][1]

nodes = nodes.assign(lat = lats, long = longs)

nodes.lat = pd.to_numeric(nodes.lat, errors='coerce')
nodes.long = pd.to_numeric(nodes.long, errors = 'coerce')

keys=["Name", "Lat", "Long"]
dic = {}
for i in range(len(nodes)):
               dic[i] = {"Name": nodes.Name[i], 'Lat':nodes.lat[i], 'Long': nodes.long[i]}
    
nnodes = nodes.drop(['coo'], axis = 1)
nnodes = nnodes.Name.tolist() 
nedges = tot[['Investors', 'Organisation']]
nedges = list(zip(nedges.Investors, nedges.Organisation))

G = nx.Graph()
G.add_nodes_from(nnodes)
G.add_edges_from(nedges)
nx.info(G)
Lat= {}
Long = {}
nnodes = nodes.values.tolist()
for node in nnodes:
    Lat[node[0]] = node[2]
    Long[node[0]] = node[3]
nx.set_node_attributes(G, Lat, 'Lat')
nx.set_node_attributes(G, Long, 'Long')  
nx.write_gexf(G, "chris.gexf")
