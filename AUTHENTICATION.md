# Authentication System Documentation

## Overview
A simple login/signup system has been implemented for the Django blog project.

## Features
- User registration (signup)
- User login
- User logout
- Protected home page with welcome message
- Form validation
- Error handling
- Success messages

## URLs
- `/login/` - Login page
- `/signup/` - Registration page
- `/logout/` - Logout (POST only)
- `/` - Home page (requires authentication)

## Files Created/Modified

### New Files
1. `accounts/` - New Django app for authentication
2. `accounts/views.py` - Contains signup_view, login_view, and home_view
3. `accounts/urls.py` - URL routing for authentication
4. `accounts/templates/accounts/base.html` - Base template with styling
5. `accounts/templates/accounts/login.html` - Login form
6. `accounts/templates/accounts/signup.html` - Registration form
7. `accounts/templates/accounts/home.html` - Welcome page

### Modified Files
1. `blog/settings.py` - Added 'accounts' to INSTALLED_APPS and authentication settings
2. `blog/urls.py` - Included accounts URLs
3. `docker-compose.yml` - Removed obsolete version attribute
4. `README.md` - Updated with authentication features

## How to Use

### 1. Start the application
```bash
docker-compose up --build
```

### 2. Access the application
Visit http://localhost:8000/login

### 3. Create a new account
- Click "Sign up" link or go to http://localhost:8000/signup
- Enter a username and password (twice for confirmation)
- Click "Sign Up"
- You'll be automatically logged in and redirected to the welcome page

### 4. Login
- Go to http://localhost:8000/login
- Enter your username and password
- Click "Login"

### 5. Logout
- Click the "Logout" button on the welcome page

## Technical Details

### Views
- **signup_view**: Handles user registration using Django's UserCreationForm
- **login_view**: Handles user authentication using AuthenticationForm
- **home_view**: Protected view that shows welcome message (requires @login_required)

### Templates
All templates extend `base.html` which includes:
- Responsive design
- Modern gradient styling
- Form validation error display
- Success/error message display
- Mobile-friendly layout

### Security
- CSRF protection on all forms
- Password validation (Django's built-in validators)
- Login required decorator on protected views
- Automatic redirect if already authenticated

## Next Steps
The authentication system is ready. You can now:
- Add more features to the home page
- Create additional protected pages
- Implement password reset functionality
- Add email verification
- Create user profiles
- Add social authentication
