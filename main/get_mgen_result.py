import os
from argparse import ArgumentParser

def parse_data(path):
    of = open(path, 'r')
    lines = of.readlines()
    av_th = []
    av_th_ub = []
    for l in lines:
        ll = l.split(" ")
        av_th.append(float(ll[0]))
        av_th_ub.append(float(ll[1]))
    #print av_th
    #print av_th_ub
    av_t1 = 0
    for i in av_th:
        av_t1 += i
    av_t2 = 0
    for i in av_th_ub:
        av_t2 += i
    
    return av_t1/len(av_th), av_t2/len(av_th_ub)


def write_data(args):
    path = "/home/mohamad/simulation/lib/results/mgen/result/"+args.topology_file+"_final_result.txt"
    path1 = "/home/mohamad/simulation/lib/results/mgen/result/"+args.topology_file+".txt"
    v1, v2 = parse_data(path1)    
    of = open(path, 'a')
    of.write(str(args.server_num))
    of.write(" ")
    of.write(str(v1))
    of.write(" ")
    of.write(str(v2))
    of.write("\n")

parser = ArgumentParser(description="result file name")
parser.add_argument('-f', '--filename', dest='topology_file', default='strat.txt', help='Topology input file')
parser.add_argument('-s', '--server', dest='server_num', default='1', help='Topology input file')
args = parser.parse_args()

write_data(args)





