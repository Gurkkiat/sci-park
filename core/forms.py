from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # เลือกฟิลด์ที่จะให้ User กรอก
    is_for_others = forms.BooleanField(required=False, label="จองให้ผู้อื่น", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    registrant_name = forms.CharField(required=False, label="ชื่อผู้จอง (กรณีจองให้ผู้อื่น)", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ระบุชื่อผู้ใช้งานจริง'}))

    class Meta:
        model = Booking
        # เลือกฟิลด์ที่จะให้ User กรอก (ตัด booked_by_user ออก เพราะจะ auto-fill)
        fields = ['topic', 'facility', 'booking_date', 'start_time', 'end_time', 'phone_number', 'is_for_others', 'registrant_name']
        
        # ปรับแต่งหน้าตา Input ให้สวยด้วย Bootstrap
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # step="1800" = 30 minutes
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': '1800'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': '1800'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เช่น ประชุมทีมโปรเจกต์ A'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เบอร์โทรศัพท์ติดต่อ'}),
            'facility': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            # 1. Start < End check (Basic)
            if start_time >= end_time:
                raise forms.ValidationError("เวลาเริ่มต้นต้องมาก่อนเวลาสิ้นสุด")

            # Calculate duration in minutes
            # Convert to datetime for calculation (using dummy date)
            from datetime import datetime, date, timedelta
            dummy_date = date.today()
            start_dt = datetime.combine(dummy_date, start_time)
            end_dt = datetime.combine(dummy_date, end_time)
            duration = end_dt - start_dt
            duration_minutes = duration.total_seconds() / 60
            
            # 2. Check 30-minute intervals
            if start_time.minute % 30 != 0:
                 self.add_error('start_time', "กรุณาเลือกเวลาลงท้ายด้วย 00 หรือ 30 นาทีเท่านั้น")
            if end_time.minute % 30 != 0:
                 self.add_error('end_time', "กรุณาเลือกเวลาลงท้ายด้วย 00 หรือ 30 นาทีเท่านั้น")

            # 3. Check Duration (1 hour <= duration <= 4 hours)
            if duration_minutes < 60:
                raise forms.ValidationError("ระยะเวลาการจองต้องไม่ต่ำกว่า 1 ชั่วโมง")
            if duration_minutes > 240: # 4 * 60
                raise forms.ValidationError("ระยะเวลาการจองสูงสุดไม่เกิน 4 ชั่วโมง")
        
        return cleaned_data

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