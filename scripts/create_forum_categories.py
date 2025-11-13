"""Add initial forum categories"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from db import db
from models.forum import ForumCategory

def create_initial_categories():
    # Main categories with descriptions
    farming = ForumCategory(
        name="Farming Techniques",
        description="Discuss various farming methods and techniques for better crop production"
    )
    livestock = ForumCategory(
        name="Livestock Management",
        description="All about raising and managing farm animals and dairy production"
    )
    tech = ForumCategory(
        name="Agricultural Technology",
        description="Modern farming technologies, equipment, and innovations"
    )
    market = ForumCategory(
        name="Market & Trade",
        description="Agricultural markets, prices, and trading opportunities"
    )
    sustainable = ForumCategory(
        name="Sustainable Agriculture",
        description="Eco-friendly farming practices and sustainability"
    )
    community = ForumCategory(
        name="Community Hub",
        description="Connect with fellow farmers, share experiences and get help"
    )
    
    db.session.add_all([farming, livestock, tech, market, sustainable, community])
    db.session.commit()
    
    # Sub-categories with descriptions
    # Farming sub-categories
    db.session.add_all([
        ForumCategory(
            name="Crop Cultivation",
            description="Tips and discussions about growing various crops",
            parent_id=farming.id
        ),
        ForumCategory(
            name="Soil Management",
            description="Soil health, fertilization, and improvement techniques",
            parent_id=farming.id
        ),
        ForumCategory(
            name="Irrigation Systems",
            description="Water management and irrigation technologies",
            parent_id=farming.id
        ),
        ForumCategory(
            name="Pest Control",
            description="Managing pests and protecting crops",
            parent_id=farming.id
        ),
        ForumCategory(
            name="Organic Farming",
            description="Chemical-free and natural farming methods",
            parent_id=farming.id
        )
    ])
    
    # Livestock sub-categories
    db.session.add_all([
        ForumCategory(
            name="Cattle Farming",
            description="Raising and managing cattle for dairy and meat",
            parent_id=livestock.id
        ),
        ForumCategory(
            name="Poultry",
            description="Chicken, duck, and other poultry farming",
            parent_id=livestock.id
        ),
        ForumCategory(
            name="Animal Health",
            description="Veterinary care and disease prevention",
            parent_id=livestock.id
        ),
        ForumCategory(
            name="Feed Management",
            description="Animal nutrition and feeding strategies",
            parent_id=livestock.id
        )
    ])
    
    # Tech sub-categories
    db.session.add_all([
        ForumCategory(
            name="Smart Farming",
            description="IoT, sensors, and precision agriculture",
            parent_id=tech.id
        ),
        ForumCategory(
            name="Farm Equipment",
            description="Machinery, tools, and equipment discussions",
            parent_id=tech.id
        ),
        ForumCategory(
            name="AgriTech Solutions",
            description="Software and technology solutions for farming",
            parent_id=tech.id
        ),
        ForumCategory(
            name="Automation",
            description="Automated systems and robotics in farming",
            parent_id=tech.id
        )
    ])
    
    # Market sub-categories
    db.session.add_all([
        ForumCategory(
            name="Price Discussion",
            description="Agricultural product pricing and negotiations",
            parent_id=market.id
        ),
        ForumCategory(
            name="Market Trends",
            description="Industry trends and market analysis",
            parent_id=market.id
        ),
        ForumCategory(
            name="Export/Import",
            description="International trade opportunities",
            parent_id=market.id
        ),
        ForumCategory(
            name="Local Markets",
            description="Connecting with local buyers and sellers",
            parent_id=market.id
        )
    ])
    
    # Sustainable sub-categories
    db.session.add_all([
        ForumCategory(
            name="Conservation",
            description="Resource conservation and biodiversity",
            parent_id=sustainable.id
        ),
        ForumCategory(
            name="Renewable Energy",
            description="Solar, wind, and other clean energy solutions",
            parent_id=sustainable.id
        ),
        ForumCategory(
            name="Water Management",
            description="Water conservation and efficient use",
            parent_id=sustainable.id
        ),
        ForumCategory(
            name="Climate Smart",
            description="Adapting farming to climate change",
            parent_id=sustainable.id
        )
    ])
    
    # Community sub-categories
    db.session.add_all([
        ForumCategory(
            name="Success Stories",
            description="Share your farming achievements and experiences",
            parent_id=community.id
        ),
        ForumCategory(
            name="Questions & Help",
            description="Get support from the farming community",
            parent_id=community.id
        ),
        ForumCategory(
            name="Events & Meetups",
            description="Agricultural events and farmer gatherings",
            parent_id=community.id
        ),
        ForumCategory(
            name="Knowledge Sharing",
            description="Share farming tips and best practices",
            parent_id=community.id
        )
    ])
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Check if categories already exist
        if ForumCategory.query.count() == 0:
            print("Creating initial forum categories...")
            create_initial_categories()
            print("Done!")
        else:
            print("Categories already exist!")