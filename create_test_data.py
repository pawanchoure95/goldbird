import os
import django
from django.contrib.auth.models import User
from accounts.models import Profile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matrimonial_website.settings')
django.setup()

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    print("Superuser created: admin / admin123")
else:
    print("Superuser already exists")

# Create test users
test_users = [
    {'username': 'john', 'email': 'john@test.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'test123'},
    {'username': 'jane', 'email': 'jane@test.com', 'first_name': 'Jane', 'last_name': 'Smith', 'password': 'test123'},
    {'username': 'mike', 'email': 'mike@test.com', 'first_name': 'Mike', 'last_name': 'Johnson', 'password': 'test123'},
    {'username': 'sarah', 'email': 'sarah@test.com', 'first_name': 'Sarah', 'last_name': 'Williams', 'password': 'test123'},
]

for user_data in test_users:
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password']
        )
        # Create profile
        Profile.objects.create(
            user=user,
            gender='M' if user_data['username'] in ['john', 'mike'] else 'F',
            age=25 + hash(user_data['username']) % 20,
            location='New York',
            religion='Hindu',
            marital_status='Single',
            occupation='Software Engineer',
            education='Bachelor\'s Degree',
            bio=f"Hi, I'm {user_data['first_name']}"
        )
        print(f"User created: {user_data['username']}")
    else:
        print(f"User already exists: {user_data['username']}")
