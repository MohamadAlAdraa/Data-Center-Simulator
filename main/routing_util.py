'''
@author: Mohamad Al Adraa
@email: mohamad.y.aladraa@gmail.com
based on ripl-pox
'''

from DCTopoExpanders import ExpanderTopo
from DCTopoFatTree import FatTreeTopo
from routing import shortestPathRouting, KshortestPathRouting, HashedStructuredRouting
from mininet.util import makeNumeric

TOPOS = {'fattree': FatTreeTopo, 'strat': ExpanderTopo,
         'jellyfish': ExpanderTopo, 'xpander': ExpanderTopo}
ROUTING = {'sp': shortestPathRouting, 'ksp': KshortestPathRouting, 'ecmp': HashedStructuredRouting}


def buildTopo(topo):
    topo_name, topo_params = topo.split(',')
    topo_kw_params = {}
    for s in topo_params.split("-"):
        key, val = s.split('=')
        topo_kw_params[key] = makeNumeric(val)
    print topo_kw_params
    return TOPOS[topo_name](**topo_kw_params)


def getRouting(routing, topo):
    return ROUTING[routing](topo)
