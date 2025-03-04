import json
import random
import os
from typing import List, Dict, Any, Optional, Tuple

class AnimeDataset:
    def __init__(self, dataset_root: str, metadata_path: str):
        """
        Initialize the anime character dataset manager
        
        Args:
            dataset_root: Root directory containing the anime images
            metadata_path: Path to the metadata.json file
        """
        self.dataset_root = dataset_root
        self.metadata_path = metadata_path
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, Any]:
        with open(self.metadata_path, 'r') as f:
            return json.load(f)
    
    def get_anime_list(self) -> List[str]:
        return list(self.metadata.keys())
    
    # def get_characters_for_anime(self, anime_name: str) -> List[str]:
    #     """Get a list of all character names for a specific anime"""
    #     if anime_name not in self.metadata:
    #         return []
        
    #     return list(self.metadata[anime_name]["characters"].keys())
    
    def get_anime_image_paths(self, anime_name: str) -> List[str]:
        if (anime_name not in self.metadata):
            return []
        
        relative_paths = self.metadata[anime_name]["data"]["images"]
        absolute_paths = [os.path.join(self.dataset_root, path) for path in relative_paths]
        return absolute_paths
    
    def get_random_anime_image(self, anime_name: Optional[str] = None) -> str:
    
        if anime_name:
            image_paths = self.get_anime_image_paths(anime_name)
            if not image_paths:
                raise ValueError(f"No images found for {anime_name}")
            return random.choice(image_paths)
        
        anime = random.choice(self.get_anime_list())
        return self.get_random_anime_image(anime)
    
    def get_anime_info(self, anime_name: str) -> Dict[str, Any]:
        if (anime_name not in self.metadata):
            return {}
        
        return self.metadata[anime_name]["data"]
    
    def get_random_character_set(self, count: int,
                               from_same_anime: bool = False) -> List[Tuple[str, str]]:
        """
        Get a set of random characters
        
        Args:
            count: Number of characters to return
            from_same_anime: If True, all characters will be from the same anime
            
        Returns:
            List of tuples (anime_name, image_path)
        """
        if from_same_anime:
            # Pick a random anime with enough characters
            valid_animes = [
                anime for anime in self.get_anime_list()
                if len(self.get_anime_image_paths(anime)) >= count
            ]
            
            if not valid_animes:
                raise ValueError(f"No valid anime found")
                
            anime = random.choice(valid_animes)
            images = random.sample(self.get_anime_image_paths(anime), count)
            
            return [(anime, images)]
                
        else:
            # Pick random images from any anime
            result = []
            available_animes = self.get_anime_list()
            
            for _ in range(count):
                anime = random.choice(available_animes)
                image_path = self.get_random_anime_image(anime)
                result.append((anime, image_path))
                
            return result