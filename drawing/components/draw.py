import numpy as np
import pygame
from pygame import gfxdraw

def order_points_by_angle(simplex):
    '''
    Order the points of a drawn simplex by their centroid-centered polar
    angle.

    Parameters:
    -----------
    simplex : list
        A simplex provided as a list of coordinates of its vertices.
    
    Returns:
    --------
    ordered_simplex:
        The input simplex with its vertices ordered by their
        centroid-centered polar angle.
    '''

    points = np.array(list(simplex))
    x, y = points[:,0], points[:,1]

    centroid_x = x.mean()
    centroid_y = y.mean()

    theta = np.arctan2((y-centroid_y), (x-centroid_x))

    # Technically we would need to sort secondarily by the radius in
    # the event that two points are drawn at the exact same angle around
    # the centroid. I will tentatively assume that this never happens.

    ordered_simplex = points[np.argsort(theta)].tolist()
    ordered_simplex = list(tuple(v) for v in ordered_simplex)
    
    return ordered_simplex


def draw_polygon_alpha(surface, color, points):
    '''
    Helper function for drawing a filled polygon which respects the
    alpha value in an RGBA color sequence.

    The parameters are the same as those expected by PyGame's usual
    draw.polygon function.

    Parameters:
    -----------
    surface : pygame.Surface
        The surface to draw the polygon on.
    color : list[int]
        RGBA sequence describing the color and transparency of the
        polygon to draw.
    points : list[float]
        The coordinate sequence describing the vertices of polygon to
        draw.
    '''

    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)

    alpha_polygon = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    alpha_surface = pygame.Surface(alpha_polygon.size, pygame.SRCALPHA)

    gfxdraw.filled_polygon(alpha_surface, [(x - min_x, y - min_y) for x, y in points], color[:3],)
    alpha_surface.set_alpha(color[3])

    surface.blit(alpha_surface, alpha_polygon)

    return

def draw_line_alpha(surface, color, points, width):
    '''
    Helper function for drawing a line which respects the alpha
    value in an RGBA color sequence.

    The parameters are the same as those expected by PyGame's usual
    draw.line function.

    Parameters:
    -----------
    surface : pygame.Surface
        The surface to draw the polygon on.
    color : list[int]
        RGBA sequence describing the color and transparency of the
        polygon to draw.
    points : list[float]
        The coordinate sequence describing the vertices of polygon to
        draw.
    width : float
        The width of the line to draw.
    '''

    x0, y0 = points[0]
    x1, y1 = points[1]

    # PyGame's gfxdraw does not support specifying line thickness, so we
    # determine the coordinates of the polygon which describe our
    # thickened line manually.

    line_length = np.sqrt(np.square(x0-x1) + np.square(y0-y1))
    line_angle = np.arctan2(y0-y1, x0-x1)
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    
    box_x0 = xm + (line_length/2) * np.cos(line_angle) - (width/2) * np.sin(line_angle)
    box_y0 = ym + (width/2) * np.cos(line_angle) + (line_length/2) * np.sin(line_angle)
    box_x1 = xm - (line_length/2) * np.cos(line_angle) - (width/2) * np.sin(line_angle)
    box_y1 = ym + (width/2) * np.cos(line_angle) - (line_length/2) * np.sin(line_angle)
    box_x2 = xm - (line_length/2) * np.cos(line_angle) + (width/2) * np.sin(line_angle)
    box_y2 = ym - (width/2) * np.cos(line_angle) - (line_length/2) * np.sin(line_angle)
    box_x3 = xm + (line_length/2) * np.cos(line_angle) + (width/2) * np.sin(line_angle)
    box_y3 = ym - (width/2) * np.cos(line_angle) + (line_length/2) * np.sin(line_angle)
    
    line_poly = ((box_x0, box_y0), (box_x1, box_y1), (box_x2, box_y2), (box_x3, box_y3))

    lx, ly = zip(*line_poly)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)

    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    
    gfxdraw.aapolygon(shape_surf, [(x - min_x, y - min_y) for x, y in line_poly], color[:3])
    gfxdraw.filled_polygon(shape_surf, [(x - min_x, y - min_y) for x, y in line_poly], color[:3])
    shape_surf.set_alpha(color[3])

    surface.blit(shape_surf, target_rect)

    return