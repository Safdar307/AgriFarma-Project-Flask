"""
Script to populate blog with dummy posts.
Run with: flask shell < dev/seed_dummy_blogs.py
Or: python -c "from app import app; from db import db; from models.post import Post; from models.blog_media import BlogMedia; from models.blog_taxonomy import BlogCategory; exec(open('dev/seed_dummy_blogs.py').read())"
"""

from app import app
from db import db
from models.post import Post
from models.blog_media import BlogMedia
from models.blog_taxonomy import BlogCategory
from datetime import datetime, timedelta

with app.app_context():
    # Check if posts already exist
    existing_count = Post.query.count()
    if existing_count > 0:
        print(f"[INFO] {existing_count} posts already exist. Skipping seed.")
    else:
        print("[CREATING] Dummy blog posts...")
        
        # Get or create categories
        categories = {}
        for cat_name in ['Organic Farming', 'AgriTech', 'Irrigation', 'Soil Management', 'Pest Management', 'Crop Cultivation']:
            cat = BlogCategory.query.filter_by(name=cat_name).first()
            if not cat:
                cat = BlogCategory(name=cat_name)
                db.session.add(cat)
                db.session.commit()
            categories[cat_name] = cat.id
        
        # Dummy posts data
        dummy_posts = [
            {
                'title': 'Benefits of Organic Farming in Modern Agriculture',
                'body': '''Organic farming has become increasingly important in recent years as farmers and consumers recognize the benefits of sustainable agricultural practices. By avoiding synthetic pesticides and fertilizers, organic farming promotes healthier soil, reduces environmental pollution, and produces nutritious crops.

Key benefits include:
• Improved soil health and fertility
• Reduced chemical residues in food
• Better taste and nutritional value
• Environmental conservation
• Long-term sustainability

Many farmers worldwide are transitioning to organic methods, and the results have been remarkable. Studies show that organic farms produce yields comparable to conventional farms while maintaining ecological balance.''',
                'author_name': 'Sarah Johnson',
                'category': 'Organic Farming',
                'tags': 'organic, sustainable, farming, health',
                'days_ago': 3
            },
            {
                'title': 'IoT and Smart Sensors Revolutionizing Crop Monitoring',
                'body': '''The Internet of Things (IoT) is transforming agriculture through real-time data collection and analysis. Smart sensors deployed across fields provide farmers with critical information about soil moisture, temperature, and crop health.

Applications of IoT in agriculture:
• Real-time soil moisture monitoring
• Automated irrigation systems
• Pest and disease detection
• Weather forecasting integration
• Yield prediction and optimization

With IoT technology, farmers can make data-driven decisions that maximize productivity while minimizing resource waste. This precision agriculture approach is revolutionizing how we grow food.''',
                'author_name': 'Dr. Ahmed Khan',
                'category': 'AgriTech',
                'tags': 'technology, IoT, precision farming, innovation',
                'days_ago': 5
            },
            {
                'title': 'Efficient Irrigation Systems for Water Conservation',
                'body': '''Water is one of the most precious resources in agriculture. With climate change bringing unpredictable weather patterns, efficient irrigation has become essential for sustainable farming.

Types of efficient irrigation systems:
• Drip irrigation - saves up to 50% water
• Sprinkler systems - better coverage and control
• Soil moisture sensors - prevent overwatering
• Mulching - reduces evaporation
• Rainwater harvesting - alternative water source

By implementing these systems, farmers can reduce water consumption by 30-50% while actually increasing crop yields. The investment in modern irrigation pays off quickly through water savings and improved productivity.''',
                'author_name': 'Maria Garcia',
                'category': 'Irrigation',
                'tags': 'water, conservation, irrigation, efficiency',
                'days_ago': 8
            },
            {
                'title': 'Understanding Soil Health and Its Impact on Crops',
                'body': '''Healthy soil is the foundation of productive agriculture. Soil health encompasses physical, chemical, and biological properties that affect plant growth and overall farm productivity.

Key indicators of healthy soil:
• Good soil structure and porosity
• Adequate organic matter (3-5%)
• Balanced pH levels
• Rich microbial populations
• Proper nutrient content

Soil testing should be done regularly to monitor these parameters. By maintaining soil health through proper practices like crop rotation, composting, and reduced tillage, farmers ensure long-term productivity and sustainability.

Investing in soil health today means healthier crops and better yields tomorrow.''',
                'author_name': 'Prof. James Miller',
                'category': 'Soil Management',
                'tags': 'soil, health, nutrients, testing',
                'days_ago': 10
            },
            {
                'title': 'Integrated Pest Management Strategies',
                'body': '''Integrated Pest Management (IPM) is a holistic approach to pest control that minimizes chemical use while maintaining crop productivity. IPM combines multiple strategies for effective, sustainable pest management.

IPM strategies:
• Cultural practices (crop rotation, sanitation)
• Biological control (beneficial insects, predators)
• Chemical control (only when necessary)
• Monitoring and scouting
• Resistant crop varieties

The benefits of IPM are significant:
- Reduced pesticide costs
- Lower environmental impact
- Healthier food products
- Better long-term pest control
- Improved farm profitability

By adopting IPM practices, farmers can achieve excellent pest control results while protecting beneficial insects and maintaining environmental health.''',
                'author_name': 'Emily Rodriguez',
                'category': 'Pest Management',
                'tags': 'pests, management, organic, sustainable',
                'days_ago': 12
            },
            {
                'title': 'Seasonal Crop Planning and Rotation Techniques',
                'body': '''Successful farming requires careful planning of which crops to plant in each season. Crop rotation and seasonal planning are fundamental practices that improve soil health and maximize yields.

Benefits of crop rotation:
• Maintains soil nutrient balance
• Breaks pest and disease cycles
• Reduces chemical inputs
• Improves soil structure
• Increases farm productivity

Seasonal planting guide:
Spring: Warm season crops (tomatoes, peppers, beans)
Summer: Continuation of spring crops, start fall crops
Fall: Cool season crops (lettuce, broccoli, spinach)
Winter: Cover crops, soil rest

By planning your crop calendar strategically, you can:
- Grow vegetables year-round
- Maintain soil fertility naturally
- Reduce pest pressures
- Optimize farm space usage
- Increase overall farm income

Remember: successful farming is successful planning!''',
                'author_name': 'David Chen',
                'category': 'Crop Cultivation',
                'tags': 'crops, rotation, planning, seasonal',
                'days_ago': 15
            }
        ]
        
        # Create posts
        for i, post_data in enumerate(dummy_posts, 1):
            created_at = datetime.utcnow() - timedelta(days=post_data['days_ago'])
            
            post = Post(
                title=post_data['title'],
                body=post_data['body'],
                author_id=1,  # Assuming user ID 1 exists
                author_name=post_data['author_name'],
                category=post_data['category'],
                category_id=categories.get(post_data['category']),
                tags=post_data['tags'],
                created_at=created_at
            )
            
            db.session.add(post)
            db.session.flush()  # Get the post ID
            
            # Add corresponding image for this blog post
            image_mapping = {
                'Benefits of Organic Farming in Modern Agriculture': 'images/blogs/Benefits of Organic Farming in Modern Agriculture.jpeg',
                'IoT and Smart Sensors Revolutionizing Crop Monitoring': 'images/blogs/IoT and Smart Sensors Revolutionizing Crop Monitoring.jpeg',
                'Efficient Irrigation Systems for Water Conservation': 'images/blogs/Efficient Irrigation Systems for Water Conservation.jpeg',
                'Understanding Soil Health and Its Impact on Crops': 'images/blogs/Understanding Soil Health and Its Impact on Crops.jpeg',
                'Integrated Pest Management Strategies': 'images/blogs/Integrated Pest Management Strategies.png',
                'Seasonal Crop Planning and Rotation Techniques': 'images/blogs/Seasonal Crop Planning and Rotation Techniques.png'
            }
            
            media = BlogMedia(
                post_id=post.id,
                file_path=image_mapping.get(post_data['title'], 'images/placeholder-800x450.png'),
                media_type='image'
            )
            db.session.add(media)
            
            print(f"[{i}/6] Created: {post_data['title']}")
        
        db.session.commit()
        print(f"\n[SUCCESS] Created {len(dummy_posts)} dummy blog posts!")
        print("[INFO] Posts are now visible at http://127.0.0.1:5000/blog")
