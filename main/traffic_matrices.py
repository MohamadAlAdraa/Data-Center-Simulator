#!/usr/bin/python
import random

path = "/home/mohamad/simulation/lib/results/"

def save_traffic_matrix(senders, receivers, tm):
    of = open(path+"traffic_" + tm + ".txt", 'a')
    for i in senders:
    	of.write(str(i)) 
    	of.write(" ")
    of.write("\n")
    for j in receivers:
        of.write(str(j))
        of.write(" ")
    of.write("\n")
    
def load_traffic_matrix(it, topo, tm): #grp
    of = open(path+"traffic_" + tm + ".txt", 'r')
    lines = of.readlines()
    #senders = list(topo.hosts())
    senders = []
    receivers = []
    grouped_traffic_matrices = [lines[n:n+2] for n in range(0, len(lines), 2)]
    for i in grouped_traffic_matrices[it-1][0].split(" "):
        senders.append(i.strip("\n"))
    for j in grouped_traffic_matrices[it-1][1].split(" "):
        receivers.append(j.strip("\n"))
    senders.pop()
    receivers.pop()
    print senders
    print receivers
    return senders, receivers

def random_permutation(net, topo):
    senders = list(topo.hosts())
    
    b= True
    while b:
        temp_receivers = list(topo.hosts())
        random.shuffle(temp_receivers)
        b = False
        for i in range(len(senders)):
            if senders[i] == temp_receivers[i]:
                b = True
                break
    save_traffic_matrix(senders, temp_receivers, "rp")
    return senders, temp_receivers


def random_shuffle(net, topo):
    hosts = list(topo.hosts())
    random.shuffle(hosts)
    senders = hosts[0:len(hosts):2]
    random.shuffle(senders)
    receivers = hosts[1:len(hosts):2]
    random.shuffle(receivers)
    save_traffic_matrix(senders, receivers, "rs")
    return senders, receivers

def big_and_small(net, topo):
    hosts = list(topo.hosts())
    random.shuffle(hosts)
    senders = hosts[0:len(hosts):2]
    random.shuffle(senders)
    receivers = hosts[1:len(hosts):2]
    random.shuffle(receivers)
    save_traffic_matrix(senders, receivers, "bas")
    return senders, receivers

def one_to_many(h):
    hosts = list(h)
    s = 4
    s_h = random.sample(hosts, k=s)
    senders = []
    r = 5
    for i in range(s):
        for j in range(r):
            senders.append(s_h[i])
    for i in s_h:
        hosts.remove(i)
    receivers = []
    for i in range(s):
        r_h = random.sample(hosts, k=r)
        for j in r_h:
            hosts.remove(j)
        for k in r_h:
            receivers.append(k)
    save_traffic_matrix(senders, receivers, "otm")
    return senders, receivers

'''def many_to_one(h):
    hosts = list(h)
    s = 5
    senders = []
    r = 1
    for i in range(r):
        s_h = random.sample(hosts, k=s)
        for j in range(s):
            senders.append(s_h[j])
        for k in s_h:
            hosts.remove(k)
    receivers = []
    r_h = random.sample(hosts, k=r)
    for j in r_h:
        for i in range(s):
            receivers.append(j)
    print(hosts)
    print(senders)
    print(receivers)
    save_traffic_matrix(senders, receivers, "mto")
    return senders, receivers'''

