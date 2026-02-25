# Quick Start Guide - Goldbird

## Prerequisites
- Python 3.8 or higher
- MongoDB running locally (or accessible via connection string)
- Git (optional)

## One-Command Setup (Windows)

```bash
# 1. Navigate to project folder
cd d:\Downloads\vd\website1

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations (creates database)
python manage.py makemigrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

## Access Points

Once the server is running, open your browser:

### Public Pages
- **Home**: http://localhost:8000/
- **Register**: http://localhost:8000/accounts/register/
- **Login**: http://localhost:8000/accounts/login/
- **Admin Panel Login**: http://localhost:8000/adminpanel/login/

### After Login (User)
- **Dashboard**: http://localhost:8000/accounts/dashboard/
- **My Profile**: http://localhost:8000/accounts/profile/
- **Edit Profile**: http://localhost:8000/accounts/profile/edit/
- **Search Users**: http://localhost:8000/accounts/search/

### Admin Panel
- **Admin Login**: http://localhost:8000/adminpanel/login/
  - Email: `admin@matrimonial.com`
  - Password: `admin123`
- **Admin Dashboard**: http://localhost:8000/adminpanel/dashboard/
- **Manage Users**: http://localhost:8000/adminpanel/users/

## Testing the Website

### 1. Create a User Account
1. Go to http://localhost:8000/
2. Click "Get Started" or "Register"
3. Fill in: First Name, Last Name, Email, Password
4. Click "Create Account"
5. You'll be redirected to profile edit page

### 2. Complete Profile
1. Fill in profile details (Gender, Age, Location, Religion, etc.)
2. Upload a profile picture (optional but recommended)
3. Click "Save Profile"

### 3. View Dashboard
1. Go to Dashboard
2. See stats like likes received, profile completion percentage

### 4. Search for Matches
1. Go to Search Profiles
2. Use filters (Gender, Religion, Age Range, Location)
3. Click "Search"
4. Browse profiles and click "Like" or "View Profile"

### 5. Admin Panel (Optional)
1. Go to http://localhost:8000/adminpanel/login/
2. Use credentials: admin@matrimonial.com / admin123
3. View user statistics
4. Manage users (activate/deactivate/delete)

## Stopping the Server

Press `Ctrl+C` in the terminal running the server.

## Troubleshooting

### "MongoDB connection refused"
- Make sure MongoDB is running
- On Windows: Start MongoDB service or run `mongod` in a new terminal
- Or connect to MongoDB Atlas by updating .env with connection string

### "ModuleNotFoundError: No module named 'django'"
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

### "Address already in use"
- Another process is using port 8000
- Run on different port: `python manage.py runserver 8001`

### "TemplateDoesNotExist"
- Create the templates directory if missing
- Verify all template files are in correct locations

## Database Reset

To reset the database and start fresh:

```bash
# Delete the database
del db.sqlite3  (Windows) or rm db.sqlite3 (Mac/Linux)

# Make migrations again
python manage.py makemigrations
python manage.py migrate
```

## Next Steps

1. Create multiple test user accounts
2. Upload profile pictures
3. Search and like profiles
4. Try admin panel features
5. Test all forms and validations

For detailed documentation, see README.md

