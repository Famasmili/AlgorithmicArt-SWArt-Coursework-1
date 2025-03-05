# Basic implementation of displaying images in a grid
# from dataclasses import dataclass
# from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
# from PyQt5.QtCore import Qt
from vispy import scene
import os
import cv2
# import numpy as np
import random
import sys

class DisplayImagesInGrid(QMainWindow):
    def __init__(self, image_folder, grid_size, window_size):
        super().__init__()
        self.image_folder = image_folder
        self.grid_size = grid_size
        self.window_size = window_size
        self.image_list = self.get_image_list()
        self.image_grid = self.get_image_grid()
        self.init_ui()

    def get_image_list(self):
        image_list = []
        for image in os.listdir(self.image_folder):
            image_list.append(os.path.join(self.image_folder, image))
        return image_list

    def get_image_grid(self):
        image_grid = []
        for i in range(self.grid_size[0]):
            row = []
            for j in range(self.grid_size[1]):
                row.append(self.image_list.pop(random.randint(0, len(self.image_list) - 1)))
            image_grid.append(row)
        return image_grid

    def init_ui(self):
        canvas = scene.SceneCanvas(keys='interactive', show=True)
        grid = canvas.central_widget.add_grid(spacing=0)
        self.setWindowTitle('Image Grid')
        self.setGeometry(500, 700, self.window_size[0], self.window_size[1])

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                image = cv2.imread(self.image_grid[i][j])
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                view = grid.add_view(row=i, col=j, border_color='white')
                image_visual = scene.visuals.Image(image, parent=view.scene)
                view.camera = scene.PanZoomCamera(aspect=1)
                view.camera.set_range()
                view.camera.flip = (0, 1, 0)
                view.camera.set_range() 
        
        self.setCentralWidget(canvas.native)  # Set the SceneCanvas as the central widget
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_folder = 'D://Courses/UdeM IFT6251_AlgorithmicArt/Cours_1_work/SWArt Works/DataBased/images'
    grid_size = (2, 2)
    window_size = (800, 800)
    display_images_in_grid = DisplayImagesInGrid(image_folder, grid_size, window_size)
    sys.exit(app.exec_())

