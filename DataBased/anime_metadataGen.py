import os
import json
from pathlib import Path

def generate_anime_metadata(dataset_path):
    """
    Scans the anime_dataset directory structure and generates a metadata.json file
    
    Expected structure:
    /anime_dataset/
      /anime_name/
        image1.jpg
        image2.jpg
    
    Returns: Dictionary with metadata structure
    """
    metadata = {}
    
    # Get all anime directories
    anime_dirs = [d for d in os.listdir(dataset_path) 
                  if os.path.isdir(os.path.join(dataset_path, d))]
    
    for anime in anime_dirs:
        anime_path = os.path.join(dataset_path, anime)
        metadata[anime] = {
            "title": anime.replace("_", " ").title(),
            "data": {}
        }
        
        # Get all character directories for this anime
        # character_dirs = [d for d in os.listdir(anime_path) 
                        #  if os.path.isdir(os.path.join(anime_path, d))]
        
        # for character in character_dirs:
        #     character_path = os.path.join(anime_path, character)
            
        # Get all images for this character
        image_files = [f for f in os.listdir(anime_path) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        # Store relative paths to images
        image_paths = [str(Path(anime) / img) for img in image_files]
        
        metadata[anime]["data"] = {
            "name": anime.replace("_", " ").title(),
            "images": image_paths
        }
    
    return metadata

def save_metadata(metadata, output_path="D:/Courses/UdeM IFT6251_AlgorithmicArt/Cours_1_work/SWArt Works/DataBased/metadata.json"):
    """Saves the metadata dictionary to a JSON file"""
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to {output_path}")

if __name__ == "__main__":
    # Update this path to your dataset directory
    dataset_path = "D:/Courses/UdeM IFT6251_AlgorithmicArt/Cours_1_work/SWArt Works/DataBased/anime_dataset"
    
    metadata = generate_anime_metadata(dataset_path)
    save_metadata(metadata)
    
    # Print some statistics
    total_anime = len(metadata)
    total_characters = sum(len(anime_data["data"]) for anime_data in metadata.values())
    total_images = sum(
        len(anime_data["data"]["images"])
        for anime_data in metadata.values()
    )
    
    print(f"Dataset statistics:")
    print(f"- {total_anime} anime series")
    print(f"- {total_characters} characters")
    print(f"- {total_images} images")