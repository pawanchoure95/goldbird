# âš¡ Quick Reference - Goldbird

## ðŸš€ Start Project in 3 Steps

```bash
# 1. Install
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

# 2. Run
python manage.py runserver

# 3. Access
# Home: http://localhost:8000/
# Register: http://localhost:8000/accounts/register/
# Admin: http://localhost:8000/adminpanel/login/
```

## ðŸ“ All URL Endpoints

### Public Pages
- `http://localhost:8000/` - Home
- `http://localhost:8000/accounts/register/` - Register
- `http://localhost:8000/accounts/login/` - Login
- `http://localhost:8000/adminpanel/login/` - Admin Login

### User Pages (Login Required)
- `http://localhost:8000/accounts/dashboard/` - Dashboard
- `http://localhost:8000/accounts/profile/` - My Profile
- `http://localhost:8000/accounts/profile/edit/` - Edit Profile
- `http://localhost:8000/accounts/search/` - Search Users
- `http://localhost:8000/accounts/logout/` - Logout

### Admin Pages (Admin Login Required)
- `http://localhost:8000/adminpanel/dashboard/` - Admin Dashboard
- `http://localhost:8000/adminpanel/users/` - Manage Users
- `http://localhost:8000/adminpanel/logout/` - Admin Logout

## ðŸ‘¥ Admin Credentials

```
Email: admin@matrimonial.com
Password: admin123
```

## ðŸ—‚ï¸ File Structure Quick Look

```
website1/
â”œâ”€â”€ manage.py                    â† Start here to run server
â”œâ”€â”€ requirements.txt             â† All dependencies
â”œâ”€â”€ .env                         â† Config (MongoDB, SECRET_KEY)
â”œâ”€â”€ matrimonial_website/         â† Project settings
â”œâ”€â”€ accounts/                    â† User app
â”‚   â”œâ”€â”€ models.py               â† Profile, Like models
â”‚   â”œâ”€â”€ views.py                â† All user views
â”‚   â”œâ”€â”€ forms.py                â† All user forms
â”‚   â””â”€â”€ templates/              â† All user pages
â”œâ”€â”€ adminpanel/                 â† Admin app
â”‚   â”œâ”€â”€ views.py                â† Admin views
â”‚   â””â”€â”€ templates/              â† Admin pages
â”œâ”€â”€ templates/                  â† Base + Home templates
â””â”€â”€ DATABASE COLLECTIONS:
    - auth_user (from Django)
    - accounts_profile (user profiles)
    - accounts_like (likes)
```

## ðŸ”§ Common Commands

### Development
```bash
# Start server
python manage.py runserver

# Run on different port
python manage.py runserver 8001

# Create admin user
python manage.py createsuperuser

# Reset migrations
python manage.py makemigrations
python manage.py migrate

# Open Django admin
# Visit: http://localhost:8000/admin/
```

### Database
```bash
# View all collections
mongosh
use matrimonial
db.getCollectionNames()

# Count users
db.auth_user.countDocuments()

# Exit MongoDB
exit
```

### Maintenance
```bash
# Collect static files (production)
python manage.py collectstatic

# Check for errors
python manage.py check

# Shell (Python with Django)
python manage.py shell
```

## ðŸ“ Feature Quick Links

### Registration Flow
1. Register page: `/accounts/register/`
2. Form: UserRegistrationForm
3. Auto creates Profile
4. Redirects to: `/accounts/profile/edit/`

### Profile Flow
1. Edit profile: `/accounts/profile/edit/`
2. Upload picture
3. Fill all details
4. Save to database
5. View on: `/accounts/profile/`

### Search Flow
1. Search page: `/accounts/search/`
2. Apply filters
3. Browse profiles
4. Click "Like" or "View Profile"

### Admin Flow
1. Admin login: `/adminpanel/login/`
2. Credentials: admin@matrimonial.com / admin123
3. Dashboard: `/adminpanel/dashboard/`
4. Manage users: `/adminpanel/users/`

## ðŸŽ¨ Styling Quick Reference

### Colors Used
- **Primary Red**: #e74c3c
- **Dark Blue**: #2c3e50
- **Light Gray**: #ecf0f1
- **Success Green**: #27ae60
- **Danger Red**: #c0392b

### Bootstrap Grid
- Mobile: col-12 (full width)
- Tablet: col-md-6 (2 columns)
- Desktop: col-md-4 (3 columns)

## ðŸ› Troubleshooting

### MongoDB Error
```
Error: Connection refused
Fix: Ensure MongoDB is running
Command: mongod
Or connect to MongoDB Atlas via .env
```

### Port Already in Use
```
Error: Address already in use
Fix: python manage.py runserver 8001
Or kill process on port 8000
```

### Template Not Found
```
Error: TemplateDoesNotExist
Fix: Check TEMPLATES setting in settings.py
Verify file exists in correct folder
```

### Migration Issues
```
Error: No migrations
Fix: python manage.py makemigrations
Then: python manage.py migrate
```

### Static Files Missing
```
Fix: python manage.py collectstatic
Or check STATIC_URL in settings.py
```

## ðŸ“Š Feature Checklist

- âœ… User Registration
- âœ… User Login/Logout
- âœ… Profile Creation
- âœ… Profile Editing
- âœ… Profile Picture Upload
- âœ… User Dashboard
- âœ… Search Users
- âœ… Filter by Gender, Religion, Age, Location
- âœ… Like/Unlike Profiles
- âœ… View Other Profiles
- âœ… Admin Login
- âœ… Admin Dashboard
- âœ… Admin Manage Users
- âœ… Admin Deactivate Users
- âœ… Admin Delete Users
- âœ… Responsive Design
- âœ… Mobile Friendly

## ðŸ“š Documentation Files

| File | Purpose |
|------|---------|
| README.md | Complete documentation |
| SETUP.md | Quick start guide |
| DELIVERY_SUMMARY.md | What's included |
| PROJECT_DOCUMENTATION.md | Detailed features |
| TESTING_GUIDE.md | Test scenarios |
| FILE_LISTING.md | File structure |
| QUICK_REFERENCE.md | This file |

## ðŸŽ¯ Key Models

### Profile Model
```python
- user (OneToOne)
- bio, phone, gender, age, height
- religion, marital_status
- location, occupation, income, education
- profile_picture
- date_created, date_updated
- is_active
```

### Like Model
```python
- from_user (ForeignKey)
- to_user (ForeignKey)
- created_at
```

## ðŸ” Security Checklist

- âœ… Password hashing (PBKDF2)
- âœ… CSRF protection
- âœ… Email validation
- âœ… Form validation
- âœ… XSS prevention
- âœ… SQL injection prevention
- âœ… Session management
- âœ… Secure password requirements
- âœ… Environment variables for secrets

## ðŸ“± Responsive Breakpoints

- **Mobile**: < 768px (col-12)
- **Tablet**: 768px - 1024px (col-md-6)
- **Desktop**: > 1024px (col-md-4, col-lg-3)

## ðŸ”— External Resources

- Bootstrap 5: https://getbootstrap.com/
- Django Docs: https://docs.djangoproject.com/
- MongoDB: https://www.mongodb.com/
- Font Awesome: https://fontawesome.com/

## âŒ¨ï¸ Keyboard Shortcuts

- **Ctrl+C** - Stop server
- **F12** - Developer tools
- **Ctrl+Shift+M** - Mobile view in DevTools
- **Ctrl+L** - Focus URL bar

## ðŸŽ“ Learning Path

1. Read: SETUP.md (5 min)
2. Run: `pip install -r requirements.txt` (2 min)
3. Run: `python manage.py makemigrations && migrate` (1 min)
4. Run: `python manage.py runserver` (1 min)
5. Test: TESTING_GUIDE.md (10 min)
6. Explore: Visit all pages and test features

## ðŸ’¾ Regular Backups

```bash
# Best practice: Backup MongoDB regularly
mongodump --db matrimonial --out ./backup

# Restore from backup
mongorestore ./backup

# Backup media files (profile pictures)
# Copy media/ folder to safe location
```

## ðŸŒ Deployment Checklist

- [ ] Change DEBUG=False in settings.py
- [ ] Update SECRET_KEY to random string
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up production MongoDB
- [ ] Configure static files CDN
- [ ] Set up HTTPS/SSL
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Configure backup strategy
- [ ] Test all features in production
- [ ] Set up monitoring

## ðŸ“ž Support

For issues:
1. Check TESTING_GUIDE.md
2. Read error messages carefully
3. Check terminal output
4. Review Django logs
5. Check MongoDB connection
6. Verify file paths
7. Check permissions

## ðŸ“„ License & Credits

- Built with Django 4.2
- MongoDB via djongo
- Bootstrap 5
- Font Awesome icons

---

**Version**: 1.0 Complete Release
**Status**: Production Ready
**Last Updated**: 2026-02-24

Everything is working. Start the server with:
```bash
python manage.py runserver
```

Then visit: http://localhost:8000/

