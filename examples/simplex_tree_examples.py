from simplicial.simplex_tree import SimplexTree


print('BETTI NUMBERS\n')

'''
Compute the Betti numbers of the 3-ball triangulated by a single
tetrahedron.
'''
ball = SimplexTree()

# Add solids
ball.insert_full_simplex('A','B','C','D')

# Expected: [1,0,0,0]
print(f'3-Ball:\t\t{ball.betti_numbers()}')

'''
Compute the Betti numbers of the 2-sphere triangulated by the faces of a
single tetrahedron.
'''
sphere = SimplexTree()

# Add the tetrahedron with all of its faces, then remove the
# tetrahedron, leaving only its faces
sphere.insert_full_simplex(1,2,3,4)
sphere.remove_simplex(1,2,3,4)

# Expected: [1,0,1]
print(f'2-Sphere:\t{sphere.betti_numbers()}')

'''
Compute the Betti numbers of the cylinder.
'''
cylinder = SimplexTree()

# Add faces
cylinder.insert_full_simplices([
    [0,1,4],
    [0,2,3],
    [0,3,4],
    [1,2,5],
    [1,4,5],
    [2,3,5]
])

# Expected: [1,1,0]
print(f'Cylinder:\t{cylinder.betti_numbers()}')

'''
Compute the Betti numbers of the mobius strip.
'''
mobius = SimplexTree()

# Add faces
mobius.insert_full_simplices([
    [0,1,4],
    [0,2,3],
    [0,2,5],
    [0,3,4],
    [1,2,5],
    [1,4,5],
])

# Expected: [1,1,0]
print(f'Mobius Strip:\t{mobius.betti_numbers()}')

'''
Compute the Betti numbers of the torus.
'''
torus = SimplexTree()

# Add faces
torus.insert_full_simplices([
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
print(f'Torus:\t\t{torus.betti_numbers()}')

'''
Compute the Betti numbers of the Klein bottle.
'''
klein = SimplexTree()

# Add faces
klein.insert_full_simplices([
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
print(f'Klein Bottle:\t{klein.betti_numbers()}')

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