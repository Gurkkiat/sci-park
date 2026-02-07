
import os
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scipark_system.settings')
import django
django.setup()

from django.template.loader import get_template
from django.urls import reverse
from core.models import Training

print("--- Checking Template ---")
try:
    get_template('training_detail.html')
    print("Template 'training_detail.html' loaded OK.")
except Exception as e:
    print(f"Template Error: {e}")

print("\n--- Checking Data ---")
trainings = Training.objects.all()
if trainings.count() == 0:
    print("Creating dummy training...")
    try:
        t = Training.objects.create(
            training_id="TR-TEST-001",
            training_name="Test Training",
            training_date="2024-01-01"
        )
        print("Created TR-TEST-001")
        trainings = Training.objects.all()
    except Exception as e:
        print(f"Creation Error: {e}")

print(f"Total Trainings: {trainings.count()}")
for t in trainings:
    print(f"Training: {t.training_name} (ID: {t.training_id})")
    try:
        url = reverse('training_detail', args=[t.training_id])
        print(f"  URL: {url}")
    except Exception as e:
        print(f"  URL Error: {e}")
