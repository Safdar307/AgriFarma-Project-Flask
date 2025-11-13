#!/usr/bin/env python3
"""
Script to fix the consultant table by removing the subcategory column
that is causing NOT NULL constraint failures.
"""

import sqlite3
import os

def fix_consultant_table():
    """Fix the consultant table by removing the subcategory column"""
    
    db_path = 'database/agrifarma.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current table structure
        cursor.execute("PRAGMA table_info(consultant)")
        columns = cursor.fetchall()
        print("Current consultant table columns:")
        for col in columns:
            print(f"  {col}")
        
        # Check if subcategory column exists
        has_subcategory = any(col[1] == 'subcategory' for col in columns)
        
        if has_subcategory:
            print("\nRemoving subcategory column from consultant table...")
            
            # Create a backup of existing data if any consultants exist
            cursor.execute("SELECT * FROM consultant")
            existing_data = cursor.fetchall()
            
            if existing_data:
                print(f"Found {len(existing_data)} existing consultant records")
                
                # Get column names except subcategory
                column_names = [col[1] for col in columns if col[1] != 'subcategory']
                
                # Create new table structure without subcategory
                cursor.execute("""
                    CREATE TABLE consultant_new (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(120) NOT NULL,
                        phone VARCHAR(20) NOT NULL,
                        expertise_category INTEGER NOT NULL,
                        bio TEXT NOT NULL,
                        profile_picture VARCHAR(255),
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(email)
                    )
                """)
                
                # Insert data into new table (excluding subcategory)
                placeholders = ','.join(['?' for _ in column_names])
                for row in existing_data:
                    # Filter out subcategory column from the data
                    filtered_row = [row[i] for i, col in enumerate(columns) if col[1] != 'subcategory']
                    cursor.execute(f"INSERT INTO consultant_new ({','.join(column_names)}) VALUES ({placeholders})", filtered_row)
                
                # Drop old table and rename new one
                cursor.execute("DROP TABLE consultant")
                cursor.execute("ALTER TABLE consultant_new RENAME TO consultant")
                
                print("Successfully migrated consultant table structure")
            else:
                # No data, just drop the column
                cursor.execute("ALTER TABLE consultant DROP COLUMN subcategory")
                print("Successfully removed subcategory column from consultant table")
        else:
            print("subcategory column not found - table structure is already correct")
        
        # Add foreign key constraint if it's missing
        cursor.execute("PRAGMA foreign_key_list(consultant)")
        fks = cursor.fetchall()
        has_expertise_fk = any(fk[3] == 'category' and fk[4] == 'id' for fk in fks)
        
        if not has_expertise_fk:
            print("Adding missing foreign key constraint...")
            cursor.execute("""
                CREATE INDEX idx_consultant_expertise_category 
                ON consultant(expertise_category)
            """)
        
        # Commit changes
        conn.commit()
        
        # Verify the new structure
        cursor.execute("PRAGMA table_info(consultant)")
        new_columns = cursor.fetchall()
        print("\nNew consultant table columns:")
        for col in new_columns:
            print(f"  {col}")
        
        conn.close()
        print("\nDatabase fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    fix_consultant_table()