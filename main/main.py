'''
@author: Mohamad Al Adraa
@email: mohamad.y.aladraa@gmail.com
@description: Create the DC topologies using mininet. Based on the riplpox.
'''

from mininet.log import setLogLevel, info
from mininet.util import custom
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, CPULimitedHost

import sys
import os
from mgen_parser import Analysis
sys.path.append(".")
sys.path.insert(1, "/home/mohamad/simulation/lib")

from argparse import ArgumentParser
import time
from DCTopoExpanders import ExpanderTopo
from DCTopoFatTree import FatTreeTopo
from traffic_matrices import random_permutation, random_shuffle, one_to_many, save_traffic_matrix, load_traffic_matrix, big_and_small #many_to_one,
from http_exp import HTTP
from iperf_exp import start_throughput_experiment
from mgen_exp import Mgen
import networkx as nx

# Number of pods, specific for Fat-Tree
K = 4
# Queue Size (packets)
QUEUE_SIZE = 1000
# Link capacity (Mbps)
BW = 1
# Cpu fraction for the host machine
CPU = None
# Link delay (ms)
DELAY = None
# Loss (packets)
LOSS = None

HOST = custom(CPULimitedHost, cpu=CPU)
LINK = custom(TCLink, bw=BW, delay=DELAY,
              loss=LOSS, max_queue_size=QUEUE_SIZE, use_tbf=True) #, use_htb=True
 
# Topologies directory
STRAT_DIR = "/home/mohamad/simulation/lib/inputs/topologies/strat/"
JELLYFISH_DIR = "/home/mohamad/simulation/lib/inputs/topologies/jellyfish/"
XPANDER_DIR = "/home/mohamad/simulation/lib/inputs/topologies/xpander/"
RESULT_DIR = "/home/mohamad/simulation/lib/results"

resultPathForServers = "/home/mohamad/simulation/lib/results/mgen/serverfiles/"
resultPathForClients = "/home/mohamad/simulation/lib/results/mgen/clientfiles/"
clientMgenFiles = "/home/mohamad/simulation/lib/results/mgen/clientmgen/"
serverMgenFiles = "/home/mohamad/simulation/lib/results/mgen/servermgen/"


def get_traffic_matrix(net, topo, a):
    if a == 'rs':
        senders, receivers = random_shuffle(net, topo)
        return senders, receivers
    elif a == 'rp':
        senders, receivers = random_permutation(net, topo)
        return senders, receivers
    elif a == 'otm':
        h = list(topo.hosts())
        senders, receivers = one_to_many(h)
        return senders, receivers
    elif a == 'bas':
        senders, receivers = big_and_small(net, topo)       
        return senders, receivers
    '''elif a == 'mto':
        h = list(topo.hosts())
        senders, receivers = many_to_one(h)       
        return senders, receivers'''

def FatTreeNet(k=4):
    info('*** Creating the fattree topology')
    topo = FatTreeTopo(k)
    net = Mininet(topo, host=HOST, link=LINK, switch=OVSKernelSwitch,
                  controller=RemoteController, autoStaticArp=True, xterms=False)
    return net, topo


def JellyfishNet(args):
    info('*** Creating the jellyfish topology')
    topo = ExpanderTopo(JELLYFISH_DIR, args.topology_file, args.hosts_per_switch, BW)
    net = Mininet(topo, host=HOST, link=LINK, switch=OVSKernelSwitch,
                  controller=RemoteController, autoStaticArp=True, xterms=False)
    return net, topo


def XpanderNet(args):
    info('*** Creating the xpander topology')
    topo = ExpanderTopo(XPANDER_DIR, args.topology_file, args.hosts_per_switch, BW)
    net = Mininet(topo, host=HOST, link=LINK, switch=OVSKernelSwitch,
                  controller=RemoteController, autoStaticArp=True, xterms=False)
    return net, topo


def StratNet(args):
    info('*** Creating the strat topology')
    topo = ExpanderTopo(STRAT_DIR, args.topology_file, args.hosts_per_switch, BW)
    net = Mininet(topo, host=HOST, link=LINK, switch=OVSKernelSwitch,
                  controller=RemoteController, autoStaticArp=True, xterms=False) #
    return net, topo


def FatTreeTest():
    net, topo = FatTreeNet(k=K)
    # using net object we can access some methods like getNodeByName.
    # using topo object we can access the hosts by topo.hosts()
    net.start()
    #CLI(net)
    senders, receivers = get_traffic_matrix(net, topo, args.traffic_matrix)
    HTTP(senders, receivers, net)
    #net.stop()


def JellyfishTest(args):
    net, topo = JellyfishNet(args)
    # using net object we can access some methods like getNodeByName.
    # using topo object we can access the hosts by topo.hosts()
    net.start()
    #CLI(net)
    #time.sleep(5)
    #net.pingAll()
    time.sleep(2)
    senders, receivers = get_traffic_matrix(net, topo, args.traffic_matrix)
    #senders, receivers = load_traffic_matrix(int(args.index), topo, args.traffic_matrix)
    time.sleep(2)
    mgen = Mgen(net, senders, receivers, "110", clientMgenFiles, serverMgenFiles, resultPathForClients, resultPathForServers)
    mgen.startSimulation()
    '''if args.traffic_matrix == "bas":    
        HTTP(senders, receivers, net, bas=True)
    else:
        HTTP(senders, receivers, net)'''
    time.sleep(5)
    net.stop()


def XpanderTest(args):
    net, topo = XpanderNet(args)
    # using net object we can access some methods like getNodeByName.
    # using topo object we can access the hosts by topo.hosts()
    net.start()
    #CLI(net)
    #time.sleep(5)
    #net.pingAll()
    time.sleep(2)
    senders, receivers = load_traffic_matrix(int(args.index), topo, args.traffic_matrix)
    time.sleep(2)
    mgen = Mgen(net, senders, receivers, "110", clientMgenFiles, serverMgenFiles, resultPathForClients, resultPathForServers)
    mgen.startSimulation()
    '''if args.traffic_matrix == "bas":    
        HTTP(senders, receivers, net, bas=True)
    else:
        HTTP(senders, receivers, net)'''
    net.stop()

def StratTest(args):
    net, topo = StratNet(args)
    # using net object we can access some methods like getNodeByName.
    # using topo object we can access the hosts by topo.hosts()
    net.start()
    #CLI(net)
    #time.sleep(5)
    #net.pingAll()
    time.sleep(2)
    #senders, receivers = get_traffic_matrix(net, topo, args.traffic_matrix)
    senders, receivers = load_traffic_matrix(int(args.index), topo, args.traffic_matrix)
    time.sleep(2)
    #start_throughput_experiment(net, topo, senders, receivers, 1, 1, 30)
    mgen = Mgen(net, senders, receivers, "110", clientMgenFiles, serverMgenFiles, resultPathForClients, resultPathForServers)
    mgen.startSimulation()
    '''if args.traffic_matrix == "bas":    
        HTTP(senders, receivers, net, bas=True)
    else:
        HTTP(senders, receivers, net)'''
    net.stop()

if __name__ == '__main__':
    parser = ArgumentParser(description="topology")

    parser.add_argument('--fattree', dest='ft', default=False,
                        action='store_true', help='Run the fattree topology')

    parser.add_argument('--jellyfish', dest='jl', default=False,
                        action='store_true', help='Run the jellyfish topology')

    parser.add_argument('--xpander', dest='xp', default=False,
                        action='store_true', help='Run the xpander topology')

    parser.add_argument('--strat', dest='st', default=False,
                        action='store_true', help='Run the strat topology')

    parser.add_argument('-f', '--filename', dest='topology_file',
                        default='s16h16.txt', help='Topology input file')
    
    parser.add_argument('-s', '--servers', dest='hosts_per_switch',
                        default='16', help='number of hosts per switch')

    parser.add_argument('-t', '--traffic', dest='traffic_matrix',
                        default='rs', help='number of hosts per switch')

    parser.add_argument('-i', '--iter', dest='index',
                        default='1', help='number of hosts per switch')

    args = parser.parse_args()
    setLogLevel('info')

    if args.ft:
        FatTreeTest()
    elif args.jl:
        JellyfishTest(args=args)
    elif args.xp:
        XpanderTest(args=args)
    elif args.st:
        StratTest(args=args)
    else:
        info('**error** please specify the topology and the routing algorithm\n')

