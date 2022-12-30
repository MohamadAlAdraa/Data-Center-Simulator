import os

path1 = "/home/mohamad/simulation/lib/results/http_files/strat.txt"
path2 = "/home/mohamad/simulation/lib/results/http_files/xpander.txt"
path3 = "/home/mohamad/simulation/lib/results/http_files/jellyfish.txt"



def parse_data(path):
    of = open(path, 'r')
    lines = of.readlines()
    max_t = []
    av_t = []
    for l in lines:
        ll = l.split(" ")
        max_t.append(float(ll[0]))
        av_t.append(float(ll[1]))
    av_t1 = 0
    for i in av_t:
        av_t1 += i
    
    return max(max_t), av_t1/len(av_t)

print(parse_data(path1))
print(parse_data(path2))
print(parse_data(path3))







