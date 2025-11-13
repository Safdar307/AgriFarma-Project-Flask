# Blog Feature Setup & Migration Guide

## Recent Updates (Nov 11, 2025)

The blog feature has been redesigned and extended with the following:

### New Features
- **Reply System**: Users can reply to comments, creating threaded discussion threads.
- **Like System**: Users can like posts (API endpoint provides JSON response).
- **Modern Templates**: Responsive design with media gallery carousel, tags, category filters, and live search.
- **Admin Moderation**: Admin can delete posts, comments, and replies; manage categories.

### New Models & Files
- `models/comment_reply.py` - CommentReply model for nested comments
- `models/like.py` - Like model for post/comment likes
- `models/tag.py` - Tag model (prepared for future tag-based filtering)
- Updated `templates/blog_list.html` - Modern responsive blog listing with search/filter
- Updated `templates/blog_post.html` - Post view with media carousel, replies, and likes
- New routes in `routes/blog_routes.py`:
  - `POST /blog/like/<post_id>` - Like a post (returns JSON)
  - `POST /blog/comment/<comment_id>/reply` - Reply to a comment

---

## Database Migration Steps

### Prerequisites
- Python 3.8+
- Flask app running (verify with `pip list | grep Flask`)
- SQLite database initialized

### Apply Migration

1. **Backup your database (optional but recommended)**:
   ```powershell
   Copy-Item instance/blog.db instance/blog.db.backup
   ```

2. **Apply the migration**:
   ```powershell
   cd C:\Users\safda\OneDrive\Desktop\AgriFarma_starter
   flask db upgrade
   ```

3. **Verify the migration succeeded**:
   ```powershell
   flask shell
   ```
   Inside the Flask shell:
   ```python
   from db import db
   from models.comment_reply import CommentReply
   db.inspect(db.engine)  # or query the DB to confirm comment_reply table exists
   exit()
   ```

### Rollback (if needed)
If something goes wrong, rollback the migration:
```powershell
flask db downgrade
```

---

## Testing the New Features

### 1. Test Comment Replies
```bash
# Create a blog post, then a comment, then reply to that comment via POST to:
# /blog/comment/{comment_id}/reply
```

### 2. Test Like API
```bash
# Send a POST request to /blog/like/{post_id}
# Expected response (JSON):
{
  "success": true,
  "action": "liked",  // or "unliked"
  "count": 5
}
```

### 3. Verify Templates Render
- Visit http://127.0.0.1:5000/blog to see the new blog listing
- Click on a post to see the post view with media carousel and reply forms

---

## Architecture Overview

### Comment Threading
- `BlogComment` table: stores top-level comments on posts
- `CommentReply` table: stores replies to comments (linked via `comment_id` FK)
- Template renders replies nested under their parent comment with inline reply forms

### Likes
- `Like` model: tracks user likes on posts/comments
- `POST /blog/like/<post_id>` endpoint: toggles like (creates/deletes Like record)
- Returns JSON so frontend can update UI via AJAX without page reload

### Search & Filtering
- Server-side search in `blog_list()` endpoint (searches title, body, tags)
- Category filtering via `?cat={category_id}` query parameter
- Live search (JavaScript) on blog listing page

---

## Next Steps (Optional Enhancements)

1. **AJAX Reply/Like UI**: Wire the reply forms and like button to use AJAX instead of page reloads
   - Replace form posts with `fetch()` calls
   - Update counts in-place

2. **Tag System**: Implement tag-based filtering (Tag model already exists)
   - Parse post tags and filter by tag query param

3. **Pagination**: Implement proper pagination using Flask-SQLAlchemy's `paginate()`

4. **Admin Dashboard Stats**: Add blog stats (post count, recent activity) to admin dashboard

5. **Upload Validation**: Add file size limits, MIME type validation, image thumbnail generation

---

## Database Schema (comment_reply table)

```sql
CREATE TABLE comment_reply (
    id INTEGER PRIMARY KEY,
    comment_id INTEGER NOT NULL REFERENCES blog_comment(id),
    author_id INTEGER REFERENCES user(id),
    author_name VARCHAR(120),
    body TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Troubleshooting

### Migration fails: "table comment_reply already exists"
- Your database may already have this table from a previous attempt
- Rollback and retry, or manually drop the table if needed

### Replies don't show in template
- Ensure migration has been applied (`flask db upgrade`)
- Check that `BlogComment` model has the `replies` relationship defined
- Verify `comment_reply.py` is in `models/` folder

### Like endpoint returns 401
- User is not logged in; ensure `session.get('user_id')` is set
- Test: login first, then try liking

### Template syntax errors
- Verify `{% block content %}` and `{% endblock %}` are balanced in templates
- Check for unclosed Jinja2 tags (e.g., missing `{% endif %}`)

---

## File Locations

- Models: `models/`
- Routes: `routes/blog_routes.py`
- Templates: `templates/blog_list.html`, `templates/blog_post.html`
- Migrations: `migrations/versions/`

---

## Support

For questions or issues, check:
1. Flask error logs in the terminal
2. Browser console for JavaScript errors
3. Database logs (if applicable)

---

Generated: November 11, 2025
