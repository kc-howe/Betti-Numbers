# Computing Betti Numbers

## Description
This repository computes Betti numbers of a topological space by taking advantage of boundary matrices of a triangulating simplicial complex. It was written to programatically solve the problem of finding the Betti numbers of the 2-dimensional Klein bottle, given as an exercise in Edelsburnner and Harer's *Computational Topology: An Introduction*.

Betti numbers can be thought of as a count of p-dimensional holes in a topological space. They are computed by finding the rank of p-th homology group of a triangulating simplicial complex of a space. Such a complex can be described as a collection of boundary matrices describing the (p-1)-dimensional boundaries of each p-simplex in the simplicial complex.

The p-th boundary matrix of a complex is a simple construct, with **a_i,j = 1** if the i-th (p-1)-simplex is a face of the j-th p-simplex and **a_i,j = 0** otherwise. By computing the Smith normal form of these boundary matrices, one can easily compute the ranks of the p-th homology groups of the complex, i.e. the Betti numbers.

Unfortunately this approach is untenable for large complexes, as the boundary matrices of a complex  are generally sparse and quite large.

## Example

To find the Betti numbers of the 3-dimensional ball, we can triangulate it with a single tetrahedron and find each p-th boundary matrix describing this tetrahedron.

~~~
'''
Compute the Betti numbers of the 3-ball triangulated by a single tetrahedron.
'''
ball = SimplicialComplex()

ball.add_boundary_matrix(0, np.array([
    [1,1,1,1]
]))

ball.add_boundary_matrix(1, np.array([
    [1,1,1,0,0,0],
    [1,0,0,1,1,0],
    [0,1,0,1,0,1],
    [0,0,1,0,1,1]
]))

ball.add_boundary_matrix(2, np.array([
    [1,1,0,0],
    [1,0,1,0],
    [0,1,1,0],
    [1,0,0,1],
    [0,1,0,1],
    [0,0,1,1]
]))

ball.add_boundary_matrix(3, np.array([
    [1],
    [1],
    [1],
    [1]
]))

# Expected: [1,0,0,0]
print(f'3-Ball: {ball.betti_numbers()}')
~~~

When executed, this code outputs:
~~~
3-Ball: [1. 0. 0. 0.]
~~~
These are the expected Betti numbers of the 3-ball.

Another example regarding the 2-dimensional Klein bottle is given in `betti_test.py`.
