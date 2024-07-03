import sys

import pygame

from components.draw import *
from components.events import *
from components.setup import *
from components.update import *

def main():
    
    pygame.init()

    SCREEN.fill(BACKGROUND_COLOR)

    clock = pygame.time.Clock()

    icon = pygame.image.load('images/triangle-icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Simplicial Complex Drawing Tool')

    points = []
    selected = []
    
    simplex_verts = []
    simplex_edges = []
    simplex_triangles = []
    simplex_tetrahedra = []

    betti_numbers = []
    
    pygame.font.init()
    font = pygame.font.SysFont('Roboto', 25)

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
                    selected, simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra = handle_right_mouseclick(points, selected, simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra)
                
                betti_numbers = recompute_betti_numbers(simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra)
            
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                key = event.key
                selected, simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra, betti_numbers = handle_keys(key, selected, simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra, betti_numbers)
                betti_numbers = recompute_betti_numbers(simplex_verts, simplex_edges, simplex_triangles, simplex_tetrahedra)

        SCREEN.fill(BACKGROUND_COLOR)

        # Draw the complex specified by the vertex, edge, and triangle sets
        points = []
        for t in simplex_triangles:
            t = list(t)
            #pygame.draw.polygon(SCREEN, AQUA, t, 0)
            draw_polygon_alpha(SCREEN, FACE_COLOR, t)
        for th in simplex_tetrahedra:
            th = order_tetrahedron(th)
            #pygame.draw.polygon(SCREEN, AQUA, t, 0)
            draw_polygon_alpha(SCREEN, SOLID_COLOR, th)
        for e in simplex_edges:
            e = list(e)
            draw_line_alpha(SCREEN, LINE_COLOR, e, 4)
        for v in simplex_verts:
            circle = pygame.draw.circle(SCREEN, BACKGROUND_COLOR, v, 14)
            gfxdraw.aacircle(SCREEN, v[0], v[1], 14, LINE_COLOR)
            gfxdraw.filled_circle(SCREEN, v[0], v[1], 14, LINE_COLOR)
            gfxdraw.aacircle(SCREEN, v[0], v[1], 10, VERTEX_COLOR)
            gfxdraw.filled_circle(SCREEN, v[0], v[1], 10, VERTEX_COLOR)
            points.append(circle)
        for s in selected:
            gfxdraw.aacircle(SCREEN, s[0], s[1], 10, SELECT_COLOR)
            gfxdraw.filled_circle(SCREEN, s[0], s[1], 10, SELECT_COLOR)

        # Display Betti numbers at the top of the screen if any
        text = font.render('', True, LINE_COLOR)
        if betti_numbers:
            text = font.render('Betti Numbers: ' + str(betti_numbers), True, LINE_COLOR)
        
        SCREEN.blit(text, (10, 10))
        pygame.display.update()