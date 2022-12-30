#!/bin/bash

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=strat,DIR=/home/mohamad/simulation/lib/inputs/topologies/strat/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --strat -f s32.txt -s 3 -t rs
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f strat
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=jellyfish,DIR=/home/mohamad/simulation/lib/inputs/topologies/jellyfish/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --jellyfish -f s32.txt -s 3 -t rs -i $i
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f jellyfish
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=xpander,DIR=/home/mohamad/simulation/lib/inputs/topologies/xpander/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --xpander -f s32.txt -s 3 -t rs -i $i
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f xpander
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

python get_http_result.py > rsecmp.txt
> /home/mohamad/simulation/lib/results/http_files/jellyfish.txt
> /home/mohamad/simulation/lib/results/http_files/xpander.txt
> /home/mohamad/simulation/lib/results/http_files/strat.txt
> /home/mohamad/simulation/lib/results/traffic_rp.txt
> /home/mohamad/simulation/lib/results/traffic_rs.txt
> /home/mohamad/simulation/lib/results/traffic_bas.txt
> /home/mohamad/simulation/lib/results/traffic_otm.txt

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=strat,DIR=/home/mohamad/simulation/lib/inputs/topologies/strat/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --strat -f s32.txt -s 3 -t rp
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f strat
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=jellyfish,DIR=/home/mohamad/simulation/lib/inputs/topologies/jellyfish/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --jellyfish -f s32.txt -s 3 -t rp -i $i
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f jellyfish
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=xpander,DIR=/home/mohamad/simulation/lib/inputs/topologies/xpander/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --xpander -f s32.txt -s 3 -t rp -i $i
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f xpander
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

python get_http_result.py > rpecmp.txt
> /home/mohamad/simulation/lib/results/http_files/jellyfish.txt
> /home/mohamad/simulation/lib/results/http_files/xpander.txt
> /home/mohamad/simulation/lib/results/http_files/strat.txt
> /home/mohamad/simulation/lib/results/traffic_rp.txt
> /home/mohamad/simulation/lib/results/traffic_rs.txt
> /home/mohamad/simulation/lib/results/traffic_bas.txt
> /home/mohamad/simulation/lib/results/traffic_otm.txt

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=strat,DIR=/home/mohamad/simulation/lib/inputs/topologies/strat/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --strat -f s32.txt -s 3 -t bas
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f strat
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=jellyfish,DIR=/home/mohamad/simulation/lib/inputs/topologies/jellyfish/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --jellyfish -f s32.txt -s 3 -t bas -i $i
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f jellyfish
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=xpander,DIR=/home/mohamad/simulation/lib/inputs/topologies/xpander/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --xpander -f s32.txt -s 3 -t bas -i $i
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f xpander
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

python get_http_result.py > basecmp.txt
> /home/mohamad/simulation/lib/results/http_files/jellyfish.txt
> /home/mohamad/simulation/lib/results/http_files/xpander.txt
> /home/mohamad/simulation/lib/results/http_files/strat.txt
> /home/mohamad/simulation/lib/results/traffic_rp.txt
> /home/mohamad/simulation/lib/results/traffic_rs.txt
> /home/mohamad/simulation/lib/results/traffic_bas.txt
> /home/mohamad/simulation/lib/results/traffic_otm.txt

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=strat,DIR=/home/mohamad/simulation/lib/inputs/topologies/strat/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --strat -f s32.txt -s 3 -t otm
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f strat
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=jellyfish,DIR=/home/mohamad/simulation/lib/inputs/topologies/jellyfish/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --jellyfish -f s32.txt -s 3 -t otm -i $i
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f jellyfish
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

for i in 1 2
do
	kill -9 $(ps -A | grep python | awk '{print $1}')
	sleep 2
	python pox/pox.py forwarding.DCController --topo=xpander,DIR=/home/mohamad/simulation/lib/inputs/topologies/xpander/-filename=s32.txt-hosts_per_switch=3-bw=1 --routing=ecmp &
	sleep 5	
	python main.py --xpander -f s32.txt -s 3 -t otm -i $i
	sleep 5
	echo "done.."
	echo "parsing"
	python parser.py -f xpander
	sleep 5
	rm -r /home/mohamad/simulation/lib/results/http_files/logs/*
	rm -r /home/mohamad/simulation/lib/results/http_files/data/*
	mn -c
	kill -9 $(ps -A | grep python | awk '{print $1}')
done

python get_http_result.py > otmecmp.txt
> /home/mohamad/simulation/lib/results/http_files/jellyfish.txt
> /home/mohamad/simulation/lib/results/http_files/xpander.txt
> /home/mohamad/simulation/lib/results/http_files/strat.txt
> /home/mohamad/simulation/lib/results/traffic_rp.txt
> /home/mohamad/simulation/lib/results/traffic_rs.txt
> /home/mohamad/simulation/lib/results/traffic_bas.txt
> /home/mohamad/simulation/lib/results/traffic_otm.txt




