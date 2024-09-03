import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

def plot_voronoi(points, max_radius, xlim, ylim, cell_colors=None):

    center_x = (xlim[0] + xlim[1])/2
    center_y = (ylim[0] + ylim[1])/2
    max_displacement = max(np.concatenate((np.abs(points[:,0]-center_x), np.abs(points[:,1]-center_y))))

    aug_points = 100*max_displacement*np.array([[-1,-1],[1,-1],[1,1],[-1,1]])
    aug_points[:,0] += center_x
    aug_points[:,1] += center_y

    all_points = np.concatenate((points, aug_points))

    vor = Voronoi(all_points)

    if cell_colors is None:
        cell_colors = ['green']*len(points)

    fig, ax = plt.subplots(1,1)

    for i, point in enumerate(points):
        region_index = vor.point_region[i]
        region = vor.regions[region_index]
        verts = vor.vertices[region]
        
        polygon = Polygon(verts)
        circle = Point(point).buffer(max_radius)
        intersection = polygon.intersection(circle)
        xs, ys = intersection.exterior.xy

        ax.plot(point[0],point[1],'o', color='k')
        ax.fill(xs, ys, alpha=0.5, fc=cell_colors[i], ec='none')
        ax.plot(xs, ys, color='k')

    plt.xlim(xlim)
    plt.ylim(ylim)

    return fig, ax