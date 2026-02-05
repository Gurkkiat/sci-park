import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scipark_system.settings')
django.setup()

from core.models import *

def add_test_student():
    # 1. Pick a project
    project = Project.objects.first()
    if not project:
        print("No project found. Run seed.py first.")
        return

    print(f"Target Project: {project.project_name} (ID: {project.project_id})")

    # 2. Get the team responsible
    # Try finding team by exact name first
    team = Team.objects.filter(project_name=project.project_name).first()
    
    if not team:
        print(f"No team found with exact project name '{project.project_name}'. Checking any team...")
        # Fallback: Just pick the first team and assign it to this project for testing
        team = Team.objects.first()
        if team:
            print(f"    -> Assigning Team '{team.team_name}' to Project '{project.project_name}' temporarily.")
            team.project_name = project.project_name
            team.save()
        else:
            print("No teams exist at all. Run seed.py")
            return
    
    print(f"Target Team: {team.team_name}")

    # 3. Create a Test Student
    s_id = "TEST-USER-001"
    student, created = Student.objects.get_or_create(
        student_id=s_id,
        defaults={
            'full_name': "Testersky McTestface",
            'nickname': "Test",
            'major': "Debugging Engineering",
            'faculty': "Engineering",
            'email': "test@example.com"
        }
    )
    if created:
        print(f"Created Student: {student.full_name}")
    else:
        print(f"Student {student.full_name} already exists")

    # 4. Add to Team
    ts_id = f"TS-TEST-{random.randint(1000,9999)}"
    TeamStudent.objects.create(
        tsid=ts_id,
        team_name=team.team_name,
        student=student.student_id
    )
    print(f"Added {student.full_name} to Team {team.team_name}")
    
    print(f"\nCHECK URL: http://127.0.0.1:8000/project/{project.project_id}/")

if __name__ == '__main__':
    add_test_student()
