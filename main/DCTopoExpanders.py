#!/usr/bin/python
"""
@author: Mohamad Al Adraa
@email: mohamad.y.aladraa@gmail.com
@description: Create the differnt expander DC topologies using mininet. Based on the riplpox. 
"""
import networkx as nx

from mininet.log import lg
from mininet.topo import Topo


class ExpanderNodeID(object):
    '''Topo node identifier.'''

    def __init__(self, switch_id=None, host_id=None, dpid=None, name=None):
        '''Init.

        @param switch_id
        @param host_id
        @param dpid dpid
        '''
        if name is not None:
            if name[0] == 'h':
                self.switch_id = int(name[1:])
                self.host_id = int(name[1:])
            elif name[0] == 's':
                self.switch_id = int(name[1:])
                self.host_id = 255
            self.dpid = (self.switch_id << 8) + self.host_id
        elif dpid is not None:
            self.switch_id = (dpid & 0xff00) >> 8
            self.host_id = (dpid & 0xff)
            self.dpid = dpid
        else:
            self.host_id = host_id
            self.switch_id = switch_id
            self.dpid = ((self.switch_id) << 8) + (self.host_id)

    def __str__(self):
        '''String conversion.

        @return str dpid as string
        '''
        if self.host_id == 255:
            return "s%d" % self.switch_id
        else:
            return "h%d" % self.host_id

    def name_str(self):
        '''Name conversion.

        @return name name as string
        '''
        return str(self)

    def ip_str(self):
        '''Name conversion.

        @return ip ip as string
        '''
        mid = (self.dpid & 0xff00) >> 8
        lo = self.dpid & 0xff
        return "10.0.%i.%i" % (mid, lo)

    def mac_str(self):
        mid = (self.dpid & 0xff00) >> 8
        lo = self.dpid & 0xff
        return "00:00:00:00:%02x:%02x" % (mid, lo)


class StructuredNodeSpec(object):
    '''Layer-specific vertex metadata for a StructuredTopo graph.'''

    def __init__(self, up_total, down_total, up_speed, down_speed,
                 type_str=None):
        '''Init.

        @param up_total number of up links
        @param down_total number of down links
        @param up_speed speed in Gbps of up links
        @param down_speed speed in Gbps of down links
        @param type_str string; model of switch or server
        '''
        self.up_total = up_total
        self.down_total = down_total
        self.up_speed = up_speed
        self.down_speed = down_speed
        self.type_str = type_str


class StructuredEdgeSpec(object):
    '''Static edge metadata for a StructuredTopo graph.'''

    def __init__(self, speed=1.0):
        '''Init.

        @param speed bandwidth in Gbps
        '''
        self.speed = speed


class StructuredTopo(Topo):
    '''Data center network representation for structured multi-trees.'''

    def __init__(self, node_specs, edge_specs):
        '''Create StructuredTopo object.

        @param node_specs list of StructuredNodeSpec objects, one per layer
        @param edge_specs list of StructuredEdgeSpec objects for down-links,
            one per layer
        '''
        super(StructuredTopo, self).__init__()
        self.node_specs = node_specs
        self.edge_specs = edge_specs

    def def_nopts(self, layer):
        '''Return default dict for a structured topo.

        @param layer layer of node
        @return d dict with layer key/val pair, plus anything else (later)
        '''
        return {'layer': layer}

    def layer(self, name):
        '''Return layer of a node

        @param name name of switch
        @return layer layer of switch
        '''
        return self.g.node[name]['layer']

    def isPortUp(self, port):
        ''' Returns whether port is facing up or down

        @param port port number
        @return portUp boolean is port facing up?
        '''
        return port % 2 == PORT_BASE

    def layer_nodes(self, layer):
        '''Return nodes at a provided layer.

        @param layer layer
        @return names list of names
        '''
        def is_layer(n):
            '''Returns true if node is at layer.'''
            return self.layer(n) == layer

        nodes = [n for n in self.g.nodes() if is_layer(n)]
        return nodes

    def up_nodes(self, name):
        '''Return edges one layer higher (closer to core).

        @param name name

        @return names list of names
        '''
        layer = self.layer(name) - 1
        nodes = [n for n in self.g[name] if self.layer(n) == layer]
        return nodes

    def down_nodes(self, name):
        '''Return edges one layer higher (closer to hosts).

        @param name name
        @return names list of names
        '''
        layer = self.layer(name) + 1
        nodes = [n for n in self.g[name] if self.layer(n) == layer]
        return nodes

    def up_edges(self, name):
        '''Return edges one layer higher (closer to core).

        @param name name
        @return up_edges list of name pairs
        '''
        edges = [(name, n) for n in self.up_nodes(name)]
        return edges

    def down_edges(self, name):
        '''Return edges one layer lower (closer to hosts).

        @param name name
        @return down_edges list of name pairs
        '''
        edges = [(name, n) for n in self.down_nodes(name)]
        return edges


# Topology to be instantiated in Mininet
class ExpanderTopo(StructuredTopo):
    "Jellyfish Topology."

    LAYER_EDGE = 2
    LAYER_HOST = 3

    def def_nopts(self, layer, name=None):
        '''Return default dict for a FatTree topo.

        @param layer layer of node
        @param name name of node
        @return d dict with layer key/val pair, plus anything else (later)
        '''
        d = {'layer': layer}
        if name:
            id = self.id_gen(name=name)
            # For hosts only, set the IP
            if layer == self.LAYER_HOST:
                d.update({'ip': id.ip_str()})
                d.update({'mac': id.mac_str()})
            d.update({'dpid': "%016x" % id.dpid})
        return d

    def __init__(self, DIR, filename, hosts_per_switch, bw):
        # Add default members to class.
        self.bw = bw
        self.DIR = DIR
        self.hosts_per_switch = int(hosts_per_switch)
        self.filename = filename
        self.id_gen = ExpanderNodeID
	G = nx.read_adjlist(self.DIR+self.filename)
	self.ports_per_switch_to_the_network = int(nx.diameter(G))
   	edge_specs = [StructuredEdgeSpec(bw)] * 3
    	node_specs = [StructuredNodeSpec(self.ports_per_switch_to_the_network,
                                     self.hosts_per_switch, bw, bw, 'edge'),
                  StructuredNodeSpec(1, 0, bw, None, 'host'),
                 ]
	super(ExpanderTopo, self).__init__(node_specs, edge_specs)
        self.create_topology(G, self.hosts_per_switch)

    def addHosts(self, G, hosts_per_switch):
        switches_dic = {}
        for s in G.nodes():
            switch_id = self.id_gen(int(s), 255).name_str()
            switch_opts = self.def_nopts(self.LAYER_EDGE, switch_id)
            switch = self.addSwitch(
                switch_id, protocols="OpenFlow10", **switch_opts)
            switches_dic[int(s)] = switch
            lg.debug("Adding switch: %s\n" % (switch_id))
            for h in range(hosts_per_switch):
                host_id = self.id_gen(int(str(s)+str(h+1)), int(str(s)+str(h+1))).name_str() #str(s)+
                host_opts = self.def_nopts(self.LAYER_HOST, host_id)
                host = self.addHost(host_id, **host_opts)
                self.addLink(host, switch, bw=self.bw) #
                lg.debug("Adding link: %s to %s\n" % (str(host), str(switch)))
        for e in G.edges():
            self.addLink(switches_dic.get(
                int(e[0])), switches_dic.get(int(e[1])), bw=self.bw)

    def up_nodes(self, name):
        '''Return edges one layer higher (closer to core).

        @param name name

        @return names list of names
        '''
        return [n for n in self.g[name] if self.isSwitch(n)]

    def down_nodes(self, name):
        '''Return edges one layer higher (closer to hosts).

        @param name name
        @return names list of names
        '''
        layer = self.layer(name) + 1
        nodes = [n for n in self.g[name] if self.layer(n) == layer]
        return nodes

    def create_topology(self, G, hosts_per_switch):
        self.addHosts(G, hosts_per_switch)


topos = {"exp": (lambda: ExpanderTopo())}

if __name__ == '__main__':
    pass

