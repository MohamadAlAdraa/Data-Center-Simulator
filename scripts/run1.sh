#!/bin/bash

for i in 1 2 3 4 5 6
do
	for j in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
	do
		kill -9 $(ps -A | grep python | awk '{print $1}')
		sleep 2
		python pox/pox.py forwarding.DCController --topo=jellyfish,DIR=/home/mohamad/simulation/lib/inputs/topologies/jellyfish/-filename=s32.txt-hosts_per_switch=$i-bw=1 --routing=sp &
		sleep 5	
		python main.py --jellyfish -f s32.txt -s $i -t rs
		sleep 5
		echo "done.."
		echo "parsing"
		python mgen_parser.py -f jellyfish
		sleep 2
		mn -c
		kill -9 $(ps -A | grep python | awk '{print $1}')
		sleep 2
		python pox/pox.py forwarding.DCController --topo=strat,DIR=/home/mohamad/simulation/lib/inputs/topologies/strat/-filename=s32.txt-hosts_per_switch=$i-bw=1 --routing=sp &
		sleep 5	
		python main.py --strat -f s32.txt -s $i -t rs -i $j
		sleep 5
		echo "done.."
		echo "parsing"
		python mgen_parser.py -f strat
		sleep 2
		mn -c
		kill -9 $(ps -A | grep python | awk '{print $1}')
		sleep 2
		python pox/pox.py forwarding.DCController --topo=xpander,DIR=/home/mohamad/simulation/lib/inputs/topologies/xpander/-filename=s32.txt-hosts_per_switch=$i-bw=1 --routing=sp &
		sleep 5	
		python main.py --xpander -f s32.txt -s $i -t rs -i $j
		sleep 5
		echo "done.."
		echo "parsing"
		python mgen_parser.py -f xpander
		sleep 2
		mn -c
	done
	python get_mgen_result.py -f jellyfish -s $i
	python get_mgen_result.py -f xpander -s $i
	python get_mgen_result.py -f strat -s $i
	> /home/mohamad/simulation/lib/results/mgen/result/strat.txt
	> /home/mohamad/simulation/lib/results/mgen/result/jellyfish.txt
	> /home/mohamad/simulation/lib/results/mgen/result/xpander.txt
	> /home/mohamad/simulation/lib/results/traffic_rs.txt
done

