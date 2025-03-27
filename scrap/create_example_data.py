#!/usr/bin/env python3
"""
Example Data Creator for Welsh Learning App

This script creates a directory structure with example data for the Welsh Learning App,
including multiple categories and vocabulary items with variations.
"""

import os
import json
import shutil
from pathlib import Path

# Configuration
BASE_DIR = Path("assets")

# Example categories with items
EXAMPLE_DATA = {
    "body-parts": {
        "name": "Body Parts",
        "items": {
            "head": {
                "welsh": "pen",
                "english_variations": ["head", "the head", "a head", "your head"],
                "welsh_variations": ["pen", "y pen", "dy ben", "eich pen"]
            },
            "eye": {
                "welsh": "llygad",
                "english_variations": ["eye", "the eye", "an eye", "your eye"],
                "welsh_variations": ["llygad", "y llygad", "dy lygad", "eich llygad"]
            },
            "ear": {
                "welsh": "clust",
                "english_variations": ["ear", "the ear", "an ear", "your ear"],
                "welsh_variations": ["clust", "y glust", "dy glust", "eich clust"]
            },
            "nose": {
                "welsh": "trwyn",
                "english_variations": ["nose", "the nose", "a nose", "your nose"],
                "welsh_variations": ["trwyn", "y trwyn", "dy drwyn", "eich trwyn"]
            },
            "mouth": {
                "welsh": "ceg",
                "english_variations": ["mouth", "the mouth", "a mouth", "your mouth"],
                "welsh_variations": ["ceg", "y geg", "dy geg", "eich ceg"]
            }
        }
    },
    "colors": {
        "name": "Colors",
        "items": {
            "red": {
                "welsh": "coch",
                "english_variations": ["red", "the color red", "red color"],
                "welsh_variations": ["coch", "y lliw coch", "lliw coch"]
            },
            "blue": {
                "welsh": "glas",
                "english_variations": ["blue", "the color blue", "blue color"],
                "welsh_variations": ["glas", "y lliw glas", "lliw glas"]
            },
            "green": {
                "welsh": "gwyrdd",
                "english_variations": ["green", "the color green", "green color"],
                "welsh_variations": ["gwyrdd", "y lliw gwyrdd", "lliw gwyrdd"]
            },
            "yellow": {
                "welsh": "melyn",
                "english_variations": ["yellow", "the color yellow", "yellow color"],
                "welsh_variations": ["melyn", "y lliw melyn", "lliw melyn"]
            },
            "black": {
                "welsh": "du",
                "english_variations": ["black", "the color black", "black color"],
                "welsh_variations": ["du", "y lliw du", "lliw du"]
            }
        }
    },
    "animals": {
        "name": "Animals",
        "items": {
            "cat": {
                "welsh": "cath",
                "english_variations": ["cat", "the cat", "a cat"],
                "welsh_variations": ["cath", "y gath", "ei gath"]
            },
            "dog": {
                "welsh": "ci",
                "english_variations": ["dog", "the dog", "a dog"],
                "welsh_variations": ["ci", "y ci", "ei gi"]
            },
            "bird": {
                "welsh": "aderyn",
                "english_variations": ["bird", "the bird", "a bird"],
                "welsh_variations": ["aderyn", "yr aderyn", "ei haderyn"]
            },
            "fish": {
                "welsh": "pysgodyn",
                "english_variations": ["fish", "the fish", "a fish"],
                "welsh_variations": ["pysgodyn", "y pysgodyn", "ei bysgodyn"]
            },
            "rabbit": {
                "welsh": "cwningen",
                "english_variations": ["rabbit", "the rabbit", "a rabbit"],
                "welsh_variations": ["cwningen", "y gwningen", "ei gwningen"]
            }
        }
    },
    "numbers": {
        "name": "Numbers",
        "items": {
            "one": {
                "welsh": "un",
                "english_variations": ["one", "the number one", "1"],
                "welsh_variations": ["un", "rhif un", "1"]
            },
            "two": {
                "welsh": "dau",
                "english_variations": ["two", "the number two", "2"],
                "welsh_variations": ["dau", "rhif dau", "2"]
            },
            "three": {
                "welsh": "tri",
                "english_variations": ["three", "the number three", "3"],
                "welsh_variations": ["tri", "rhif tri", "3"]
            },
            "four": {
                "welsh": "pedwar",
                "english_variations": ["four", "the number four", "4"],
                "welsh_variations": ["pedwar", "rhif pedwar", "4"]
            },
            "five": {
                "welsh": "pump",
                "english_variations": ["five", "the number five", "5"],
                "welsh_variations": ["pump", "rhif pump", "5"]
            }
        }
    }
}

# Placeholder content
PLACEHOLDER_IMAGE_CONTENT = "This is a placeholder image. Replace with a real image."
PLACEHOLDER_AUDIO_CONTENT = "This is a placeholder audio file. Replace with a real audio file."

def create_placeholder_file(filepath, content):
    """Create a file with placeholder content."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def create_directory_structure():
    """Create the entire directory structure with example data."""
    print("Creating directory structure with example data...")
    
    # Create base directory if it doesn't exist
    os.makedirs(BASE_DIR, exist_ok=True)
    
    # Create categories list
    categories = []
    
    # Process each category
    for category_id, category_data in EXAMPLE_DATA.items():
        # Add to categories list for categories.json
        categories.append({
            "id": category_id,
            "name": category_data["name"]
        })
        
        # Create category directory
        category_dir = BASE_DIR / category_id
        os.makedirs(category_dir, exist_ok=True)
        
        # Process each item in the category
        for item_id, item_data in category_data["items"].items():
            # Create item directory
            item_dir = category_dir / item_id
            os.makedirs(item_dir, exist_ok=True)
            
            # Create subdirectories
            os.makedirs(item_dir / "images", exist_ok=True)
            os.makedirs(item_dir / "english_audio", exist_ok=True)
            os.makedirs(item_dir / "welsh_audio", exist_ok=True)
            
            # Create english.txt with variations
            with open(item_dir / "english.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(item_data["english_variations"]))
            
            # Create welsh.txt with variations
            with open(item_dir / "welsh.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(item_data["welsh_variations"]))
            
            # Create placeholder files
            create_placeholder_file(
                item_dir / "images" / "placeholder.jpg",
                PLACEHOLDER_IMAGE_CONTENT
            )
            create_placeholder_file(
                item_dir / "english_audio" / "placeholder.mp3",
                PLACEHOLDER_AUDIO_CONTENT
            )
            create_placeholder_file(
                item_dir / "welsh_audio" / "placeholder.mp3",
                PLACEHOLDER_AUDIO_CONTENT
            )
            
            print(f"  Created item: {category_id}/{item_id}")
    
    # Create categories.json
    with open(BASE_DIR / "categories.json", 'w', encoding='utf-8') as f:
        json.dump({"categories": categories}, f, indent=2)
    
    print("\nDirectory structure creation complete!")
    print(f"Created {len(categories)} categories with example data.")
    print(f"Base directory: {BASE_DIR.absolute()}")

def main():
    """Main function to run the script."""
    # Check if directory exists and prompt if not empty
    if BASE_DIR.exists() and any(BASE_DIR.iterdir()):
        response = input(f"The directory '{BASE_DIR}' already exists and is not empty. Proceed anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    create_directory_structure()

if __name__ == "__main__":
    main()
