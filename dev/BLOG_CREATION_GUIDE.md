# Blog Post Creation Guide

## Where to Create a Blog Post

Users can now create blog posts from **two locations**:

### 1. **Public Blog Listing Page** (`/blog`)
- Click the **"Create Blog Post"** button in the hero section (top of page)
- White button with pen icon
- Visible to all logged-in users

### 2. **Admin Blog Management Page** (`/blog/admin/categories`)
- Click the **"Create New Post"** button (top-right)
- Blue primary button
- For admin users

---

## How to Create a Blog Post

1. **Click "Create Blog Post"** button from either location above
2. **Fill out the form:**
   - **Title** - Post title (required)
   - **Category** - Select a blog category
   - **Subcategory** - (optional) Select a subcategory
   - **Tags** - Comma-separated tags (e.g., "farming, irrigation, tips")
   - **Body** - Post content/article text
   - **Media** - Upload images, videos, audio, or documents

3. **Submit** - Click "Create Post"
4. **Success** - Redirected to post view with comment section

---

## Access Requirements

- **Must be logged in** to create posts
- **No admin role required** - any logged-in user can post
- Anonymous posts will show author as "Author" if not logged in

---

## Post Creation Form Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Title | Text | Yes | Post title |
| Category | Dropdown | No | Select from existing categories |
| Subcategory | Dropdown | No | Filter by selected category |
| Tags | Text | No | Comma-separated (e.g., "organic, farming") |
| Body | Textarea | Yes | Post content |
| Media | File upload | No | Support: jpg, png, gif, webp, mp4, webm, ogg, mp3, wav, pdf, doc, docx, ppt, pptx |

---

## Supported Media Types

### Images
- `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`

### Video
- `.mp4`, `.webm`, `.ogg`

### Audio
- `.mp3`, `.wav`

### Documents
- `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`

---

## Navigation

**Quick Links to Create Posts:**

1. **From Blog Listing:**
   - Visit http://127.0.0.1:5000/blog
   - Click "Create Blog Post" button

2. **From Admin Dashboard:**
   - Visit http://127.0.0.1:5000/admin
   - Click "Our Blogs" in sidebar
   - Click "Create New Post" button at top-right

3. **Direct URL:**
   - http://127.0.0.1:5000/blog/create

---

## Tips

- **Add media while creating** - Upload images/videos with your post for better engagement
- **Use tags** - Help others find your post through tags
- **Categories** - Select relevant categories for better organization
- **Preview** - After creation, your post appears immediately in the blog listing

---

## Troubleshooting

**Can't see "Create" button?**
- Make sure you're logged in
- Refresh the page

**File upload failed?**
- Check file size isn't too large
- Ensure file format is supported (see list above)
- Try re-uploading

**Form won't submit?**
- Fill in all required fields (Title, Body)
- Check for JavaScript errors in browser console

---

**Last Updated:** November 11, 2025
