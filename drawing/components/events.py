import pygame

from components.setup import *

'''
Function for handling left mouse click event. Left mouse click removes vertices from the complex.
'''
def handle_left_mouseclick(points, selected, simplex_verts):
    pos = pygame.mouse.get_pos()
    
    select = True
    deselect = False

    # Check if an already existing point has been clicked
    exists = False
    for p in points:
        if p.collidepoint(pos):
            clicked_point = p
            clicked_center = clicked_point.center
            if clicked_center in selected:
                select = False
                deselect = True
            exists = True

    # Draw the point if it doesn't exist
    if not exists:
        simplex_verts.append(pos)
    elif select:
        selected.append(clicked_center)
    elif deselect and clicked_center in selected:
        selected.remove(clicked_center)
    
    if len(selected) > 4:
        del selected[0]

    # Reset screen
    SCREEN.fill(BACKGROUND_COLOR)

    return selected, simplex_verts

'''
Function for handling right mouse click event. Right mouse click adds or selects vertices.
'''
def handle_right_mouseclick(points, selected, simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra):
    pos = pygame.mouse.get_pos()

    # Check if an already existing point has been clicked
    exists = False
    for p in points:
        if p.collidepoint(pos):
            clicked_point = p
            exists = True
    
    # Erase the point and associated simplices if it exists
    if exists:
        pos = clicked_point.center
        simplex_verts.remove(pos)
        for e in simplex_edges.copy():
            if pos in e:
                simplex_edges.remove(e)
        for t in simplex_triangles.copy():
            if pos in t:
                simplex_triangles.remove(t)
        for t in simplex_tetrahedra.copy():
            if pos in t:
                simplex_tetrahedra.remove(t)
        if pos in selected:
            selected.remove(pos)
    
    else:
        selected = []

    # Reset screen
    SCREEN.fill(BACKGROUND_COLOR)

    return selected, simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra

'''
Function for handling keyboard input.
'''
def handle_keys(key, selected, simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra, betti_numbers):

    simplex_edges = [set(e) for e in simplex_edges]
    simplex_triangles = [set(t) for t in simplex_triangles]
    simplex_tetrahedra = [set(th) for th in simplex_tetrahedra]

    # If space bar is pressed, draw/remove the simplex corresponding to the affine hull of the selected points
    if key == pygame.K_SPACE:

        simplex = {v for v in selected}

        # Handle case where two points are selected (edge)
        if len(selected) == 2:
            # Add edge if not already drawn
            if simplex not in simplex_edges:
                simplex_edges.append(simplex)
            
            # Remove edge if already drawn
            else:
                while simplex in simplex_edges:
                    simplex_edges.remove(simplex)

                # Remove any triangles that contain this edge
                simplex = list(simplex)
                v0 = simplex[0]
                v1 = simplex[1]

                for t in simplex_triangles.copy():
                    if v0 in t and v1 in t:
                        simplex_triangles.remove(t)
                for t in simplex_tetrahedra.copy():
                    if v0 in t and v1 in t:
                        simplex_tetrahedra.remove(t)

        # Handle case where three points are selected (triangle)
        if len(selected) == 3:
            # Add triangle if not already drawn
            if simplex not in simplex_triangles:
                simplex_triangles.append(simplex)
                
                # Add edges if not already drawn
                simplex = list(simplex)
                for vertex in simplex:
                    for other in simplex:
                        edge = (vertex, other)
                        if vertex != other and edge not in simplex_edges:
                            simplex_edges.append(edge)
            
            # If already drawn, remove triangle
            else:
                while simplex in simplex_triangles:
                    simplex_triangles.remove(simplex)

                # Remove any tetrahedra that contain this face
                simplex = list(simplex)
                v0 = simplex[0]
                v1 = simplex[1]
                v2 = simplex[2]

                for t in simplex_tetrahedra.copy():
                    if v0 in t and v1 in t and v2 in t:
                        simplex_tetrahedra.remove(t)
        
        if len(selected) == 4:
            # Add triangle if not already drawn
            if simplex not in simplex_tetrahedra:
                simplex_tetrahedra.append(simplex)
                
                # Add edges if not already drawn
                simplex = list(simplex)
                for vertex in simplex:
                    for other in simplex:
                        edge = (vertex, other)
                        if vertex != other and edge not in simplex_edges:
                            simplex_edges.append(edge)
                        for another in simplex:
                            triangle = (vertex, other, another)
                            if vertex != other and vertex != another and other != another and triangle not in simplex_triangles:
                                simplex_triangles.append(triangle)
            
            # If already drawn, remove tetrahedron
            else:
                simplex_tetrahedra.remove(simplex)
    
    if key == pygame.K_r:
        selected, simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra = [], [], [], [], []
    
    # Reset screen
    SCREEN.fill(BACKGROUND_COLOR)

    return selected, simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra, betti_numbers