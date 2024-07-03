import numpy as np

from simplicial.boundary_matrix import BoundaryMatrix

print('BETTI NUMBERS\n')

'''
Compute the Betti numbers of the 3-ball triangulated by a single tetrahedron.
'''
ball = BoundaryMatrix()

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
print(f'3-Ball:\t\t{ball.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-sphere triangulated by the faces of a single tetrahedron.
'''
sphere = BoundaryMatrix()

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
print(f'2-Sphere:\t{sphere.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-dimensional Klein bottle
'''

klein = BoundaryMatrix()

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
print(f'Klein Bottle:\t{klein.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-dimensional torus
'''

torus = BoundaryMatrix()

torus.add_boundary_matrix(0, np.array([
    [1,1,1,1,1,1,1,1,1]
]))

torus.add_boundary_matrix(1, np.array([
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,1,0],
    [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,1],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,1]

]))

torus.add_boundary_matrix(2, np.array([
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1]
]))

# Expected: [1,2,1]
print(f'Torus:\t\t{torus.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-dimensional mobius strip
'''

mobius = BoundaryMatrix()

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
print(f'Mobius Strip:\t{mobius.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-dimensional cylinder
'''

cylinder = BoundaryMatrix()

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
print(f'Cylinder:\t{cylinder.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-dimensional dunce cap

This calculation was the primary goal of this project. This was
certainly the most difficult triangulation to define the boundary
matrices for, mostly due to the number of simplices and face relations
that one must keep track of throughout the construction.
'''

dunce = BoundaryMatrix()

dunce.add_boundary_matrix(0, np.array([
    [1,1,1,1,1,1,1,1]
]))

dunce.add_boundary_matrix(1, np.array([
    [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0],
    [0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,1,1],
    [0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1]
]))

dunce.add_boundary_matrix(2, np.array([
    [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
    [0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
    [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
    [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
    [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0]
]))

# Expected: [1,0,0]
print(f'Dunce Cap:\t{dunce.get_betti_numbers()}')

print('\nEULER CHARACTERISTIC\n')

'''
Euler characteristic computations
'''

print(f'3-Ball:\t\t{ball.euler_characteristic()}')
print(f'2-Sphere:\t{sphere.euler_characteristic()}')
print(f'Cylinder:\t{cylinder.euler_characteristic()}')
print(f'Mobius Strip:\t{mobius.euler_characteristic()}')
print(f'Torus:\t\t{torus.euler_characteristic()}')
print(f'Klein Bottle:\t{klein.euler_characteristic()}')
print(f'Dunce Cap:\t{dunce.euler_characteristic()}')
