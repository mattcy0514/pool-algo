import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import config
import random

plt.switch_backend('agg')
class Graphic:
    def __init__(self):
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.ax.set_aspect('equal')
        self._set_lim()
        self._set_facecolor("green")

    def _set_lim(self):
        self.ax.set_xlim((0, config.length))
        self.ax.set_ylim((0, config.width))

    def _set_facecolor(self, color):
        self.ax.set_facecolor(color)

    def _set_mball(self, mball, color):
        mball_plt = plt.Circle([mball.pos[0,0], mball.pos[1,0]], radius=config.radius, color=color)
        self.ax.add_patch(mball_plt)

    def _set_tballs(self, tballs, color):
        for i in range(len(tballs)):
            tball_plt = plt.Circle([tballs[i].pos[0,0], tballs[i].pos[1,0]], radius=config.radius, color=color)
            self.ax.add_patch(tball_plt)    
            self._set_text(tballs[i].pos, i, 4)
    
    def _set_holes(self, holes, color):
        for hole in holes:
            hole = plt.Circle([hole.pos[0,0], hole.pos[1,0]], radius=config.radius, color=color)
            self.ax.add_patch(hole)

    def _set_moving_list(self, moving_list):
        r = lambda: random.randint(0,255)
        color = '#%02X%02X%02X' % (r(),r(),r())
        for j in range(len(moving_list)-1):
            current_pos = moving_list[j].pos
            next_pos = moving_list[j+1].pos
            self._set_line(current_pos, next_pos, color)

    def _set_line(self, current_pos, next_pos, color):
        line = Line2D([current_pos[0,0], next_pos[0,0]], [current_pos[1,0], next_pos[1,0]], linewidth=0.5, color=color)
        self.ax.add_line(line)

    def _set_text(self, pos, text, fontsize):
        self.ax.text(pos[0,0], pos[1,0], text, fontsize=fontsize)
    
    def _show(self):
        plt.show()
    
    def _savefig(self, name, dpi):
        plt.savefig(name, dpi=dpi)
