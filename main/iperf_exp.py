import random

from subprocess import Popen
from multiprocessing import Process
import sys
from time import sleep
from monitor import monitor_devs_ng

SAMPLE_WAIT_SEC = 10.0
result_dir = "/home/mohamad/simulation/lib/results/iperf"

def wait(msg, seconds, granularity=10):
    sys.stdout.write(msg)
    sys.stdout.flush()
    for i in range(granularity):
        sleep(float(seconds) / granularity)
        sys.stdout.write(".")
        sys.stdout.flush()
    print "DONE"


def read_list(fname, delim=","):
    lines = open(fname).xreadlines()
    ret = []
    for l in lines:
        ls = l.strip().split(delim)
        ls = map(
            lambda e: "0"
            if e.strip() == "" or e.strip() == "ms" or e.strip() == "s"
            else e,
            ls,
        )
        ret.append(ls)
    return ret


def start_iperf_receiver(receiver, result_dir):
    receiver.popen(
        "iperf -s -p 5001 > %s/%s-server.txt"
        % (result_dir, receiver),
        shell=True,
    )


def start_iperf_sender(sender, receiver, flows, result_dir):
    print "Starting iperf from %s (%s) to %s (%s)." % (
        sender,
        sender.IP(),
        receiver,
        receiver.IP(),
    )
    sender.popen(
        "iperf -c %s -t 3600 -p 5001 -P %s -f m -i 1 > %s/%s-client.txt"
        % (receiver.IP(), str(flows), result_dir, sender),
        shell=True,
    )


def stop_iperf(node):
    node.popen("killall iperf")


def get_iface_for_host(host, topo):
    ups = topo.up_nodes(host)
    assert len(ups) == 1
    return "%s-eth%d" % (ups[0], topo.port(host, ups[0])[1])


def parse_rates(senders, topo, result_dir):
    ifaces = [get_iface_for_host(host, topo) for host in senders]
    #print senders
    #print ifaces
    data = read_list("%s/txrate.txt" % result_dir)
    total = 0.0
    n_samples = 0
    for row in data:
        try:
            ifname = row[1]
        except:
            continue
        if ifname in ifaces:
            #print "yes"
            #print row[3]
            total = float(row[3]) * 8.0 / (1 << 20)
            n_samples = n_samples + 1
    return total / n_samples


def start_throughput_experiment(net, topo, s, r, bw, flows, time):

    senders = s
    receivers = r

    for receiver in receivers:
        start_iperf_receiver(net.getNodeByName(receiver), result_dir)
    wait("Waiting for iperf servers to start", 3)

    for (sender, receiver) in zip(senders, receivers):
        start_iperf_sender(
            net.getNodeByName(sender), net.getNodeByName(receiver), flows, result_dir
        )
    wait("Letting network warm up", SAMPLE_WAIT_SEC)

    monitor = Process(target=monitor_devs_ng, args=("%s/txrate.txt" % result_dir, 0.01))
    monitor.start()

    wait("Running experiment", time)

    monitor.terminate()

    wait("Stopping monitor", 2)

    for r in receivers:
        stop_iperf(net.getNodeByName(r))

    rate = parse_rates(senders, topo, result_dir)
    f = open("%s/throughput.txt" % result_dir, "w")
    f.write("%s\n" % (rate / bw))
    f.close()
    print "The average sending rate is: %s" % rate
    print "The percent utilization is: %s" % (rate / bw)

