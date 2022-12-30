import os
from argparse import ArgumentParser

path = "/home/mohamad/simulation/lib/results/http_files/logs/"
path1 = "/home/mohamad/simulation/lib/results/http_files/"

parser = ArgumentParser(description="result file name")

parser.add_argument('-f', '--filename', dest='topology_file',
                        default='strat.txt', help='Topology input file')


values = []
num_f = 0
for f in os.listdir(path):
    of = open(path+f, 'r')
    num_f += 1
    lines = of.readlines()
    if "=" in lines[-4]:
        v1 = lines[-4].split("=")
        v2 = v1[-1]
        if "m" in v2:
            v3 = v2.split("m")
            v4 = float(v3[0])*60
            v5 = float(v3[-1][:-2])
            v6 = v4+v5
            values.append(float(v6))
        else:
            v3 = v2[:-2]
            values.append(float(v3))

max_t = max(values)

s = 0
for i in values:
    s += i

av_t = s/len(values)

args = parser.parse_args()
of = open(path1+args.topology_file+".txt", 'a')
of.write(str(max_t))
of.write(" ")
of.write(str(av_t))
of.write(" ")
of.write(str(num_f))
of.write(" ")
of.write(str(len(values)))
of.write("\n")
    

