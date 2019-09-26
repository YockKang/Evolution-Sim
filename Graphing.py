import matplotlib, pygame
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import matplotlib.backends.backend_agg as agg
from Sprites import *

class Graph():
    def __init__(self, datax=[], datay=[], name = 'Graph :)'):
        self.datax = datax
        self.datay = datay
        self.name = name
        self.fig, self.ax = plt.subplots(figsize=(4, 2))
        self.canvas = None

        self.ax.set(title=self.name)
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.canvas.draw()
        self.renderer = self.canvas.get_renderer()
        self.canvas.flush_events()
        self.rawdata = self.renderer.tostring_rgb()
        plt.rc({'ytick': 8})
        
    def update(self, yval, xval, colour = 'blue'):
        self.canvas.flush_events()
        self.ax.set(title=self.name)
        self.lines, = self.ax.plot(xval,yval, c=colour, aa=True)
        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.canvas.draw()
        self.renderer = self.canvas.get_renderer()
        self.rawdata = self.renderer.tostring_rgb()

def showgraph(graph,pos):
    canvas = graph.canvas
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(graph.rawdata, size, "RGB")
    screen.blit(surf, pos)
