def dfs_v(Adj,s,parent,order):
    for u in Adj[s]:
        if u not in parent:
            parent[u]=s
            dfs_v(Adj,u,parent,order)
    order.append(s)

def dfs(Adj,s):
    parent={s:s}
    order=[]
    dfs_v(Adj,s,parent,order)
    return parent,order

def relax(Adj, w, d, parent, u, v, h):
    if d[h[v]] > d[h[u]] + w[(u, v)]: # better path through vertex u
        d[h[v]] = d[h[u]] + w[(u, v)] # relax edge with shorter path found
        parent[h[v]] = h[u]

def build_time(source_files, transformations, target_file):
    """
    Return milliseconds needed to build the target file, assuming 
    files not dependent on each other can be processed simultaneously.
    Input:      source | list of source file names
            transforms | list of transformations of form
                       | ([input_files], output_file, transform_time)
                target | name of target file to build
    """
    ##################
    # YOUR CODE HERE #
    ##################
    Adj={}
    w={}
    for file in source_files:
        Adj[file]=set()
    Adj[target_file]=set()
    for transformation in transformations:
        input_files=transformation[0]
        output_file=transformation[1]
        transform_time=transformation[2]
        for i in input_files:
            if i in Adj:
                Adj[i].add(output_file)
            else:
                Adj[i]=set()
                Adj[i].add(output_file)
            if output_file not in Adj:
                Adj[output_file]=set()
            w[(i,output_file)]=-transform_time
    Adj["s"]=set(source_files)
    s="s"
    for file in Adj[s]:
        w[(s,file)]=0
    #print(Adj)
    _, order = dfs(Adj, s) # run depth-first search on graph
    order.reverse() # reverse returned order
    h={}
    i=0
    for file in Adj:
        h[file]=i
        i+=1   
    d = [float('inf') for _ in Adj] # shortest path estimates d(s, v)
    parent = [None for _ in Adj] # initialize parent pointers
    d[h[s]], parent[h[s]] = 0, h[s] # initialize source
    for u in order: # loop through vertices in topo sort
        for v in Adj[u]: # loop through out-going edges of u
            relax(Adj, w, d, parent, u, v, h) # relax edge from u to v       

    return -d[h[target_file]]
