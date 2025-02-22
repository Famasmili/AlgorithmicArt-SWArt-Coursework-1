import colorsys
import random
from typing import Tuple
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                           QSlider, QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import Qt, QTimer
from vispy import scene

from collections import deque

@dataclass
class AttractorParams:
    params: Tuple[float, ...]
    name: str
    dimension: int = 3
    trail_length: int = 1000  # How many previous points to show

class AttractorSystem(ABC):
    def __init__(self, params: AttractorParams, dt: float = 0.01):
        self.params = params
        self.dt = dt
        self.current_state = np.random.uniform(-0.1, 0.1, size=params.dimension)
        self.trail = deque(maxlen=params.trail_length)
        self.trail.append(self.current_state.copy())
    
    @abstractmethod
    def step(self) -> np.ndarray:
        pass

class CliffordAttractor(AttractorSystem):
    def step(self) -> np.ndarray:
        x, y = self.current_state
        a, b, c, d = self.params.params

        self.current_state[0] = np.sin(a * y) + c * np.cos(a * x)
        self.current_state[1] = np.sin(b * x) + d * np.cos(b * y)
        self.trail.append(self.current_state.copy())
        return self.current_state               

class DeJongAttractor(AttractorSystem):
    def step(self) -> np.ndarray:
        x, y = self.current_state
        a, b, c, d = self.params.params

        self.current_state[0] = np.sin(a * y) - np.cos(b * x)
        self.current_state[1] = np.sin(c * x) - np.cos(d * y)
        self.trail.append(self.current_state.copy())
        return self.current_state

class AizawaAttractor(AttractorSystem):
   def step(self) -> np.ndarray:
      def derivatives(s: np.ndarray) -> np.ndarray:
          x, y, z = s
          a, b, c, d, e = self.params.params
          return np.array([
              (z - b) * x - d * y,
              d * x + (z - b) * y,
              c + a * z - (z ** 3) / 3 - (x ** 2 + y ** 2) * (1 + e * z) + 0.1 * z * x ** 3
          ])
      # RK4 integration
      k1 = derivatives(self.current_state)
      k2 = derivatives(self.current_state + 0.5 * self.dt * k1)
      k3 = derivatives(self.current_state + 0.5 * self.dt * k2)
      k4 = derivatives(self.current_state + self.dt * k3)
      # Update state
      self.current_state += (self.dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
      self.trail.append(self.current_state.copy())
      return self.current_state

"""    
class ThomasAttractor(AttractorSystem):
    def step(self) -> np.ndarray:
        def derivatives(s: np.ndarray) -> np.ndarray:
            x, y, z = s
            b = self.params.params
            return np.array([
                np.sin(y) - b * x,
                np.sin(z) - b * y,
                np.sin(x) - b * z
            ])
        # RK4 integration
        k1 = derivatives(self.current_state)
        k2 = derivatives(self.current_state + 0.5 * self.dt * k1)
        k3 = derivatives(self.current_state + 0.5 * self.dt * k2)
        k4 = derivatives(self.current_state + self.dt * k3)

        # Update state
        self.current_state += (self.dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        self.trail.append(self.current_state.copy())

        return self.current_state
"""

class LorenzAttractor(AttractorSystem):
    def step(self) -> np.ndarray:
        def derivatives(s: np.ndarray) -> np.ndarray:
            x, y, z = s
            sigma, rho, beta = self.params.params
            return np.array([
                sigma * (y - x),
                x * (rho - z) - y,
                x * y - beta * z
            ])
        
        # RK4 integration
        k1 = derivatives(self.current_state)
        k2 = derivatives(self.current_state + 0.5 * self.dt * k1)
        k3 = derivatives(self.current_state + 0.5 * self.dt * k2)
        k4 = derivatives(self.current_state + self.dt * k3)
        
        # Update state
        self.current_state += (self.dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        self.trail.append(self.current_state.copy())
        
        return self.current_state

class AttractorVisualizer(QMainWindow):
    def __init__(self, attractor: AttractorSystem):
        super().__init__()
        self.attractor = attractor
        self.animation_speed = 1
        self.rotation_speed = 1.0
        self.trail_color_shift = 0.0
        self.paused = False
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Strange Attractor Evolution')
        self.setGeometry(1300, 700, 1000, 800)
        
        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Vispy canvas
        self.canvas = scene.SceneCanvas(keys='interactive', size=(800, 800))
        main_layout.addWidget(self.canvas.native)
        
        # 3D view
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable' if self.attractor.params.dimension == 3 else 'panzoom'
        self.view.camera.fov = 45 
        self.view.camera.distance = 80 # Zoom out
        
        # Line plot for the trail
        self.line = scene.visuals.Line(parent=self.view.scene)
        self.show_lines = True
        
        # Current point marker
        self.current_point = scene.visuals.Markers(parent=self.view.scene)
        self.scatter = scene.visuals.Markers(parent=self.view.scene)
        self.points_show = False
        
        # Controls
        control_layout = QHBoxLayout()
        
        # Speed control
        speed_layout = QVBoxLayout()
        speed_label = QLabel("Evolution Speed")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.valueChanged.connect(self.update_speed)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        control_layout.addLayout(speed_layout)
        
        # Trail length control
        trail_layout = QVBoxLayout()
        trail_label = QLabel("Trail Length")
        self.trail_slider = QSlider(Qt.Horizontal)
        self.trail_slider.setMinimum(100)
        self.trail_slider.setMaximum(5000)
        self.trail_slider.setValue(1000)
        self.trail_slider.valueChanged.connect(self.update_trail_length)
        trail_layout.addWidget(trail_label)
        trail_layout.addWidget(self.trail_slider)
        control_layout.addLayout(trail_layout)
        
        # Pause/Resume button
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        control_layout.addWidget(self.pause_button)
        
        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_system)
        control_layout.addWidget(self.reset_button)

        # Show scattered points button
        self.scatter_button = QPushButton("Show points")
        self.scatter_button.clicked.connect(self.show_points)
        control_layout.addWidget(self.scatter_button)

        # Clear the lines button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_lines)
        control_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(control_layout)
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system)
        self.timer.start(16)  # ~60 FPS
        
    def update_system(self):
        if self.paused:
            return
            
        # Update system multiple times per frame based on speed
        for _ in range(self.animation_speed):
            self.attractor.step()
        
        # Update visualization
        trail_points = np.array(list(self.attractor.trail))
        
        # Generate colors for the trail (newer points are brighter)
        n_points = len(trail_points)
        color_values = np.linspace(0.2, 1.0, n_points)
        colors = np.zeros((n_points, 4))
        
        # Create rainbow trail effect
        for i in range(n_points):
            hue = (i / n_points + self.trail_color_shift) % 1.0
            rgb = colorsys.hsv_to_rgb(hue, 0.8, color_values[i])
            colors[i] = np.append(rgb, 1.0)  # Add alpha channel
        
        # Update trail visualization
        self.line.set_data(pos=trail_points, color=colors)
        self.line.visible = self.show_lines
        
        # Update current point
        self.current_point.set_data(
            pos=trail_points[-1:],
            edge_color='white',
            face_color='white',
            size=10
        )
        
        # Rotate view
        if self.attractor.params.dimension == 3:
            self.view.camera.azimuth += self.rotation_speed * 0.1 # Rotate around the y axis
            # self.view.camera.elevation += self.rotation_speed * 0.1 # Rotate around the z axis
            self.view.camera.roll += self.rotation_speed * 0.1 # Rotate around the x
        
        self.trail_color_shift = (self.trail_color_shift + 0.001) % 1.0
        
        self.canvas.update()
        
    def update_speed(self):
        self.animation_speed = self.speed_slider.value() // 10
        
    def update_trail_length(self):
        new_length = self.trail_slider.value()
        old_trail = list(self.attractor.trail)
        self.attractor.trail = deque(old_trail[-new_length:], maxlen=new_length)
        
    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.setText("Resume" if self.paused else "Pause")
        
    def reset_system(self):
        self.attractor.current_state = np.random.uniform(-0.1, 0.1, 
                                                       size=self.attractor.params.dimension)
        self.attractor.trail.clear()
        if self.points_show:
            self.scatter.set_data(self.attractor.current_state.reshape(1, -1), edge_color=(0.5, 0.5, 0.5, 0.7),
                                   face_color=(0.5, 0.5, 0.5, 0.7), size=2)
        else:
            self.scatter.set_data(self.attractor.current_state.reshape(1, -1), edge_color=(0, 0, 0, 0),
                                   face_color=(0, 0, 0, 0), size=0)
        self.attractor.trail.append(self.attractor.current_state.copy())

    def show_points(self):
        trail_points = np.array(list(self.attractor.trail))
        if self.scatter_button.text() == "Show points":
            self.scatter_button.setText("Hide points")
            self.points_show = True
            self.scatter.set_data(trail_points, edge_color=(0.5, 0.5, 0.5, 0.7), face_color=(0.5, 0.5, 0.5, 0.7), size=2)
            # self.scatter.visible = True
        # Hide points
        else:
            self.scatter_button.setText("Show points")
            self.points_show = False
            self.scatter.set_data(trail_points, edge_color=(0, 0, 0, 0), face_color=(0, 0, 0, 0), size=0)

        self.canvas.update()

    def clear_lines(self):
        if self.clear_button.text() == "Clear":
            self.clear_button.setText("Show lines")
            self.attractor.trail.clear()
            self.show_lines = False
            
        else:
            self.clear_button.setText("Clear")
            self.show_lines = True
            # self.update_system() # redraw with lines
        self.canvas.update()


def main():
    app = QApplication([])
    
    params = random.choice((AttractorParams(
        params=(10.0, 28.0, 8/3),
        name='Lorenz',
        dimension=3 ,
        trail_length=10000
    ), (AttractorParams(
        params=(-1.4, 1.6, 1.0, 0.7),
        name='Clifford',
        dimension=2,
        trail_length=10000
    )), (AttractorParams(
        params=(-2.0, -2.0, -1.2, 2.0),
        name='DeJong',
        dimension=2,
        trail_length=10000
    )), (AttractorParams(
        params=(0.95, 0.7, 0.6, 3.5, 0.25),
        name='Aizawa',
        dimension=3,
        trail_length=10000
    ))))
    print(f"params: {params}")
    if params.name == 'Clifford':
        attractor = CliffordAttractor(params)
    elif params.name == 'DeJong':
        attractor = DeJongAttractor(params)
    elif params.name == 'Aizawa':
        attractor = AizawaAttractor(params)
    else:
        attractor = LorenzAttractor(params)
    
    # Create and show visualizer
    viz = AttractorVisualizer(attractor)
    viz.show()
    
    app.exec_()

if __name__ == '__main__':
    main()