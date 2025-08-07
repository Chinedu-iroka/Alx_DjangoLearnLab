# Django REST Framework CRUD API for Books

This API provides endpoints for managing book records using Django REST Framework's generic views.

## API Endpoints

| Method | Endpoint                | Description                 | Permission          |
|--------|-------------------------|-----------------------------|---------------------|
| GET    | /api/books/             | List all books              | Public              |
| GET    | /api/books/<id>/        | Get book by ID              | Public              |
| POST   | /api/books/create/      | Create a new book           | Authenticated users |
| PUT    | /api/books/<id>/update/ | Update a book by ID         | Authenticated users |
| DELETE | /api/books/<id>/delete/ | Delete a book by ID         | Authenticated users |

## Permissions

- `AllowAny`: for GET requests (public access)
- `IsAuthenticated`: for POST, PUT, DELETE (auth-only)

## Models

- `Author`: name
- `Book`: title, publication_year, author (ForeignKey)

## Custom Logic

- `BookSerializer` ensures `publication_year` is not in the future.
- Nested `books` are included when serializing `Author` instances.
