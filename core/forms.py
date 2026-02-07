from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # เลือกฟิลด์ที่จะให้ User กรอก
        fields = ['topic', 'booked_by_user', 'facility', 'booking_date', 'start_time', 'end_time', 'phone_number']
        
        # ปรับแต่งหน้าตา Input ให้สวยด้วย Bootstrap
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น ประชุมทีมโปรเจกต์ A'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เบอร์โทรศัพท์ติดต่อ'}),
            'facility': forms.Select(attrs={'class': 'form-select'}),
            'booked_by_user': forms.Select(attrs={'class': 'form-select'}),
        }

from .models import Project, Student, Team

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_fullname', 'project_detail', 'objective', 'budget_year']
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อโครงการสั้นๆ (เช่น Smart Farm)'}),
            'project_fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อโครงการเต็มรูปแบบ'}),
            'project_detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'รายละเอียดโครงการ...'}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'วัตถุประสงค์ของโครงการ...'}),
            'budget_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ปีงบประมาณ (เช่น 2567)'}),
        }

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['concept', 'development_needs']
        widgets = {
            'concept': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'แนวคิดหลักของโครงงาน (Concept)'}),
            'development_needs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ความต้องการสนับสนุน (Development Needs)'}),
        }

class MemberAddForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('student_id'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="เลือกนักศึกษา"
    )

class StudentForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('Student', 'นักศึกษา'),
        ('Lecturer', 'อาจารย์'),
        ('Researcher', 'นักวิจัย'),
        ('Entrepreneur', 'ผู้ประกอบการ'),
    ]
    type_student = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="สถานะ"
    )

    class Meta:
        model = Student
        fields = ['student_id', 'type_student', 'full_name', 'major', 'faculty', 'year_of_study', 'email', 'tel']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'รหัส (เช่น STD..., LEC...)'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อ-นามสกุล'}),
            'major': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'สาขาวิชา/ความเชี่ยวชาญ'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'คณะ/หน่วยงาน'}),
            'year_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชั้นปี (ถ้ามี)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'อีเมล'}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เบอร์โทรศัพท์'}),
        }

from .models import ProjectTimeline

class ProjectTimelineForm(forms.ModelForm):
    class Meta:
        model = ProjectTimeline
        fields = ['milestone_title', 'milestone_date', 'status', 'description', 'evidence_file']
        widgets = {
            'milestone_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อระยะการดำเนินงาน'}),
            'milestone_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('Pending', 'Pending'),
                ('In Progress', 'In Progress'),
                ('Completed', 'Completed')
            ]),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'รายละเอียดความคืบหน้า...'}),
            'evidence_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'อีเมล'}))

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'อีเมล'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อผู้ใช้'}),
        }

from .models import Training, Student

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['training_name', 'training_date', 'training_end_date', 'lecturer_name', 'project', 'description']
        widgets = {
            'training_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'หัวข้อการอบรม'}),
            'training_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'วันเริ่ม'}),
            'training_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'วันสิ้นสุด'}),
            'lecturer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อวิทยากร (Lecturer)'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'รายละเอียดการอบรม...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'รายละเอียดการอบรม...'}),
        }

class TrainingParticipantForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="เลือกนักศึกษา"
    )

from .models import ProjectAward

class ProjectAwardForm(forms.ModelForm):
    class Meta:
        model = ProjectAward
        fields = ['award_name', 'around', 'year', 'rank']
        widgets = {
            'award_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อรางวัล (เช่น Best Innovation)'}),
            'around': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'รอบการแข่งขัน (เช่น รอบสุดท้าย)'}),
            'year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ปีที่ได้รับ (เช่น 2024)'}),
            'rank': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ลำดับรางวัล (เช่น ชนะเลิศ, รองชนะเลิศ)'}),
        }