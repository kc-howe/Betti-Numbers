import pygame
import sys

import numpy as np

from simplicial_complex import SimplicialComplex

SIZE = WIDTH, HEIGHT = 1000, 620
SCREEN = pygame.display.set_mode(SIZE)

# Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (114, 114, 114)
DARK = (0,80,140)
AQUA = (212, 255, 242)
PINK = (255, 188, 220)

'''
A drawing tool for simplicial complexes.

This drawing tool allows a user to draw points, edges, and triangles of a simplicial complex
while computing the Betti numbers of the drawn complex. The tool should enforce that the structure
of a simplicial complex is enforced at all times, filling in and removing simplexes as necessary to
do so.
'''
def main():
    
    pygame.init()

    SCREEN.fill(WHITE)

    clock = pygame.time.Clock()

    icon = pygame.image.load('images/triangle-icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Simplicial Complex Drawing Tool')

    points = []
    selected = []
    
    simplex_verts = []
    simplex_edges = []
    simplex_triangles = []

    betti_numbers = []
    
    pygame.font.init()
    font = pygame.font.SysFont('Century Gothic', 26)

    while True:
        
        # Set FPS
        clock.tick(60)

        
        # Handle events
        for event in pygame.event.get():

            # Allow user to close the window without crashing
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Handle mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                if state[0]:
                    selected, simplex_verts = handle_left_mouseclick(points, selected, simplex_verts)
                if state[2]:
                    selected, simplex_verts, simplex_edges, simplex_triangles = handle_right_mouseclick(points, selected, simplex_verts, simplex_edges, simplex_triangles)
                
                betti_numbers = recompute_betti_numbers(simplex_verts, simplex_edges, simplex_triangles)
            
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                key = event.key
                simplex_edges, simplex_triangles, betti_numbers = handle_keys(key, selected, simplex_verts, simplex_edges, simplex_triangles, betti_numbers)
                betti_numbers = recompute_betti_numbers(simplex_verts, simplex_edges, simplex_triangles)

        # Draw the complex specified by the vertex, edge, and triangle sets
        points = []
        for t in simplex_triangles:
            t = list(t)
            triangle = pygame.draw.polygon(SCREEN, AQUA, t, 0)
        for e in simplex_edges:
            e = list(e)
            edge = pygame.draw.line(SCREEN, GREY, e[0], e[1], 4)
        for s in selected:
            circle = pygame.draw.circle(SCREEN, PINK, s, 14)
        for v in simplex_verts:
            circle = pygame.draw.circle(SCREEN, BLACK, v, 8)
            points.append(circle)

        # Display Betti numbers at the top of the screen if any
        text = font.render('', False, BLACK)
        if betti_numbers:
            text = font.render('Betti Numbers: ' + str(betti_numbers), False, BLACK)
        
        SCREEN.blit(text, (10, 10))
        pygame.display.flip()

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
            if clicked_point.center in selected:
                select = False
                deselect = True
            exists = True

    # Draw the point if it doesn't exist
    if not exists:
        simplex_verts.append(pos)
    elif select:
        selected.append(clicked_point.center)
    elif deselect:
        selected.remove(clicked_point.center)
    
    if len(selected) > 3:
        del selected[0]

    # Reset screen
    SCREEN.fill(WHITE)

    return selected, simplex_verts

'''
Function for handling right mouse click event. Right mouse click adds or selects vertices.
'''
def handle_right_mouseclick(points, selected, simplex_verts, simplex_edges, simplex_triangles):
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
        if pos in selected:
            selected.remove(pos)

    # Reset screen
    SCREEN.fill(WHITE)

    return selected, simplex_verts, simplex_edges, simplex_triangles

'''
Function for handling keyboard input.
'''
def handle_keys(key, selected, simplex_verts, simplex_edges, simplex_triangles, betti_numbers):
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
                simplex_edges.remove(simplex)

                # Remove any triangles that contain this edge
                simplex = list(simplex)
                v0 = simplex[0]
                v1 = simplex[1]

                for t in simplex_triangles.copy():
                    if v0 in t and v1 in t:
                        simplex_triangles.remove(t)

        # Handle case where three points are selected (triangle)
        if len(selected) == 3:
            # Add triangle if not already drawn
            if simplex not in simplex_triangles:
                simplex_triangles.append(simplex)
                
                # Add edges if not already drawn
                simplex = list(simplex)
                for vertex in simplex:
                    for other in simplex:
                        edge = {vertex, other}
                        if vertex != other and edge not in simplex_edges:
                            simplex_edges.append(edge)
            
            # If already drawn, remove triangle
            else:
                simplex_triangles.remove(simplex)
    
    # Reset screen
    SCREEN.fill(WHITE)

    return simplex_edges, simplex_triangles, betti_numbers

'''
Computes boundary matrices for the drawn complex.
'''
def get_boundary_matrices(simplex_verts, simplex_edges, simplex_triangles):
    B0 = []
    B1 = []
    B2 = []
    
    # Add all vertices
    row = []
    for v in simplex_verts:
        row.append(1)
    B0.append(row)
    
    # For each vertex-edge pair, set to 1 if vertex is in edge
    for v in simplex_verts:
        row = []
        for e in simplex_edges:
            if v in e:
                row.append(1)
            else:
                row.append(0)
        B1.append(row)
    
    # For each edge-triangle pair, set to 1 if edge is in triangle
    for e in simplex_edges:
        row = []
        for t in simplex_triangles:
            e = list(e)
            if e[0] in t and e[1] in t:
                row.append(1)
            else:
                row.append(0)
        B2.append(row)
    
    return B0, B1, B2

'''
Computes Betti numbers of the drawn complex and returns them as a list.
'''
def recompute_betti_numbers(simplex_verts, simplex_edges, simplex_triangles):
    B0, B1, B2 = get_boundary_matrices(simplex_verts, simplex_edges, simplex_triangles)
    comp = SimplicialComplex()
    betti_numbers = []
    if any(B0):
        comp.add_boundary_matrix(0, np.array(B0))
    if any(B1):
        comp.add_boundary_matrix(1, np.array(B1))
    if any(B2):
        comp.add_boundary_matrix(2, np.array(B2))
    if any(B0):
        betti_numbers = comp.get_betti_numbers(recompute=True)
    
    return betti_numbers



if __name__ == "__main__":
    main()