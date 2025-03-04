from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from vispy import scene, app
import cv2
import sys
import os
import random
import numpy as np
from anime_dataset import AnimeDataset

class GridCell:
    """Represents a cell in the poster grid with position and size information"""
    def __init__(self, x, y, width, height, weight=1.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.weight = weight
        
    def __repr__(self): # for debugging
        return f"GridCell(x={self.x}, y={self.y}, w={self.width}, h={self.height})"


class PosterLayoutGenerator:
    
    def __init__(self, canvas_width, canvas_height, min_cell_width=0.2, min_cell_height=0.2):
        
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.min_cell_width_frac = min_cell_width
        self.min_cell_height_frac = min_cell_height
        
    def generate_variable_grid(self, complexity=0.5):
        
        # Approach: Binary space partitioning
        min_cell_width = int(self.canvas_width * self.min_cell_width_frac)
        min_cell_height = int(self.canvas_height * self.min_cell_height_frac)
        
        cells = [GridCell(0, 0, self.canvas_width, self.canvas_height)]
        
        num_splits = int(5 + complexity * 15)
        
        # Binary splits
        for _ in range(num_splits):
            if not cells:
                break
                
            cell_weights = [cell.width * cell.height for cell in cells]
            cell_index = random.choices(range(len(cells)), weights=cell_weights)[0]
            cell = cells.pop(cell_index)
            
            # Split orientation
            if cell.width >= cell.height:
                split_horizontal = True
            elif cell.width < cell.height:
                split_horizontal = False
            
            if split_horizontal and cell.width < min_cell_width * 2:
                cells.append(cell)
    
            elif not split_horizontal and cell.height < min_cell_height * 2:
                cells.append(cell)
            
            # Split position
            margin = 0.3
            if split_horizontal:
                min_split = int(cell.width * margin)
                max_split = int(cell.width * (1 - margin))
                if max_split <= min_split:
                    split_pos = cell.width // 2
                else:
                    split_pos = random.randint(min_split, max_split)
                    
                # New cells (horizontal split)
                cells.append(GridCell(cell.x, cell.y, split_pos, cell.height))
                cells.append(GridCell(cell.x + split_pos, cell.y, cell.width - split_pos, cell.height))
            else:
                min_split = int(cell.height * margin)
                max_split = int(cell.height * (1 - margin))
                if max_split <= min_split:
                    split_pos = cell.height // 2
                else:
                    split_pos = random.randint(min_split, max_split)
                    
                # New cells (vertical split)
                cells.append(GridCell(cell.x, cell.y, cell.width, split_pos))
                cells.append(GridCell(cell.x, cell.y + split_pos, cell.width, cell.height - split_pos))
        
        # Weights assignment: larger cells get more weight
        total_area = sum(cell.width * cell.height for cell in cells)
        for cell in cells:
            cell.weight = (cell.width * cell.height) / total_area
            
        return cells


class AnimePosterGenerator(QMainWindow):
    def __init__(self, dataset, window_size, use_variable_grid=True, complexity=0.7, 
                 enable_animation=False):
        super().__init__()
        self.dataset = dataset
        self.window_size = window_size
        self.use_variable_grid = use_variable_grid
        self.complexity = complexity
        self.enable_animation = enable_animation
        
        self.layout_generator = PosterLayoutGenerator(window_size[0], window_size[1])
        if use_variable_grid:
            self.grid_cells = self.layout_generator.generate_variable_grid(complexity)
        else:
            # Create regular grid (3x3 for example)
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
        
        self.images = self.assign_images_to_cells()
        
        # Initialize UI
        self.init_ui()
        
        # Animation
        if self.enable_animation:
            self.animation_timer = QTimer(self)
            self.animation_timer.timeout.connect(self.update_animation)
            self.animation_timer.start(0) 
            self.animation_step = 0
            self.animation_direction = 1  # 1 for growing, -1 for shrinking
        
    def assign_images_to_cells(self):
        images = []
        
        num_cells = len(self.grid_cells)
        
        use_same_anime = random.random() < 0.3  # 30% chance to use same anime
        
        try:
            if use_same_anime:
                anime_list = self.dataset.get_anime_list()
                for anime in random.sample(anime_list, len(anime_list)):
                    # Get all images for this anime
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
        self.canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='black')
    
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(aspect=1)
        self.view.camera.set_range(x=(0, self.window_size[0]), y=(0, self.window_size[1]), margin=0)
        
        self.setWindowTitle('Anime Poster Generator')
        self.setGeometry(700, 800, self.window_size[0], self.window_size[1])
        
        self.image_visuals = []
        for i, (cell, (anime, image_path)) in enumerate(zip(self.grid_cells, self.images)):
            image = self.load_and_fit_image(image_path, cell)
            
            if image is not None:
                image_visual = scene.visuals.Image(
                    image, 
                    parent=self.view.scene
                )
                image_visual.transform = scene.transforms.STTransform(
                    translate=(cell.x, cell.y)
                )
                self.image_visuals.append(image_visual)
            else:
                print(f"Warning: Failed to load image at {image_path}")
        
        self.setCentralWidget(self.canvas.native)
        
    def load_and_fit_image(self, image_path, cell):
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None
                
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
                return cropped_image
            
            return resized_image
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None
    
    def update_animation(self):
        if not self.enable_animation:
            return
            
        self.animation_step += 0.05 * self.animation_direction
        
        if self.animation_step > 1.0:
            self.animation_direction = -1
        elif self.animation_step < 0.0:
            self.animation_direction = 1
        
        scale_factor = 1.0 + 0.1 * self.animation_step  # 1.0 and 1.1
        
        for i, visual in enumerate(self.image_visuals):
            cell = self.grid_cells[i]
            
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    dataset_root = "D:/Courses/UdeM IFT6251_AlgorithmicArt/Cours_1_work/SWArt Works/DataBased/anime_dataset"
    metadata_path = "D:/Courses/UdeM IFT6251_AlgorithmicArt/Cours_1_work/SWArt Works/DataBased/metadata.json"
    
    dataset = AnimeDataset(dataset_root, metadata_path)
    
    window_size = (900, 900)

    use_variable_grid = True
    complexity = 0.7  
    enable_animation = True
    
    poster_generator = AnimePosterGenerator(
        dataset, 
        window_size, 
        use_variable_grid=use_variable_grid,
        complexity=complexity,
        enable_animation=enable_animation
    )
    
    poster_generator.show()
    
    sys.exit(app.exec_())