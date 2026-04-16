import math


class Graph:
    '''
    Undirected graph.

    Graph(n) -> empty graph on n vertices.
    '''
    def __init__(self, n : int, adj_list : list):
        self._nvertices = n
        self._adj_list = [set() for i in range(n)]
        for u in range(n):
            for v in adj_list[u]:
                if(v <= u):
                    self.add_edge(u, v)
    def add_edge(self, u : int, v : int):
        '''
        Add an edge between vertices with numbers u and v.
        '''
        if(type(u) != int or type(v) != int or
           u < 0 or u >= self._nvertices or
           v < 0 or v >= self._nvertices):
            raise ValueError('arguments must be numbers of vertices')
        if(v == u):
            raise ValueError('loops are not allowed')
        if(u not in self._adj_list[v]):
            self._adj_list[u].add(v)
            self._adj_list[v].add(u)
        else:
            raise ValueError('double edges are not allowed')
    def remove_edge(self, u : int, v : int):
        '''
        Remove an edge between vertices with numbers u and v.
        '''
        if(u in self._adf_list[v]):
            self._adj_list[u].remove(v)
            self._adj_list[v].remove(u)
        else:
            raise ValueError('edge is not in graph')
    def deg(self,v:int):
        if(type(v) != int or v < 0 or v >= self._nvertices):
            raise ValueError('argument must be a number of vertice')
        return len(self._adj_list[v])
    def _get_number_of_thickenings(self):
        res = 1
        for i in range(self._nvertices):
            res *= math.factorial(self.deg(i))
        return res
    def copy(self):
        return Graph(self._nvertices, self._adj_list)
    def connected(self):
        used = [0] * self._nvertices
        def dfs(g, v):
            for u in g.adj_list[v]:
                if(not used[u]):
                    used[u] = 1
                    dfs(u)
        dfs(0)
        for v in range(n):
            if not used[v]:
                return False
        return True
    def handles(self):
        '''
        get minimal number of handles of sphere to realize this graph
        '''
        res = Thickening(self, 0).handles()
        for i in range(1, self._get_number_of_thickenings()):
            res = min(res, Thickening(self, i).handles())
        return res
            

class Thickening:
    '''
    Oriented thickening of a graph.
    '''
    def __init__(self, g: Graph, k: int):
        '''
        Get n-th thickening of graph g (in some order)
        '''
        def get_kth_permutation(elements, k):
            n = len(elements)
            res = []
            _k=k
            for i in range(n):
                res.append(elements[k // math.factorial(n - i - 1)])
                elements.pop(k // math.factorial(n - i - 1))
                k = k % math.factorial(n - i - 1)
            return res
        if type(g) != Graph or type(k) != int:
            raise ValueError('invalid argument type')
        if k >= g._get_number_of_thickenings():
            raise ValueError('invalid argument type')
        n = g._nvertices
        self._orders = [[]] * n
        self._V = n
        self._E = 0
        for i in range(n):
            self._orders[i] = get_kth_permutation(list(g._adj_list[i]), k % math.factorial(g.deg(i)))
            k //= math.factorial(g.deg(i))
            self._E += g.deg(i)
        self._E //= 2
    def holes(self):
        '''
        Get number of boundary circles of thickening.
        '''
        n = self._V
        used = set()
        def go_round(v,pos):
            while((v,pos) not in used):
                used.add((v, pos))
                _v = self._orders[v][pos]
                _pos = (self._orders[_v].index(v)+1)%len(self._orders[_v])
                v,pos=_v,_pos
        h = 0
        for v in range(n):
            for pos in range(len(self._orders[v])):
                if((v,pos) not in used):
                    h += 1
                    go_round(v, pos)
        return h
    def handles(self):
        '''
        Minimal number of handles of sphere, needed to realize this thickening.
        '''
        return (self._E - self._V - self.holes() + 2) // 2

    def __str__(self):
        return f'Thickening, {self._orders}'
