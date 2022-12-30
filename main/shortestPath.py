'''
Thanks to https://github.com/pranav93y/mininet-topology-simulation
'''


def shortestPathFunction(topo, src, dst):
    topoG = topo.g

    graphDic = {}  # empty dictionary
    for node in topoG.nodes():  # make switch dictionary without links
        graphDic[node] = {}
    for edge in topoG.edges():  # adds each link to each switch
        graphDic[edge[0]][edge[1]] = 1
        graphDic[edge[1]][edge[0]] = 1

    path = getShortestPath(graphDic, src, dst, visited=[],
                           distances={}, predecessors={})
    #print path
    dpidPath = []
    for switch in path:
        dpidPath.append(topo.id_gen(name=switch).dpid)
	
    return path


def getShortestPath(graph, src, dest, visited=[], distances={}, predecessors={}):

    if src not in graph:
        raise TypeError('The root of the shortest path tree cannot be found')
    if dest not in graph:
        raise TypeError('The target of the shortest path cannot be found')

    if src == dest:
        path = []
        pred = dest
        while pred != None:
            path.append(pred)
            pred = predecessors.get(pred, None)
        return tuple(reversed(path))

    else:
        if not visited:
            distances[src] = 0
        for neighbor in graph[src]:
            if neighbor not in visited:
                new_distance = distances[src] + graph[src][neighbor]
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = src
        visited.append(src)
        unvisited = {}
        for k in graph:
            if k not in visited:
                unvisited[k] = distances.get(k, float('inf'))
        x = 0
        x = min(unvisited, key=unvisited.get)
        return getShortestPath(graph, x, dest, visited, distances, predecessors)

