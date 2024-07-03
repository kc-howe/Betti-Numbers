from simplicial.simplex_tree import SimplexTree

'''
Computes Betti numbers of the drawn complex and returns them as a list.
'''
def recompute_betti_numbers(simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra):

    if not simplex_verts:
        return []

    vertex_aliases = {v:i for i, v in enumerate(simplex_verts)}
    
    simplex_verts = [vertex_aliases[v] for v in simplex_verts]
    simplex_edges = [sorted(vertex_aliases[v] for v in s) for s in simplex_edges]
    simplex_triangles = [sorted(vertex_aliases[v] for v in s) for s in simplex_triangles]
    simplex_tetrahedra = [sorted(vertex_aliases[v] for v in s) for s in simplex_tetrahedra]

    simplex_tree = SimplexTree()
    for v in simplex_verts:
        simplex_tree.insert_simplex(v)
    for e in simplex_edges:
        simplex_tree.insert_full_simplex(*e)
    for t in simplex_triangles:
        simplex_tree.insert_full_simplex(*t)
    for th in simplex_tetrahedra:
        simplex_tree.insert_full_simplex(*th)

    return simplex_tree.betti_numbers()