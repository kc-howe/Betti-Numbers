import pygame

from components.draw import order_points_by_angle
from components.setup import *

from simplicial.simplex_tree import SimplexTree


def handle_left_mouseclick(points, selected, simplex_tree):
    '''
    Handle left mouseclick events.

    If left-clicked, an unselected vertex is selected. Conversely,
    a selected vertex is de-selected on left-click.

    Parameters:
    -----------
    points : list
        List of drawn (vertex) objects supporting collidepoint method
        calls.
    selected : list
        The running list of selected vertices.
    simplex_tree : SimplexTree
        The simplex tree of the drawn simplicial complex.
    
    Returns:
    --------
    selected : list
        The running list of selected vertices.
    simplex_tree : SimplexTree
        The simplex tree of the drawn simplicial complex.
    '''

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
        simplex_tree.insert_simplex(pos)
    elif select:
        selected.append(clicked_center)
    elif deselect and clicked_center in selected:
        selected.remove(clicked_center)
    
    if len(selected) > 4:
        del selected[0]

    # Reset screen
    SCREEN.fill(BACKGROUND_COLOR)

    return selected, simplex_tree

def handle_right_mouseclick(points, selected, simplex_tree):

    '''
    Handle right mouseclick events.

    If right-clicked, a vertex is removed from the simplicial complex.
    If instead the canvas is right-clicked, we clear the current
    vertex selection.

    Parameters:
    -----------
    points : list
        List of drawn (vertex) objects supporting collidepoint method
        calls.
    selected : list
        The running list of selected vertices.
    simplex_tree : SimplexTree
        The simplex tree of the drawn simplicial complex.
    
    Returns:
    --------
    selected : list
        The running list of selected vertices.
    simplex_tree : SimplexTree
        The simplex tree of the drawn simplicial complex.
    '''

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
        simplex_tree.remove_simplex(pos)
        if pos in selected:
            selected.remove(pos)
    
    else:
        selected = []

    # Reset screen
    SCREEN.fill(BACKGROUND_COLOR)

    return selected, simplex_tree


def handle_keys(key, selected, simplex_tree): 
    '''
    Handle keyboard input events.

    Parameters:
    -----------
    key : pygame.key
        PyGame constant indicated which key was pressed.
    selected : list
        The running list of selected vertices.
    simplex_tree : SimplexTree
        The simplex tree of the drawn simplicial complex.
    
    Returns:
    --------
    selected : list
        The running list of selected vertices.
    simplex_tree : SimplexTree
        The simplex tree of the drawn simplicial complex.
    '''

    # If space bar is pressed, draw/remove the simplex corresponding to
    # the affine hull of the selected points
    if key == pygame.K_SPACE:

        simplex = sorted(selected, key=lambda x: str(x))

        if simplex_tree.search_simplex(*simplex) is None:
            simplex_tree.insert_full_simplex(*simplex)
        else:
            simplex_tree.remove_simplex(*simplex)
            if len(simplex) == 1:
                selected = []
    
    if key == pygame.K_r:
        selected = []
        simplex_tree = SimplexTree()
    
    # Reset screen
    SCREEN.fill(BACKGROUND_COLOR)

    return selected, simplex_tree