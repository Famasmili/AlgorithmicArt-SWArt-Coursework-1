from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from vispy import scene, app
import cv2
import sys
import os
import random
import numpy as np
import time
from anime_dataset import AnimeDataset

class GridCell:
    """Represents a cell in the poster grid with position and size information"""
    def __init__(self, x, y, width, height, weight=1.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.weight = weight  # Importance weight for the image

class PosterLayoutGenerator:
    
    def __init__(self, canvas_width, canvas_height, min_cell_width=0.2, min_cell_height=0.2):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.min_cell_width_frac = min_cell_width
        self.min_cell_height_frac = min_cell_height
        
    def generate_variable_grid(self, complexity=0.5):
        min_cell_width = int(self.canvas_width * self.min_cell_width_frac)
        min_cell_height = int(self.canvas_height * self.min_cell_height_frac)
        
        cells = [GridCell(0, 0, self.canvas_width, self.canvas_height)]
        
        num_splits = int(5 + complexity * 15)
        
        for _ in range(num_splits):
            if not cells:
                break
                
            cell_weights = [cell.width * cell.height for cell in cells]
            cell_index = random.choices(range(len(cells)), weights=cell_weights)[0]
            cell = cells.pop(cell_index)
            
            if cell.width >= cell.height:
                split_horizontal = True
            elif cell.width < cell.height:
                split_horizontal = False
            
            if split_horizontal and cell.width < min_cell_width * 2:
                cells.append(cell)  # Put it back
            elif not split_horizontal and cell.height < min_cell_height * 2:
                cells.append(cell)  # Put it back
            
            margin = 0.3
            if split_horizontal:
                min_split = int(cell.width * margin)
                max_split = int(cell.width * (1 - margin))
                if max_split <= min_split:
                    split_pos = cell.width // 2
                else:
                    split_pos = random.randint(min_split, max_split)
                    
                cells.append(GridCell(cell.x, cell.y, split_pos, cell.height))
                cells.append(GridCell(cell.x + split_pos, cell.y, cell.width - split_pos, cell.height))
            else:
                min_split = int(cell.height * margin)
                max_split = int(cell.height * (1 - margin))
                if max_split <= min_split:
                    split_pos = cell.height // 2
                else:
                    split_pos = random.randint(min_split, max_split)
                    
                cells.append(GridCell(cell.x, cell.y, cell.width, split_pos))
                cells.append(GridCell(cell.x, cell.y + split_pos, cell.width, cell.height - split_pos))
            
        return cells


class AnimePosterGenerator(QMainWindow):
    def __init__(self, dataset, window_size, use_variable_grid=True, complexity=0.7):
        super().__init__()
        self.dataset = dataset
        self.window_size = window_size
        self.use_variable_grid = use_variable_grid
        self.complexity = complexity
        
        # Animation and audio state
        self.enable_animation = False
        self.animation_speed = 0.02
        self.animation_scale_factor = 0.1
        self.enable_audio = False
        self.last_frame_time = 0
        self.animation_value = 0.0
        
        if use_variable_grid:
            self.layout_generator = PosterLayoutGenerator(window_size[0], window_size[1])
            self.grid_cells = self.layout_generator.generate_variable_grid(complexity)
        else:
            # Create regular grid
            rows, cols = 3, 3
            cell_width = window_size[0] // cols
            cell_height = window_size[1] // rows
            self.grid_cells = []
            for i in range(rows):
                for j in range(cols):
                    self.grid_cells.append(GridCell(
                        j * cell_width, i * cell_height, 
                        cell_width, cell_height
                    ))
        
        self.media_player = QMediaPlayer()
        
        self.images = self.assign_images_to_cells()
        
        self.init_ui()
        
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16)  # ~60fps
        
    def assign_images_to_cells(self):
        images = []
        
        num_cells = len(self.grid_cells)
        
        use_same_anime = random.random() < 0.3
        
        # Get random anime images
        try:
            if use_same_anime:
                anime_list = self.dataset.get_anime_list()
                for anime in random.sample(anime_list, len(anime_list)):
                    all_images = self.dataset.get_anime_image_paths(anime)
                    if len(all_images) >= num_cells:
                        selected_images = random.sample(all_images, num_cells)
                        images = [(anime, path) for path in selected_images]
                        break
                
                if not images:
                    use_same_anime = False
            
            if not use_same_anime:
                anime_list = self.dataset.get_anime_list()
                for _ in range(num_cells):
                    anime = random.choice(anime_list)
                    image_path = self.dataset.get_random_anime_image(anime)
                    images.append((anime, image_path))
        
        except ValueError as e:
            print(f"Warning: {e}. Falling back to mixed anime selection.")
            anime_list = self.dataset.get_anime_list()
            for _ in range(num_cells):
                anime = random.choice(anime_list)
                image_path = self.dataset.get_random_anime_image(anime)
                images.append((anime, image_path))
                
        return images
        
    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        self.canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='black')
        
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(aspect=1)
        
        # Crucial
        self.view.camera.set_range(x=(0, self.window_size[0]), y=(0, self.window_size[1]), margin=0)
        
        main_layout.addWidget(self.canvas.native, 1)
        
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        # Animation toggle button
        self.animation_btn = QPushButton("Animation: OFF")
        self.animation_btn.clicked.connect(self.toggle_animation)
        control_layout.addWidget(self.animation_btn)
        
        # Animation speed slider
        speed_layout = QVBoxLayout()
        speed_label = QLabel("Animation Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(20)  # Default value
        self.speed_slider.valueChanged.connect(self.set_animation_speed)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        control_layout.addLayout(speed_layout)
        
        # Audio controls
        audio_layout = QVBoxLayout()
        self.audio_btn = QPushButton("Audio: OFF")
        self.audio_btn.clicked.connect(self.toggle_audio)
        audio_layout.addWidget(self.audio_btn)
        
        # Load audio button
        load_audio_btn = QPushButton("Load Audio File")
        load_audio_btn.clicked.connect(self.load_audio_file)
        audio_layout.addWidget(load_audio_btn)
        control_layout.addLayout(audio_layout)
        
        # Regenerate button
        regenerate_btn = QPushButton("Generate New Poster")
        regenerate_btn.clicked.connect(self.regenerate_poster)
        control_layout.addWidget(regenerate_btn)
        
        # Export button
        export_btn = QPushButton("Export Image")
        export_btn.clicked.connect(self.export_poster)
        control_layout.addWidget(export_btn)
        
        main_layout.addWidget(control_panel)
        
        self.setCentralWidget(central_widget)
        
        self.setWindowTitle('Anime Poster Generator')
        self.setGeometry(700, 800, self.window_size[0], self.window_size[1] + 100)
        
        self.create_image_visuals()
    
    def create_image_visuals(self):
        self.image_visuals = []
        
        for i, (cell, (anime, image_path)) in enumerate(zip(self.grid_cells, self.images)):
            # Load and process image
            try:
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Warning: Failed to load image at {image_path}")
                    continue
                
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = np.flipud(image)
                
                img_height, img_width, _ = image.shape
                
                width_ratio = cell.width / img_width
                height_ratio = cell.height / img_height
                
                scale_ratio = max(width_ratio, height_ratio)
                
                new_width = int(img_width * scale_ratio)
                new_height = int(img_height * scale_ratio)
                
                resized_image = cv2.resize(image, (new_width, new_height))
                
                if new_width > cell.width or new_height > cell.height:
                    start_x = (new_width - cell.width) // 2 if new_width > cell.width else 0
                    start_y = (new_height - cell.height) // 2 if new_height > cell.height else 0
                    
                    cropped_image = resized_image[
                        start_y:start_y + min(cell.height, new_height),
                        start_x:start_x + min(cell.width, new_width)
                    ]
                    final_image = cropped_image
                else:
                    final_image = resized_image
                
                # Create image visual
                image_visual = scene.visuals.Image(
                    final_image, 
                    parent=self.view.scene
                )
                
                # Position the image
                image_visual.transform = scene.transforms.STTransform(
                    translate=(cell.x, cell.y)
                )
                
                self.image_visuals.append((image_visual, cell))
                
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
    
    def update_animation(self):
        # Calculate delta time for smooth animation regardless of frame rate
        current_time = time.time()
        dt = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        if not self.enable_animation:
            return
        
        self.animation_value += self.animation_speed * dt * 60  # Normalize to 60fps
        
        while self.animation_value > 1.0:
            self.animation_value -= 1.0
            
        scale_factor = 1.0 + self.animation_scale_factor * (0.5 + 0.5 * np.sin(self.animation_value * 2 * np.pi))
        
        for visual, cell in self.image_visuals:
            center_x = cell.x + cell.width / 2
            center_y = cell.y + cell.height / 2
            
            transform = (
                scene.transforms.STTransform(translate=(center_x, center_y)) *
                scene.transforms.STTransform(scale=(scale_factor, scale_factor)) *
                scene.transforms.STTransform(translate=(-center_x, -center_y)) *
                scene.transforms.STTransform(translate=(cell.x, cell.y))
            )
            
            visual.transform = transform
        
        self.canvas.update()
    
    def toggle_animation(self):
        self.enable_animation = not self.enable_animation
        self.animation_btn.setText(f"Animation: {'ON' if self.enable_animation else 'OFF'}")
        
        if self.enable_animation:
            self.last_frame_time = time.time()
            self.animation_value = 0.0
    
    def set_animation_speed(self, value):
        self.animation_speed = value / 1000.0  # Convert to reasonable range
    
    def toggle_audio(self):
        self.enable_audio = not self.enable_audio
        self.audio_btn.setText(f"Audio: {'ON' if self.enable_audio else 'OFF'}")
        
        if self.enable_audio:
            self.media_player.play()
        else:
            self.media_player.pause()
    
    def load_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.ogg)"
        )
        
        if file_path:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            
            if self.enable_audio:
                self.media_player.play()
    
    def regenerate_poster(self):
        # Clear previous visuals
        for visual, _ in self.image_visuals:
            visual.parent = None
        
        if self.use_variable_grid:
            self.grid_cells = self.layout_generator.generate_variable_grid(self.complexity)
        
        self.images = self.assign_images_to_cells()
        
        self.create_image_visuals()
    
        self.canvas.update()
    
    def export_poster(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Poster Image",
            "",
            "Images (*.png *.jpg *.svg)"
        )
        
        if file_path:
            # Render the scene to an image
            img = self.canvas.render()
            img = np.flipud(img)

            img = img[:, :, :3]  # Remove alpha channel if present
            img = img[:, :, ::-1]  # RGB to BGR
            
            cv2.imwrite(file_path, img)
            print(f"Poster exported to {file_path}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    dataset_root = "D:/Courses/UdeM IFT6251_AlgorithmicArt/Cours_1_work/SWArt Works/DataBased/anime_dataset"
    metadata_path = "D:/Courses/UdeM IFT6251_AlgorithmicArt/Cours_1_work/SWArt Works/DataBased/metadata.json"
    
    dataset = AnimeDataset(dataset_root, metadata_path)
    
    window_size = (900, 900)
    
    use_variable_grid = True
    complexity = 0.7
    
    poster_generator = AnimePosterGenerator(
        dataset,
        window_size,
        use_variable_grid=use_variable_grid,
        complexity=complexity
    )
    
    poster_generator.show()
    
    sys.exit(app.exec_())