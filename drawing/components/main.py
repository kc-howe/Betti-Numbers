import sys
from pathlib import Path

import pygame

from components.draw import *
from components.events import *
from components.setup import *

from simplicial.simplex_tree import SimplexTree

def main():
    
    pygame.init()

    SCREEN.fill(BACKGROUND_COLOR)

    clock = pygame.time.Clock()

    current_dir = Path(__file__).parent
    icon_path = current_dir / 'images/triangle-icon.png'
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Simplicial Complex Drawing Tool')

    points = []
    selected = []

    simplex_tree = SimplexTree()

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
                    selected, simplex_tree = handle_left_mouseclick(
                        points, selected, simplex_tree
                    )
                if state[2]:
                    (
                        selected,
                        simplex_tree
                    ) = handle_right_mouseclick(
                        points,
                        selected,
                        simplex_tree
                    )
                betti_numbers = simplex_tree.betti_numbers()
            
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                key = event.key
                (
                    selected,
                    simplex_tree
                ) = handle_keys(
                    key,
                    selected,
                    simplex_tree
                )
                betti_numbers = simplex_tree.betti_numbers()

        SCREEN.fill(BACKGROUND_COLOR)

        # Draw the complex specified by the simplex lists
        points = list()
        for tetrahedron in simplex_tree.locate_k_simplices(3):
            tetrahedron = order_points_by_angle(tetrahedron.get_vertex_list())
            #pygame.draw.polygon(SCREEN, AQUA, t, 0)
            draw_polygon_alpha(SCREEN, SOLID_COLOR, tetrahedron)
        for triangle in simplex_tree.locate_k_simplices(2):
            triangle = triangle.get_vertex_list()
            #pygame.draw.polygon(SCREEN, AQUA, t, 0)
            draw_polygon_alpha(SCREEN, FACE_COLOR, triangle)
        for edge in simplex_tree.locate_k_simplices(1):
            edge = edge.get_vertex_list()
            draw_line_alpha(SCREEN, LINE_COLOR, edge, 4)
        for vertex in simplex_tree.locate_k_simplices(0):
            vertex = vertex.get_vertex_list()[0]
            circle = pygame.draw.circle(SCREEN, BACKGROUND_COLOR, vertex, 14)
            gfxdraw.aacircle(SCREEN, vertex[0], vertex[1], 14, LINE_COLOR)
            gfxdraw.filled_circle(SCREEN, vertex[0], vertex[1], 14, LINE_COLOR)
            gfxdraw.aacircle(SCREEN, vertex[0], vertex[1], 10, VERTEX_COLOR)
            gfxdraw.filled_circle(SCREEN, vertex[0], vertex[1], 10, VERTEX_COLOR)
            points.append((circle, vertex))
        for s in selected:
            gfxdraw.aacircle(SCREEN, s[0], s[1], 10, SELECT_COLOR)
            gfxdraw.filled_circle(SCREEN, s[0], s[1], 10, SELECT_COLOR)

        # Display Betti numbers at the top of the screen if any
        text = font.render('', True, LINE_COLOR)
        if betti_numbers:
            text = font.render(
                'Betti Numbers: ' + str(betti_numbers), True, LINE_COLOR
            )
        
        SCREEN.blit(text, (10, 10))
        pygame.display.update()