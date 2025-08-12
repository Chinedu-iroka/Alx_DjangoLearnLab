# Django Blog Authentication System

## Features:
- User Registration (with email)
- User Login & Logout (using Django's built-in authentication)
- Profile Management (edit email)
- CSRF protection enabled
- Password hashing (PBKDF2 by default)

## How It Works:
1. Registration handled by custom RegisterForm extending UserCreationForm.
2. Login & Logout handled by CustomLoginView and CustomLogoutView.
3. Profile view requires authentication and allows email updates.

## Testing:
- Visit /register/ to create a new account.
- Visit /login/ to sign in.
- Visit /profile/ to update email.
- Visit /logout/ to end session.