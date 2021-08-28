import numpy as np

from simplicial_complex import SimplicialComplex

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

'''
Compute the Betti numbers of the 2-dimensional Klein bottle
'''

klein = SimplicialComplex()

klein.add_boundary_matrix(0, np.array([
    [1,1,1,1]
]))

klein.add_boundary_matrix(1, np.array([
    [1,1,0,1,1,0,0,0,0,0,1,1],
    [0,0,1,1,0,0,1,1,1,0,0,1],
    [0,0,0,0,1,1,0,1,1,1,1,0],
    [1,1,1,0,0,1,1,0,0,1,0,0]
]))

klein.add_boundary_matrix(2, np.array([
    [1,0,0,0,0,1,0,0],
    [0,0,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,0,0,0,0,0,0],
    [0,1,1,0,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,1,0,0,1,0,0,0],
    [0,0,0,1,0,0,1,0],
    [0,0,0,0,1,1,0,0],
    [0,0,0,0,0,1,1,0],
    [0,0,0,0,0,0,1,1]
]))

# Expected: [1,2,1]
print(f'Klein Bottle: {klein.betti_numbers()}')

'''
Compute the Betti numbers of the 2-dimensional torus
'''

torus = SimplicialComplex()

torus.add_boundary_matrix(0, np.array([
    [1,1,1,1]
]))

torus.add_boundary_matrix(1, np.array([
    [1,1,1,0,0,1,1,1,0,0,0,0],
    [1,1,0,1,1,0,0,0,1,1,0,0],
    [0,0,1,1,0,0,1,0,0,1,1,1],
    [0,0,0,0,1,1,0,1,1,0,1,1]
]))

torus.add_boundary_matrix(2, np.array([
    [1,0,0,0,0,1,0,0],
    [0,0,1,0,0,0,0,1],
    [1,0,0,1,0,0,0,0],
    [1,1,0,0,0,0,0,0],
    [0,1,1,0,0,0,0,0],
    [0,0,1,1,0,0,0,0],
    [0,0,0,0,1,0,0,1],
    [0,0,0,0,1,1,0,0],
    [0,0,0,0,0,1,1,0],
    [0,0,0,0,0,0,1,1],
    [0,1,0,0,1,0,0,0],
    [0,0,0,1,0,0,1,0]
]))

# Expected: [1,2,1]
print(f'Torus: {torus.betti_numbers()}')