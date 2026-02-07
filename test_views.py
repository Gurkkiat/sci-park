
import os
import django
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scipark_system.settings')
django.setup()

from django.contrib.auth.models import AnonymousUser, User
from core.views import dashboard, training_list

factory = RequestFactory()
user = User.objects.filter(is_superuser=True).first()
if not user:
    print("No user found, creating one")
    user = User.objects.create_superuser('admin', 'admin@example.com', 'pass')

print("--- Testing Dashboard ---")
try:
    request = factory.get('/')
    request.user = user
    response = dashboard(request)
    print(f"Dashboard Status: {response.status_code}")
except Exception as e:
    print(f"Dashboard Error: {e}")

print("\n--- Testing Training List ---")
try:
    request = factory.get('/training/')
    request.user = user
    response = training_list(request)
    print(f"Training List Status: {response.status_code}")
except Exception as e:
    print(f"Training List Error: {e}")
