#!/usr/bin/python

''' 
@author: Mohamad Al Adraa
@email: mohamad.y.aladraa@gmail.com
based on riplpox
Thanks to https://github.com/pcostell/cs244-jellyfish
'''

import Queue
import logging
from copy import deepcopy
import random
from copy import copy
from shortestPath import shortestPathFunction


class Routing(object):

    '''Base class for data center network routing.

    Routing engines must implement the get_route() method.
    '''

    def __init__(self, topo):
        '''Create Routing object.

        @param topo Topo object from Net parent
        '''

        self.topo = topo

    def get_route(self, src, dst):
        '''Return flow path.

        @param src source host
        @param dst destination host

        @return flow_path list of DPIDs to traverse (including hosts)
        '''

        raise NotImplementedError


class shortestPathRouting(Routing):

    ''' Shortestpath routing '''

    def __init__(self, topo):
        self.topo = topo

    def get_route(
        self,
        src,
        dst,
        hash_=None,
        ):
        ''' Return flow path. No need for the hash_'''

        return shortestPathFunction(self.topo, src, dst)


class KshortestPathRouting(Routing):

    ''' Kshortestpath routing '''

    def __init__(self, topo):
        self.k = 8
        self.topo = topo
        random.seed()
        self.k_paths = dict()
        self.all_paths = dict()

    def k_shortest_paths(self, start, end):
        if (start, end) not in self.k_paths:
            self.k_paths[(start, end)] = self.find_all_paths(start, end)
        return self.k_paths[(start, end)]

    def find_all_paths(self, start, end):
        queue = Queue.Queue()
        first = [start]
        queue.put(first)
        all_paths = []

        while not queue.empty():

            path = queue.get()
            end_node = path[len(path) - 1]
            if end_node == end:
                all_paths.append(path)
                if len(all_paths) == self.k:
                    break

            up_edges = self.topo.up_edges(end_node)
            down_edges = self.topo.down_edges(end_node)
            all_edges = up_edges + down_edges
            for edge in all_edges:
                if not edge[1] in path:
                    path_copy = deepcopy(path)
                    path_copy.append(edge[1])
                    queue.put(path_copy)

        return all_paths

    def get_route(
        self,
        src,
        dst,
        hash_,
        ):

        if src == dst:
            return [src]

        paths = self.k_shortest_paths(src, dst)

        #print "paths found:\n"
        #print paths
        choice = hash_ % len(paths)
        #print hash_
        #print len(paths)
	#print choice
        path = paths[choice]
        #print "path used:\n"
        #print path

        return path


class StructuredRouting(Routing):

    def __init__(self, topo, path_choice):
        self.topo = topo
        self.path_choice = path_choice
        self.src_paths = None
        self.dst_paths = None
        self.src_path_layer = None
        self.dst_path_layer = None

    def _extend_reachable(self, frontier_layer):

        complete_paths = []

        if self.src_path_layer > frontier_layer:

            src_paths_next = {}

            # expand src frontier up

            for node in sorted(self.src_paths):

                src_path_list = self.src_paths[node]
                if not src_path_list or len(src_path_list) == 0:
                    continue
                last = src_path_list[0][-1]  # Last element on first list

                up_edges = self.topo.up_edges(last)
                if not up_edges:
                    continue
                assert up_edges
                up_nodes = self.topo.up_nodes(last)
                if not up_nodes:
                    continue
                assert up_nodes

                for edge in sorted(up_edges):
                    (a, b) = edge
                    assert a == last
                    assert b in up_nodes
                    frontier_node = b

                    # add path if it connects the src and dst

                    if frontier_node in self.dst_paths:
                        dst_path_list = self.dst_paths[frontier_node]
                        for dst_path in dst_path_list:
                            dst_path_rev = copy(dst_path)
                            dst_path_rev.reverse()
                            for src_path in src_path_list:
                                new_path = src_path + dst_path_rev
                                complete_paths.append(new_path)
                    else:
                        if frontier_node not in src_paths_next:
                            src_paths_next[frontier_node] = []
                        for src_path in src_path_list:
                            extended_path = src_path + [frontier_node]
                            src_paths_next[frontier_node].append(extended_path)
            self.src_paths = src_paths_next
            self.src_path_layer -= 1

        if self.dst_path_layer > frontier_layer:

            dst_paths_next = {}
            for node in self.dst_paths:

                dst_path_list = self.dst_paths[node]
                last = dst_path_list[0][-1]  # last element on first list

                up_edges = self.topo.up_edges(last)
                if not up_edges:
                    continue
                assert up_edges
                up_nodes = self.topo.up_nodes(last)
                if not up_nodes:
                    continue
                assert up_nodes
                for edge in sorted(up_edges):
                    (a, b) = edge
                    assert a == last
                    assert b in up_nodes
                    frontier_node = b

                    # add path if it connects the src and dst

                    if frontier_node in self.src_paths:
                        src_path_list = self.src_paths[frontier_node]
                        for src_path in src_path_list:
                            for dst_path in dst_path_list:
                                dst_path_rev = copy(dst_path)
                                dst_path_rev.reverse()
                                new_path = src_path + dst_path_rev
                                complete_paths.append(new_path)
                    else:

                        if frontier_node not in dst_paths_next:
                            dst_paths_next[frontier_node] = []
                        for dst_path in dst_path_list:
                            extended_path = dst_path + [frontier_node]
                            dst_paths_next[frontier_node].append(extended_path)

            self.dst_paths = dst_paths_next
            self.dst_path_layer -= 1
        #print complete_paths
        return complete_paths

    def get_route(
        self,
        src,
        dst,
        hash_,
        ):

        if src == dst:
            return [src]

        self.src_paths = {src: [[src]]}
        self.dst_paths = {dst: [[dst]]}

        src_layer = self.topo.layer(src)
        dst_layer = self.topo.layer(dst)

        # use later in extend_reachable

        self.src_path_layer = src_layer
        self.dst_path_layer = dst_layer

        lowest_starting_layer = src_layer
        if dst_layer > src_layer:
            lowest_starting_layer = dst_layer

        for depth in range(lowest_starting_layer - 1, -1, -1):
            paths_found = self._extend_reachable(depth)
            #print paths_found
            if paths_found:
                path_choice = self.path_choice(paths_found, src, dst,
                        hash_)
                return path_choice
        return None


class HashedStructuredRouting(StructuredRouting):

    '''Hashed Structured Routing.'''

    def __init__(self, topo):

        def choose_hashed(
            paths,
            src,
            dst,
            hash_,
            ):
            #print "paths found:\n"
            #print paths
            choice = hash_ % len(paths)
            #print hash_
            #print len(paths)
	    #print choice
            path = paths[choice]
            #print "path used:\n"
            #print path
	    return path

        super(HashedStructuredRouting, self).__init__(topo,
                choose_hashed)

