from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from vispy import scene
import cv2
import sys
import os
import random
from anime_dataset import AnimeDataset

class AnimeCharacterGrid(QMainWindow):
    def __init__(self, dataset, grid_size, window_size):
        super().__init__()
        self.dataset = dataset
        self.grid_size = grid_size
        self.window_size = window_size
        self.character_images = self.get_random_images()
        self.init_ui()

    def get_random_images(self):
        # Get total number of cells in the grid
        num_cells = self.grid_size[0] * self.grid_size[1]
        
        from_same_anime = random.choice([True, False])  # 50% chance for characters from same anime
        
        try:
            character_set = self.dataset.get_random_character_set(
                num_cells, from_same_anime=from_same_anime
            )
            return character_set
        except ValueError as e:
            # Fallback to mixed anime if we don't have enough characters
            print(f"Warning: {e}. Falling back to characters from mixed anime.")
            return self.dataset.get_random_character_set(num_cells, from_same_anime=False)
        
    def init_ui(self):
        canvas = scene.SceneCanvas(keys='interactive', show=True)
        grid = canvas.central_widget.add_grid(spacing=0)
        
        self.setWindowTitle('Anime Character Grid')
        self.setGeometry(500, 700, self.window_size[0], self.window_size[1])

        # Character counter for flat indexing
        char_idx = 0
        
        # Place images in grid
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if char_idx < len(self.character_images):
                    _, image_path = self.character_images[char_idx]
                    
                    # Load and convert image
                    image = cv2.imread(image_path)
                    if image is not None:
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        
                        # Create view for this grid cell
                        view = grid.add_view(row=i, col=j, border_color='white')
                        image_visual = scene.visuals.Image(image, parent=view.scene)
                        view.camera = scene.PanZoomCamera(aspect=1)
                        view.camera.set_range()
                        view.camera.flip = (0, 1, 0)
                        view.camera.set_range()
                    else:
                        print(f"Warning: Failed to load image at {image_path}")
                
                char_idx += 1
        
        self.setCentralWidget(canvas.native)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set these paths to match your setup
    dataset_root = "D:/Courses/UdeM IFT6251_AlgorithmicArt/Cours_1_work/SWArt Works/DataBased/anime_dataset"
    metadata_path = "D:/Courses/UdeM IFT6251_AlgorithmicArt/Cours_1_work/SWArt Works/DataBased/metadata.json"
    
    # Create the dataset loader
    dataset = AnimeDataset(dataset_root, metadata_path)
    
    # Create and show the grid
    grid_size = (3, 3)  # 3x3 grid
    window_size = (900, 900)  # 900x900 pixel window
    
    anime_grid = AnimeCharacterGrid(dataset, grid_size, window_size)
    
    sys.exit(app.exec_())