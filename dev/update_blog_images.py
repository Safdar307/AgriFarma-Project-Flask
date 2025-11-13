"""
Script to update existing blog posts with correct images
Run with: python update_blog_images.py
"""

from app import app
from db import db
from models.post import Post
from models.blog_media import BlogMedia

with app.app_context():
    # Image mapping for blog posts
    image_mapping = {
        'Benefits of Organic Farming in Modern Agriculture': 'images/blogs/Benefits of Organic Farming in Modern Agriculture.jpeg',
        'IoT and Smart Sensors Revolutionizing Crop Monitoring': 'images/blogs/IoT and Smart Sensors Revolutionizing Crop Monitoring.jpeg',
        'Efficient Irrigation Systems for Water Conservation': 'images/blogs/Efficient Irrigation Systems for Water Conservation.jpeg',
        'Understanding Soil Health and Its Impact on Crops': 'images/blogs/Understanding Soil Health and Its Impact on Crops.jpeg',
        'Integrated Pest Management Strategies': 'images/blogs/Integrated Pest Management Strategies.png',
        'Seasonal Crop Planning and Rotation Techniques': 'images/blogs/Seasonal Crop Planning and Rotation Techniques.png'
    }
    
    print("[UPDATING] Blog post images...")
    
    # Get all posts and update their media
    posts = Post.query.all()
    updated_count = 0
    
    for post in posts:
        # Delete existing media for this post
        existing_media = BlogMedia.query.filter_by(post_id=post.id).all()
        for media in existing_media:
            db.session.delete(media)
        
        # Add new media with correct image
        if post.title in image_mapping:
            new_media = BlogMedia(
                post_id=post.id,
                file_path=image_mapping[post.title],
                media_type='image'
            )
            db.session.add(new_media)
            updated_count += 1
            print(f"[UPDATED] {post.title}")
        else:
            print(f"[SKIPPED] {post.title} (no matching image)")
    
    db.session.commit()
    print(f"\n[SUCCESS] Updated {updated_count} blog posts with correct images!")