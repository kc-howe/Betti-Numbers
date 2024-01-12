import numpy as np

from simplicial_complex import SparseSimplicialComplex


print('BETTI NUMBERS\n')

'''
Compute the Betti numbers of the 3-ball triangulated by a single
tetrahedron.

Bonus: We can specify vertices using any data types supported by NumPy.
'''
ball = SparseSimplicialComplex()

# Add vertices
ball.add_simplices(
    ['A', 'B', 'C', 'D']
)

# Add edges
ball.add_simplices([
    ['A', 'B'],
    ['A', 'C'],
    ['A', 'D'],
    ['B', 'C'],
    ['B', 'D'],
    ['C', 'D']
])

# Add faces
ball.add_simplices([
    ['A','B','C'],
    ['A','B','D'],
    ['A','C','D'],
    ['B','C','D']
])

# Add solids
ball.add_simplices([
    ['A','B','C','D']
])

# Expected: [1,0,0,0]
print(f'3-Ball:\t\t{ball.get_betti_numbers()}')

'''
Compute the Betti numbers of the 2-sphere triangulated by the faces of a
single tetrahedron.
'''
sphere = SparseSimplicialComplex()

# Add vertices
sphere.add_simplices(
    [0,1,2,3]
)

# Add edges
sphere.add_simplices([
    [0,1],
    [0,2],
    [0,3],
    [1,2],
    [1,3],
    [2,3]
])

# Add faces
sphere.add_simplices([
    [0,1,2],
    [0,1,3],
    [0,2,3],
    [1,2,3]
])

# Expected: [1,0,1]
print(f'2-Sphere:\t{sphere.get_betti_numbers()}')

'''
Compute the Betti numbers of the cylinder.
'''
cylinder = SparseSimplicialComplex()

# Add vertices
cylinder.add_simplices(
    [0,1,2,3,4,5]
)

# Add edges
cylinder.add_simplices([
    [0,1],
    [0,2],
    [0,3],
    [0,4],
    [1,2],
    [1,4],
    [1,5],
    [2,3],
    [2,5],
    [3,4],
    [3,5],
    [4,5]
])

# Add faces
cylinder.add_simplices([
    [0,1,4],
    [0,2,3],
    [0,3,4],
    [1,2,5],
    [1,4,5],
    [2,3,5]
])

# Expected: [1,1,0]
print(f'Cylinder:\t{cylinder.get_betti_numbers()}')

'''
Compute the Betti numbers of the mobius strip.
'''
mobius = SparseSimplicialComplex()

# Add vertices
mobius.add_simplices(
    [0,1,2,3,4,5]
)

# Add edges
mobius.add_simplices([
    [0,1],
    [0,2],
    [0,3],
    [0,4],
    [0,5],
    [1,2],
    [1,4],
    [1,5],
    [2,3],
    [2,5],
    [3,4],
    [4,5]
])

# Add faces
mobius.add_simplices([
    [0,1,4],
    [0,2,3],
    [0,2,5],
    [0,3,4],
    [1,2,5],
    [1,4,5],
])

# Expected: [1,1,0]
print(f'Mobius Strip:\t{mobius.get_betti_numbers()}')

'''
Compute the Betti numbers of the torus.
'''
torus = SparseSimplicialComplex()

# Add vertices
torus.add_simplices(
    [0,1,2,3,4,5,6,7,8]
)

# Add edges
torus.add_simplices([
    [0,1],
    [0,2],
    [0,3],
    [0,5],
    [0,6],
    [0,7],
    [1,2],
    [1,3],
    [1,4],
    [1,7],
    [1,8],
    [2,4],
    [2,5],
    [2,6],
    [2,8],
    [3,4],
    [3,5],
    [3,6],
    [3,8],
    [4,5],
    [4,6],
    [4,7],
    [5,7],
    [5,8],
    [6,7],
    [6,8],
    [7,8]
])

# Add faces
torus.add_simplices([
    [0,1,3],
    [0,1,7],
    [0,2,5],
    [0,2,6],
    [0,3,5],
    [0,6,7],
    [1,2,4],
    [1,2,8],
    [1,3,4],
    [1,7,8],
    [2,4,5],
    [2,6,8],
    [3,4,6],
    [3,5,8],
    [3,6,8],
    [4,5,7],
    [4,6,7],
    [5,7,8]
])

# Expected: [1,2,1]
print(f'Torus:\t\t{torus.get_betti_numbers()}')

'''
Compute the Betti numbers of the Klein bottle.
'''
klein = SparseSimplicialComplex()

# Add vertices
klein.add_simplices(
    [0,1,2,3,4,5,6,7,8]
)

# Add edges
klein.add_simplices([
    [0,1],
    [0,2],
    [0,3],
    [0,5],
    [0,6],
    [0,7],
    [1,2],
    [1,3],
    [1,4],
    [1,7],
    [1,8],
    [2,3],
    [2,4],
    [2,5],
    [2,8],
    [3,4],
    [3,6],
    [3,8],
    [4,5],
    [4,6],
    [4,7],
    [5,6],
    [5,7],
    [5,8],
    [6,7],
    [6,8],
    [7,8]
])

# Add faces
klein.add_simplices([
    [0,1,3],
    [0,1,7],
    [0,2,3],
    [0,2,5],
    [0,5,6],
    [0,6,7],
    [1,2,4],
    [1,2,8],
    [1,3,4],
    [1,7,8],
    [2,3,8],
    [2,4,5],
    [3,4,6],
    [3,6,8],
    [4,5,7],
    [4,6,7],
    [5,6,8],
    [5,7,8]
])

# Expected: [1,2,1]
print(f'Klein Bottle:\t{klein.get_betti_numbers()}')

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