# Goldbird - Dating/Matrimonial Website

A complete, fully functional matrimonial/dating website built with Django and MongoDB.

## Features

### User Features
- User Registration & Authentication
- User Profiles with Profile Pictures
- Profile Editing & Customization
- Advanced Search with Filters (Gender, Religion, Age, Location)
- Like/Interest System
- User Dashboard
- Responsive Mobile-Friendly UI

### Admin Features
- Admin Login/Logout
- View All Users
- User Activation/Deactivation
- Delete Users
- View User Profiles
- System Statistics

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: MongoDB (NoSQL) via djongo
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Authentication**: Django session-based authentication
- **Image Upload**: Pillow

## Installation & Setup

### Prerequisites

1. **Python 3.8+** installed on your system
2. **MongoDB** installed locally (or use MongoDB Atlas connection string)

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd website1

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure MongoDB Connection (Optional)

- Ensure MongoDB is running locally on port 27017
- Or update the MONGODB_URI in .env file with your MongoDB connection string

### Step 4: Create Migrations & Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000`

## Access the Website

### User Portal
- **Home**: http://localhost:8000/
- **Register**: http://localhost:8000/accounts/register/
- **Login**: http://localhost:8000/accounts/login/
- **Dashboard**: http://localhost:8000/accounts/dashboard/
- **Profile**: http://localhost:8000/accounts/profile/
- **Search**: http://localhost:8000/accounts/search/

### Admin Panel
- **Admin Login**: http://localhost:8000/adminpanel/login/
- **Admin Dashboard**: http://localhost:8000/adminpanel/dashboard/
- **Manage Users**: http://localhost:8000/adminpanel/users/

### Django Admin
- **Django Admin**: http://localhost:8000/admin/
- Create superuser: `python manage.py createsuperuser`

## Default Admin Credentials

- **Email**: admin@matrimonial.com
- **Password**: admin123

## Project Structure

```
matrimonial_website/
â”œâ”€â”€ matrimonial_website/          # Main project settings
â”‚   â”œâ”€â”€ settings.py
â”‚   â”œâ”€â”€ urls.py
â”‚   â”œâ”€â”€ wsgi.py
â”‚   â””â”€â”€ asgi.py
â”œâ”€â”€ accounts/                      # User accounts app
â”‚   â”œâ”€â”€ migrations/
â”‚   â”œâ”€â”€ templates/
â”‚   â”‚   â”œâ”€â”€ register.html
â”‚   â”‚   â”œâ”€â”€ login.html
â”‚   â”‚   â”œâ”€â”€ dashboard.html
â”‚   â”‚   â”œâ”€â”€ profile.html
â”‚   â”‚   â”œâ”€â”€ profile_edit.html
â”‚   â”‚   â””â”€â”€ search.html
â”‚   â”œâ”€â”€ models.py
â”‚   â”œâ”€â”€ forms.py
â”‚   â”œâ”€â”€ views.py
â”‚   â””â”€â”€ urls.py
â”œâ”€â”€ adminpanel/                    # Admin panel app
â”‚   â”œâ”€â”€ migrations/
â”‚   â”œâ”€â”€ templates/
â”‚   â”‚   â”œâ”€â”€ admin_login.html
â”‚   â”‚   â”œâ”€â”€ admin_dashboard.html
â”‚   â”‚   â”œâ”€â”€ admin_users.html
â”‚   â”‚   â””â”€â”€ admin_user_detail.html
â”‚   â”œâ”€â”€ models.py
â”‚   â”œâ”€â”€ views.py
â”‚   â””â”€â”€ urls.py
â”œâ”€â”€ templates/
â”‚   â”œâ”€â”€ base.html                 # Base template
â”‚   â””â”€â”€ home.html                 # Home page
â”œâ”€â”€ static/
â”‚   â””â”€â”€ css/                      # Static CSS files
â”œâ”€â”€ media/                         # User uploads (profile pictures)
â”œâ”€â”€ manage.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .env
â””â”€â”€ .gitignore
```

## Database Collections

The application uses MongoDB with the following main collections:

1. **auth_user** - User authentication data
2. **accounts_profile** - User profile information
3. **accounts_like** - Like/interest records

## Key Functionality

### User Registration
- Email-based registration
- Password validation
- Automatic profile creation upon signup

### Profile Management
- Upload profile picture
- Edit personal & professional information
- Multiple choice fields (Gender, Religion, Marital Status)
- Searchable fields (Age, Location, Occupation)

### Search & Filter
- Filter by Gender, Religion, Age Range
- Search by Location
- Pagination of results (12 profiles per page)
- View match profiles

### Like System
- Like/Unlike profiles
- Track likes received and given
- Persistent storage in database

### Admin Dashboard
- View system statistics
- Manage user accounts
- Activate/Deactivate users
- Delete users
- View detailed user profiles

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `mongod`
- Check connection string in .env file
- Or install and run: `brew services start mongodb-community` (Mac)

### Migration Errors
```bash
# Reset migrations if needed
python manage.py makemigrations --empty accounts --name initial_migration
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Port Already in Use
```bash
python manage.py runserver 8001  # Use different port
```

## Production Deployment

Before deploying to production:

1. Change `DEBUG = False` in settings.py
2. Update `SECRET_KEY` to a random, secure value
3. Configure `ALLOWED_HOSTS` with your domain
4. Set up production MongoDB database
5. Use environment variables for sensitive data
6. Configure static files and media storage
7. Set up HTTPS/SSL certificates

### Quick Deploy on Render

1. Push code to GitHub.
2. Go to Render Dashboard and click `New +` -> `Blueprint`.
3. Select your repository (it will auto-detect `render.yaml`).
4. Verify env vars:
   - `DEBUG=False`
   - `ALLOWED_HOSTS=.onrender.com,<your-domain>`
   - `CSRF_TRUSTED_ORIGINS=https://*.onrender.com,https://<your-domain>`
   - secure random `SECRET_KEY`
5. Deploy. Build runs `build.sh` (collectstatic + migrate) automatically.
6. Open URL: `https://<service-name>.onrender.com`

For custom domain:
- Add domain in Render settings
- Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
- Point DNS records from your domain provider to Render

## Security Notes

- Passwords are hashed using Django's default password hasher
- CSRF protection enabled
- Session-based authentication
- Form validation on all inputs
- SQL injection prevention through ORM

## Future Enhancements

- Real-time messaging system
- Email notifications
- Advanced matching algorithm
- Payment integration for premium features
- Social media login
- Video verification
- Automated spam detection
- Analytics dashboard

## License

This project is for educational purposes.

## Support

For issues or questions, please create an issue in the repository.

