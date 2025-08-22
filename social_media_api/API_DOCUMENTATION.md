# Social Media API - Posts and Comments Endpoints

## Posts Endpoints

### List Posts
**GET** `/api/posts/`
- Returns paginated list of all posts
- Query parameters: `page`, `page_size`, `search`, `author`, `ordering`
- **Example Response:**
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": {"id": 1, "username": "john_doe"},
            "title": "My First Post",
            "content": "This is my first post content...",
            "created_at": "2023-01-01T10:00:00Z",
            "updated_at": "2023-01-01T10:00:00Z",
            "comments_count": 5
        }
    ]
}


## Follow Management Endpoints

### Follow a User
**POST** `/api/auth/follow/`
- **Headers:** `Authorization: Token <your_token>`
- **Body:**
```json
{
    "user_id": 2
}



## Like Endpoints

### Like a Post
**POST** `/api/posts/{post_id}/like/`
- **Headers:** `Authorization: Token <your_token>`
- **Response:**
```json
{
    "id": 1,
    "user": "username",
    "post": 1,
    "created_at": "2023-01-01T10:00:00Z"
}