import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app import app
from scripts.create_forum_categories import create_initial_categories

if __name__ == "__main__":
    with app.app_context():
        create_initial_categories()