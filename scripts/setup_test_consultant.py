from app import app, db
from models.category import Category, SubCategory
from models.consultant import Consultant

def create_test_data():
    with app.app_context():
        # Create a test category
        category = Category(name='Agriculture', description='Agricultural consulting')
        db.session.add(category)
        db.session.commit()

        # Create a test subcategory
        subcategory = SubCategory(name='Crop Management', description='Crop management consulting', category_id=category.id)
        db.session.add(subcategory)
        db.session.commit()

        # Create a test consultant
        consultant = Consultant(
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            expertise_category=category.id,
            subcategory=subcategory.id,
            bio='Experienced agricultural consultant',
            status='approved'
        )
        db.session.add(consultant)
        db.session.commit()

if __name__ == '__main__':
    create_test_data()