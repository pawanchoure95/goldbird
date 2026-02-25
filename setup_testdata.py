#!/usr/bin/env python
"""
Script to create test data for the matrimonial website
"""
import subprocess
import sys

commands = [
    "from django.contrib.auth.models import User",
    "from accounts.models import Profile",
    "if not User.objects.filter(username='admin').exists(): User.objects.create_superuser('admin', 'admin@test.com', 'admin123'); print('Superuser created')",
    "u1 = User.objects.get_or_create(username='john', defaults={'email': 'john@test.com', 'first_name': 'John', 'last_name': 'Doe'})[0]",
    "u1.set_password('test123')",
    "u1.save()",
    "Profile.objects.get_or_create(user=u1, defaults={'gender': 'M', 'age': 28, 'location': 'New York', 'religion': 'Hindu', 'marital_status': 'Single', 'occupation': 'Engineer'})",
    "u2 = User.objects.get_or_create(username='jane', defaults={'email': 'jane@test.com', 'first_name': 'Jane', 'last_name': 'Smith'})[0]",
    "u2.set_password('test123')",
    "u2.save()",
    "Profile.objects.get_or_create(user=u2, defaults={'gender': 'F', 'age': 26, 'location': 'New York', 'religion': 'Muslim', 'marital_status': 'Single', 'occupation': 'Doctor'})",
    "print('Test users created')",
]

cmd = ' && '.join([f"'{c}'" for c in commands])
manage_cmd = ['D:\\Downloads\\vd\\website1\\.venv\\Scripts\\python.exe', 'manage.py', 'shell', '-c', cmd]

import os
os.chdir('d:\\Downloads\\vd\\website1')
result = subprocess.run(manage_cmd, capture_output=False)
sys.exit(result.returncode)
