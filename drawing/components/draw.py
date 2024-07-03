import numpy as np
import pygame
from pygame import gfxdraw

def order_tetrahedron(tetrahedron):
    points = np.array(list(tetrahedron))
    x, y = points[:,0], points[:,1]

    centroid_x = x.mean()
    centroid_y = y.mean()

    r = np.sqrt(np.square(x-centroid_x) + np.square(y-centroid_y))
    theta = np.arctan2((y-centroid_y), (x-centroid_x))

    new_points = points[np.argsort(theta)].tolist()
    
    return new_points


def draw_polygon_alpha(surface, color, points):

    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)

    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)

    gfxdraw.filled_polygon(shape_surf, [(x - min_x, y - min_y) for x, y in points], color[:3],)
    shape_surf.set_alpha(color[3])

    surface.blit(shape_surf, target_rect)

def draw_line_alpha(surface, color, points, width):

    x0, y0 = points[0]
    x1, y1 = points[1]

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