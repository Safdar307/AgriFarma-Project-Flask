#!/usr/bin/env python3
"""
Script to fix blog media image paths in the database.
This updates the file paths to use images from static/images/ directory.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Import the app and models
from app import app, db
from models.blog_media import BlogMedia

def fix_blog_image_paths():
    """Update blog media paths to use images from static/images/ directory"""
    
    with app.app_context():
        print("Fixing blog media image paths...")
        
        # Get all blog media
        all_media = BlogMedia.query.all()
        
        print(f"Found {len(all_media)} media items in database")
        
        # Get available images from static/images
        images_dir = os.path.join('static', 'images')
        available_images = []
        if os.path.exists(images_dir):
            for filename in os.listdir(images_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    available_images.append(filename)
        
        print(f"Available images in static/images/: {available_images}")
        
        # Update existing media items with proper paths
        updated_count = 0
        for i, media in enumerate(all_media):
            if media.media_type == 'image':
                # Use available images in rotation
                image_filename = available_images[i % len(available_images)] if available_images else 'placeholder-800x450.png'
                new_path = f"images/{image_filename}"
                
                print(f"Updating media ID {media.id}: {media.file_path} -> {new_path}")
                media.file_path = new_path
                updated_count += 1
        
        # Commit the changes
        db.session.commit()
        print(f"Successfully updated {updated_count} blog media image paths!")
        
        # Show current state
        print("\nCurrent blog media items:")
        media_items = BlogMedia.query.all()
        for media in media_items:
            print(f"- ID {media.id}: {media.file_path} ({media.media_type})")

if __name__ == "__main__":
    fix_blog_image_paths()