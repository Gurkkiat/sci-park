
import os
import django
from django.test import RequestFactory
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scipark_system.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Project, Training
from core.views import project_detail, training_detail

# Setup
factory = RequestFactory()
user = User.objects.filter(is_superuser=True).first()
if not user:
    user = User.objects.create_superuser('admin2', 'admin2@example.com', 'pass')

print("--- Creating Data ---")
proj, _ = Project.objects.get_or_create(
    project_id="PROJ-DBG-001",
    defaults={'project_name': "Debug Project", 'budget_year': "2567"}
)
print(f"Project: {proj.project_name}")

training, _ = Training.objects.get_or_create(
    training_id="TR-DBG-001",
    defaults={
        'training_name': "Debug Training",
        'training_date': timezone.now().date(),
        'project': proj,
        'lecturer_name': "Dr. Debug"
    }
)
print(f"Training: {training.training_name} (Linked to: {training.project.project_name})")

print("\n--- Testing Project Detail (with Training History) ---")
try:
    request = factory.get(f'/projects/{proj.project_id}/')
    request.user = user
    response = project_detail(request, project_id=proj.project_id)
    print(f"Project Detail Status: {response.status_code}")
except Exception as e:
    print(f"Project Detail Error: {e}")

print("\n--- Testing Training Detail ---")
try:
    request = factory.get(f'/training/{training.training_id}/')
    request.user = user
    response = training_detail(request, training_id=training.training_id)
    print(f"Training Detail Status: {response.status_code}")
except Exception as e:
    print(f"Training Detail Error: {e}")
