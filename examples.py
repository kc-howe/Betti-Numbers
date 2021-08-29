import numpy as np

from simplicial_complex import SimplicialComplex


print('BETTI NUMBERS\n')

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
print(f'3-Ball: {ball.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-sphere triangulated by the faces of a single tetrahedron.
'''
sphere = SimplicialComplex()

sphere.add_boundary_matrix(0, np.array([
    [1,1,1,1]
]))

sphere.add_boundary_matrix(1, np.array([
    [1,1,1,0,0,0],
    [1,0,0,1,1,0],
    [0,1,0,1,0,1],
    [0,0,1,0,1,1]
]))

sphere.add_boundary_matrix(2, np.array([
    [1,1,0,0],
    [1,0,1,0],
    [0,1,1,0],
    [1,0,0,1],
    [0,1,0,1],
    [0,0,1,1]
]))

# Notice this is the same construction as above but without the 3-dimensional filling

# Expected: [1,0,1]
print(f'2-Sphere: {sphere.get_betti_numbers()}')

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
print(f'Klein Bottle: {klein.get_betti_numbers()}')

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
print(f'Torus: {torus.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-dimensional mobius strip
'''

mobius = SimplicialComplex()

mobius.add_boundary_matrix(0, np.array([
    [1,1,1,1,1]
]))

mobius.add_boundary_matrix(1, np.array([
    [1,1,1,1,0,0,0,0,0,0],
    [1,0,0,0,1,1,1,0,0,0],
    [0,1,0,0,1,0,0,1,1,0],
    [0,0,1,0,0,1,0,1,0,1],
    [0,0,0,1,0,0,1,0,1,1]
]))

mobius.add_boundary_matrix(2, np.array([
    [1,1,0,0,0],
    [1,0,0,0,0],
    [0,0,0,0,1],
    [0,1,0,0,1],
    [1,0,1,0,0],
    [0,0,1,0,0],
    [0,1,0,0,0],
    [0,0,1,1,0],
    [0,0,0,1,0],
    [0,0,0,1,1]
]))

# Expected: [1,1,0]
print(f'Mobius Strip: {mobius.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-dimensional cylinder
'''

cylinder = SimplicialComplex()

cylinder.add_boundary_matrix(0, np.array([
    [1,1,1,1,1,1]
]))

cylinder.add_boundary_matrix(1, np.array([
    [1,1,1,1,0,0,0,0,0,0,0,0],
    [1,0,0,0,1,1,1,0,0,0,0,0],
    [0,1,0,0,1,0,0,1,1,0,0,0],
    [0,0,1,0,0,1,0,0,0,1,0,1],
    [0,0,0,0,0,0,1,1,0,1,1,0],
    [0,0,0,1,0,0,0,0,1,0,1,1]
]))

cylinder.add_boundary_matrix(2, np.array([
    [1,0,0,0,0,0],
    [0,0,0,0,1,0],
    [1,0,0,0,0,1],
    [0,0,0,0,1,1],
    [0,0,1,0,0,0],
    [1,1,0,0,0,0],
    [0,1,1,0,0,0],
    [0,0,1,1,0,0],
    [0,0,0,1,1,0],
    [0,1,0,0,0,0],
    [0,0,0,1,0,0],
    [0,0,0,0,0,1]
]))

# Expected: [1,1,0]
print(f'Cylinder: {cylinder.get_betti_numbers()}')


print('\nEULER CHARACTERISTIC\n')

'''
Euler characteristic computations
'''

print(f'3-Ball: {ball.euler_characteristic()}')
print(f'2-Sphere: {sphere.euler_characteristic()}')
print(f'Klein Bottle: {klein.euler_characteristic()}')
print(f'Torus: {torus.euler_characteristic()}')
print(f'Mobius Strip: {mobius.euler_characteristic()}')
print(f'Cylinder: {cylinder.euler_characteristic()}')
