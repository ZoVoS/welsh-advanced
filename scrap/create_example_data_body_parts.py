#!/usr/bin/env python3
"""
Example Data Creator for Welsh Learning App

This script creates a directory structure with example data for the Welsh Learning App,
including multiple categories with body parts as the primary focus.
"""

import os
import json
import shutil
from pathlib import Path

# Configuration
BASE_DIR = Path("assets")

# Body parts with their Welsh translations
BODY_PARTS = {
    "ankle": {
        "welsh": "pigwrn",
        "english_variations": ["ankle", "the ankle", "an ankle", "your ankle"],
        "welsh_variations": ["pigwrn", "y pigwrn", "dy bigwrn", "eich pigwrn"]
    },
    "arm": {
        "welsh": "braich",
        "english_variations": ["arm", "the arm", "an arm", "your arm"],
        "welsh_variations": ["braich", "y fraich", "dy fraich", "eich braich"]
    },
    "arms": {
        "welsh": "breichiau",
        "english_variations": ["arms", "the arms", "your arms"],
        "welsh_variations": ["breichiau", "y breichiau", "dy freichiau", "eich breichiau"]
    },
    "back": {
        "welsh": "cefn",
        "english_variations": ["back", "the back", "your back"],
        "welsh_variations": ["cefn", "y cefn", "dy gefn", "eich cefn"]
    },
    "bottom": {
        "welsh": "pen-ôl",
        "english_variations": ["bottom", "the bottom", "your bottom"],
        "welsh_variations": ["pen-ôl", "y pen-ôl", "dy ben-ôl", "eich pen-ôl"]
    },
    "cheek": {
        "welsh": "boch",
        "english_variations": ["cheek", "the cheek", "a cheek", "your cheek"],
        "welsh_variations": ["boch", "y foch", "dy foch", "eich boch"]
    },
    "cheeks": {
        "welsh": "bochau",
        "english_variations": ["cheeks", "the cheeks", "your cheeks"],
        "welsh_variations": ["bochau", "y bochau", "dy fochau", "eich bochau"]
    },
    "chin": {
        "welsh": "gên",
        "english_variations": ["chin", "the chin", "your chin"],
        "welsh_variations": ["gên", "yr ên", "dy ên", "eich gên"]
    },
    "ear": {
        "welsh": "clust",
        "english_variations": ["ear", "the ear", "an ear", "your ear"],
        "welsh_variations": ["clust", "y glust", "dy glust", "eich clust"]
    },
    "ears": {
        "welsh": "clustiau",
        "english_variations": ["ears", "the ears", "your ears"],
        "welsh_variations": ["clustiau", "y clustiau", "dy glustiau", "eich clustiau"]
    },
    "elbow": {
        "welsh": "penelin",
        "english_variations": ["elbow", "the elbow", "an elbow", "your elbow"],
        "welsh_variations": ["penelin", "y benelin", "dy benelin", "eich penelin"]
    },
    "eye": {
        "welsh": "llygad",
        "english_variations": ["eye", "the eye", "an eye", "your eye"],
        "welsh_variations": ["llygad", "y llygad", "dy lygad", "eich llygad"]
    },
    "eyes": {
        "welsh": "llygaid",
        "english_variations": ["eyes", "the eyes", "your eyes"],
        "welsh_variations": ["llygaid", "y llygaid", "dy lygaid", "eich llygaid"]
    },
    "finger": {
        "welsh": "bys",
        "english_variations": ["finger", "the finger", "a finger", "your finger"],
        "welsh_variations": ["bys", "y bys", "dy fys", "eich bys"]
    },
    "fingers": {
        "welsh": "bysedd",
        "english_variations": ["fingers", "the fingers", "your fingers"],
        "welsh_variations": ["bysedd", "y bysedd", "dy fysedd", "eich bysedd"]
    },
    "foot": {
        "welsh": "troed",
        "english_variations": ["foot", "the foot", "a foot", "your foot"],
        "welsh_variations": ["troed", "y droed", "dy droed", "eich troed"]
    },
    "feet": {
        "welsh": "traed",
        "english_variations": ["feet", "the feet", "your feet"],
        "welsh_variations": ["traed", "y traed", "dy draed", "eich traed"]
    },
    "hair": {
        "welsh": "gwallt",
        "english_variations": ["hair", "the hair", "your hair"],
        "welsh_variations": ["gwallt", "y gwallt", "dy wallt", "eich gwallt"]
    },
    "hand": {
        "welsh": "llaw",
        "english_variations": ["hand", "the hand", "a hand", "your hand"],
        "welsh_variations": ["llaw", "y llaw", "dy law", "eich llaw"]
    },
    "hands": {
        "welsh": "dwylo",
        "english_variations": ["hands", "the hands", "your hands"],
        "welsh_variations": ["dwylo", "y dwylo", "dy ddwylo", "eich dwylo"]
    },
    "head": {
        "welsh": "pen",
        "english_variations": ["head", "the head", "a head", "your head"],
        "welsh_variations": ["pen", "y pen", "dy ben", "eich pen"]
    },
    "knee": {
        "welsh": "pen-glin",
        "english_variations": ["knee", "the knee", "a knee", "your knee"],
        "welsh_variations": ["pen-glin", "y pen-glin", "dy ben-glin", "eich pen-glin"]
    },
    "knees": {
        "welsh": "penliniau",
        "english_variations": ["knees", "the knees", "your knees"],
        "welsh_variations": ["penliniau", "y penliniau", "dy benliniau", "eich penliniau"]
    },
    "leg": {
        "welsh": "coes",
        "english_variations": ["leg", "the leg", "a leg", "your leg"],
        "welsh_variations": ["coes", "y goes", "dy goes", "eich coes"]
    },
    "legs": {
        "welsh": "coesau",
        "english_variations": ["legs", "the legs", "your legs"],
        "welsh_variations": ["coesau", "y coesau", "dy goesau", "eich coesau"]
    },
    "mouth": {
        "welsh": "ceg",
        "english_variations": ["mouth", "the mouth", "a mouth", "your mouth"],
        "welsh_variations": ["ceg", "y geg", "dy geg", "eich ceg"]
    },
    "neck": {
        "welsh": "gwddf",
        "english_variations": ["neck", "the neck", "a neck", "your neck"],
        "welsh_variations": ["gwddf", "y gwddf", "dy wddf", "eich gwddf"]
    },
    "nose": {
        "welsh": "trwyn",
        "english_variations": ["nose", "the nose", "a nose", "your nose"],
        "welsh_variations": ["trwyn", "y trwyn", "dy drwyn", "eich trwyn"]
    },
    "shoulder": {
        "welsh": "ysgwydd",
        "english_variations": ["shoulder", "the shoulder", "a shoulder", "your shoulder"],
        "welsh_variations": ["ysgwydd", "yr ysgwydd", "dy ysgwydd", "eich ysgwydd"]
    },
    "shoulders": {
        "welsh": "ysgwyddau",
        "english_variations": ["shoulders", "the shoulders", "your shoulders"],
        "welsh_variations": ["ysgwyddau", "yr ysgwyddau", "dy ysgwyddau", "eich ysgwyddau"]
    },
    "stomach": {
        "welsh": "bola",
        "english_variations": ["stomach", "the stomach", "a stomach", "your stomach"],
        "welsh_variations": ["bola", "y bola", "dy fola", "eich bola"]
    },
    "teeth": {
        "welsh": "dannedd",
        "english_variations": ["teeth", "the teeth", "your teeth"],
        "welsh_variations": ["dannedd", "y dannedd", "dy ddannedd", "eich dannedd"]
    },
    "thumb": {
        "welsh": "bawd",
        "english_variations": ["thumb", "the thumb", "a thumb", "your thumb"],
        "welsh_variations": ["bawd", "y fawd", "dy fawd", "eich bawd"]
    },
    "tongue": {
        "welsh": "tafod",
        "english_variations": ["tongue", "the tongue", "a tongue", "your tongue"],
        "welsh_variations": ["tafod", "y tafod", "dy dafod", "eich tafod"]
    },
    "tooth": {
        "welsh": "dant",
        "english_variations": ["tooth", "the tooth", "a tooth", "your tooth"],
        "welsh_variations": ["dant", "y dant", "dy ddant", "eich dant"]
    }
}

# Example categories with items
EXAMPLE_DATA = {
    "body-parts": {
        "name": "Body Parts",
        "items": BODY_PARTS
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
