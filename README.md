# Data-Center-Simulator
This project uses Mininet simulator and POX controller to simulate DC networks. It is compatible with any Switch based DC topologies. Each topology should be represented
as an adjacency list, then the file will be parsed and the Mininet topology will be created. Please note that you should run the POX controller separately. You can refer to
scripts to see some examples.

# Routing
I have implemented two different routing algorithms:
- K-shortest path routing.
- ECMP routing use 5-tuple hash.
These routing alogirthms are implemented in a dynamic way. In other words, the created topology in Mininet will be taken directly by the POX controller to configure all
the routing tables correspond to this specific topology.

# Traffic generator
I did integrate three traffic generators:
- Iperf
- Mgen
- HTTP
Therefore, you can conduct various experiments on the topology (tcp, udp, http) traffic.

# Measure metrics
For sure, any network metric can be measured, but you have to coded yourself. However, I focused on two only:
- Flow completion time
- Throughput

Reach out if you need help!
