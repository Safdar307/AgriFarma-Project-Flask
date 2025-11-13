#!/usr/bin/env python3
"""
Script to fix consultant profile picture paths in the database.
This updates the full filesystem paths to relative paths that work with Flask's static file serving.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Import the app and models
from app import app, db
from models.consultant import Consultant

def fix_consultant_paths():
    """Update consultant profile picture paths to use relative paths from static directory"""
    
    with app.app_context():
        print("Updating consultant profile picture paths...")
        
        # Get all consultants with profile pictures
        consultants = Consultant.query.filter(Consultant.profile_picture.isnot(None)).all()
        
        updated_count = 0
        for consultant in consultants:
            if consultant.profile_picture:
                print(f"Found consultant {consultant.name} with path: {consultant.profile_picture}")
                
                # Check if it's a full path that needs to be converted
                # Handle both forward slashes and backslashes
                if consultant.profile_picture.startswith('static/') or consultant.profile_picture.startswith('static\\'):
                    # Convert to relative path from static directory
                    # Remove 'static/' or 'static\' prefix
                    if consultant.profile_picture.startswith('static/'):
                        new_path = consultant.profile_picture.replace('static/', '')
                    else:
                        new_path = consultant.profile_picture.replace('static\\', '')
                    
                    # Normalize path separators to forward slashes for web compatibility
                    new_path = new_path.replace('\\', '/')
                    
                    consultant.profile_picture = new_path
                    updated_count += 1
                    print(f"Updated {consultant.name}: {consultant.profile_picture}")
        
        # Commit the changes
        db.session.commit()
        print(f"Successfully updated {updated_count} consultant profile picture paths!")
        
        # Show current state
        print("\nCurrent consultant profile pictures:")
        consultants = Consultant.query.filter(Consultant.profile_picture.isnot(None)).all()
        for consultant in consultants:
            print(f"- {consultant.name}: {consultant.profile_picture}")

if __name__ == "__main__":
    fix_consultant_paths()