# Betti Numbers

## Description
This repository computes Betti numbers of a topological space. These Betti numbers can be computed by first [triangulating](https://en.wikipedia.org/wiki/Triangulation_(topology)) the topological space by a [simplicial complex](https://en.wikipedia.org/wiki/Simplicial_complex), then representing this complex as a collection of boundary matrices, and lastly performing some reduction on these matrices. The original purpose of this repository was to programatically solve the problem of finding the Betti numbers of the 2-dimensional [Klein bottle](https://en.wikipedia.org/wiki/Klein_bottle), given as an exercise in Edelsbrunner and Harer's *Computational Topology: An Introduction*. Triangulating and finding the Betti numbers of the [dunce cap](https://en.wikipedia.org/wiki/Dunce_hat_(topology)) topological space is also given as part of a three-credit (i.e. highest difficulty) exercise, and these problems are also solved here.

### Betti Numbers
Betti numbers can be thought of as a count of p-dimensional holes in a topological space for positive dimension p. The 0th Betti number of a space is better thought of as a count of disconnected components of a space. Betti numbers are computed by finding the rank of the p-th homology group H<sub>p</sub> of a triangulating simplicial complex of a space. Such a complex can be described as a collection of boundary matrices describing the (p-1)-dimensional boundaries of each p-simplex in the simplicial complex.

### Boundary Matrices
The p-th boundary matrix of a complex is a relatively simple construct. Given a dimension p and an arbitrary indexing of the p-simplices and (p-1)-simplices of the complex, the p-th boundary matrix has **a<sub>i</sub><sup>j</sup> = 1** if the i-th (p-1)-simplex is a face of the j-th p-simplex and **a<sub>i</sub><sup>j</sup> = 0** otherwise. By computing the Smith normal form of these boundary matrices, one can easily compute the ranks of the p-th cycle groups Z<sub>p</sub> and (p-1)-th boundary groups B<sub>p-1</sub>. These appear as the zero columns and non-zero rows, respectively. If these ranks are computed for all dimensions p, then the ranks of the p-th homology groups (i.e. the Betti numbers of the space) can be computed by the differences **rank(H<sub>p</sub>) = rank(Z<sub>p</sub>) - rank(B<sub>p</sub>)**.

### Euler Characteristic
Computing the Betti numbers of a space also enables us to compute the [Euler characteristic](https://en.wikipedia.org/wiki/Euler_characteristic) of that space. By the Euler-Poincar?? theorem, the Euler characteristic of a topological space is merely the alternating sum of its Betti numbers. A few examples of Euler characteristic are given in `examples.py`.

### Reduced Betti Numbers
Reduced Betti numbers give a somewhat more intuitive and pleasing result when interpreting Betti numbers as p-dimensional holes. In brief, they are equivalent to the standard Betti numbers except in the case of p=0, where the reduced 0th Betti number is the 0th Betti number minus one. This guarantees that the 0th reduced Betti number counts gaps between disconnected vertices (i.e. 0-dimensional holes). Techinically, the procedure of reducing boundary matrices produces the reduced Betti numbers of a space. This repository stores the standard Betti numbers after a computation, however both are retrievable.

### Limitations
Unfortunately, this approach to representing topological spaces and computing their Betti numbers is untenable for large complexes, as the boundary matrices of a complex are generally sparse and quite large. A sparse-matrix implementation would yield greater efficiency for larger complexes.

## Example
To find the Betti numbers of the 3-dimensional ball, we can triangulate it with a single tetrahedron and find each p-th boundary matrix describing this tetrahedron.

<p align="center">
  <img width="300" height="300" src="images/ball-triangulation.png">
</p>

~~~
'''
Compute the Betti numbers of the 3-ball triangulated by a single tetrahedron.
'''
ball = SimplicialComplex()

# Add vertices
ball.add_boundary_matrix(0, np.array([
    [1,1,1,1]
]))

# Relate vertices (rows) to edges (columns)
ball.add_boundary_matrix(1, np.array([
    [1,1,1,0,0,0],
    [1,0,0,1,1,0],
    [0,1,0,1,0,1],
    [0,0,1,0,1,1]
]))

# Relate edges (rows) to faces (columns)
ball.add_boundary_matrix(2, np.array([
    [1,1,0,0],
    [1,0,1,0],
    [0,1,1,0],
    [1,0,0,1],
    [0,1,0,1],
    [0,0,1,1]
]))

# Relate faces (rows) to solid interior (column)
ball.add_boundary_matrix(3, np.array([
    [1],
    [1],
    [1],
    [1]
]))

# Expected: [1,0,0,0]
print(f'3-Ball: {ball.get_betti_numbers()}')
~~~

When executed, this code outputs:
~~~
3-Ball: [1, 0, 0, 0]
~~~
These are the expected Betti numbers of the 3-ball. All of the p-th Betti numbers vanish for positive p, which matches our intuition that a solid ball has no holes.

Additional examples regarding the following spaces are provided in `examples.py`:
- The 2-dimensional sphere
- The klein bottle
- The torus
- The mobius strip
- The cylinder
- The dunce cap

## Drawing Tool Instructions

The drawing tool allows a user to draw up to 2-dimensional simplicial complexes. To draw a simplicial complex:
1. Click to add vertices to the complex.
2. Click existing vertices to select them (up to 3), and press `SPACE` to add the corresponding simplex.
3. Right click to remove vertices.
4. Select vertices and press `SPACE` to remove the corresponding simplex if it already exists.
5. Press `R` to reset the drawing area.

<p align="center">
  <img width="561" height="347" src="images/drawing-tool.gif">
</p>
