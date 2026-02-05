from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Import messages
from .models import Student, Project, Facility, Booking, Team, TeamStudent, ProjectAward
from django.db.models import Q
from .forms import BookingForm

def dashboard(request):
    # 1. ดึงข้อมูลจำนวนรายการต่างๆ มานับ (Count)
    total_students = Student.objects.count()
    total_projects = Project.objects.count()
    total_facilities = Facility.objects.count()
    
    # ดึงการจองล่าสุด 5 รายการมาแสดง
    recent_bookings = Booking.objects.order_by('-booking_date')[:5]

    # --- Chart Logic: Student Participation by Month ---
    import datetime
    from django.utils import timezone
    
    # 1. Get current year or filtered year
    current_year = timezone.now().year
    selected_year = request.GET.get('year', current_year)
    try:
        selected_year = int(selected_year)
    except ValueError:
        selected_year = current_year

    # 2. Get all projects in that year (Project Name -> Month Key)
    # Using python dict for lookup because relationships are CharFields, not FKs
    projects_in_year = Project.objects.filter(date_time__year=selected_year)
    project_date_map = {} # {'ProjectName': month_index (1-12)}
    for p in projects_in_year:
        if p.project_name and p.date_time:
            # Normalize name: strip keys
            project_date_map[p.project_name.strip()] = p.date_time.month

    # 3. Get Teams linked to those projects
    # Team.project_name -> Team.team_name
    teams = Team.objects.all()
    team_month_map = {} # {'TeamName': month_index}
    for t in teams:
        if t.project_name and t.team_name:
            p_name = t.project_name.strip()
            if p_name in project_date_map:
                team_month_map[t.team_name.strip()] = project_date_map[p_name]

    # 4. Count Students in those teams
    # TeamStudent.team_name
    team_students = TeamStudent.objects.all()
    monthly_counts = {i: 0 for i in range(1, 13)} # 1..12

    for ts in team_students:
        if ts.team_name:
            t_name = ts.team_name.strip()
            if t_name in team_month_map:
                month = team_month_map[t_name]
                monthly_counts[month] += 1

    # 5. Prepare data for Chart.js
    chart_labels = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
    chart_data = [monthly_counts[i] for i in range(1, 13)]
    
    # Available years for filter (e.g., last 5 years)
    available_years = range(current_year, current_year - 5, -1)

    # 2. ห่อข้อมูลใส่ตัวแปร context เพื่อส่งไปหน้าเว็บ
    context = {
        'total_students': total_students,
        'total_projects': total_projects,
        'total_facilities': total_facilities,
        'recent_bookings': recent_bookings,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'selected_year': selected_year,
        'available_years': available_years,
    }

    # 3. ส่งข้อมูลไปที่ไฟล์ HTML (เดี๋ยวเราจะสร้างไฟล์นี้ในขั้นตอนถัดไป)
    return render(request, 'dashboard.html', context)

def project_list(request):
    query = request.GET.get('q') # รับคำค้นหาจากช่อง Search
    projects = Project.objects.all()

    if query:
        # ระบบค้นหาอัจฉริยะ: ค้นหาจาก (ชื่อโปรเจกต์) หรือ (ชื่อทีม) หรือ (รายละเอียด)
        projects = projects.filter(
            Q(project_name__icontains=query) |
            Q(project_fullname__icontains=query) |
            Q(project_detail__icontains=query)
        )

    return render(request, 'project_list.html', {'projects': projects, 'query': query})

def project_detail(request, project_id):
    # 1. ดึงข้อมูลโปรเจกต์
    project = Project.objects.get(project_id=project_id)
    
    # 2. หาว่าโปรเจกต์นี้ ทีมไหนรับผิดชอบ
    teams = Team.objects.filter(project_name=project.project_name)
    
    # 3. จัดเตรียมข้อมูลทีมพร้อมนักศึกษาในทีมนั้นๆ
    teams_data = []
    for team in teams:
        # หา ID นักศึกษาที่อยู่ในทีมนี้
        student_ids = TeamStudent.objects.filter(team_name=team.team_name).values_list('student', flat=True)
        # ดึงข้อมูลนักศึกษา
        team_students = Student.objects.filter(student_id__in=student_ids)
        
        teams_data.append({
            'team': team,
            'students': team_students
        })
    
    # 4. Get Project Timeline
    timeline = project.timelines.all()

    context = {
        'project': project,
        'teams_data': teams_data,
        'member_form': MemberAddForm(), 
        'student_form': StudentForm(), # Add new student form
        'timeline_form': ProjectTimelineForm(), # Add timeline form
        'timeline': timeline
    }
    return render(request, 'project_detail.html', context)

import json
from django.core.serializers.json import DjangoJSONEncoder

def booking_create(request):
    # Fetch all facilities for JS filtering
    all_facilities = list(Facility.objects.all().values('facility_id', 'facility_name', 'zone', 'floor', 'facility_type'))
    facilities_json = json.dumps(all_facilities, cls=DjangoJSONEncoder)
    
    # Fetch bookings
    now = timezone.localtime(timezone.now())
    current_date = now.date()
    current_time = now.time()

    # Upcoming: Future Date OR (Today AND EndTime >= Now)
    upcoming_bookings = Booking.objects.filter(
        Q(booking_date__gt=current_date) |
        Q(booking_date=current_date, end_time__gte=current_time)
    ).order_by('booking_date', 'start_time')

    # History: Past Date OR (Today AND EndTime < Now)
    booking_history = Booking.objects.filter(
        Q(booking_date__lt=current_date) |
        Q(booking_date=current_date, end_time__lt=current_time)
    ).order_by('-booking_date', '-start_time')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Get cleaned data for validation
            booking_date = form.cleaned_data['booking_date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            facility = form.cleaned_data['facility']

            # 1. Logic Validation: Start < End
            if start_time >= end_time:
                messages.error(request, 'เวลาเริ่มต้นต้องมาก่อนเวลาสิ้นสุด (Start time must be before end time)')
                return render(request, 'booking_form.html', {
                    'form': form, 
                    'facilities_json': facilities_json,
                    'upcoming_bookings': upcoming_bookings
                })

            # 2. Overlap Validation
            # (StartA < EndB) and (EndA > StartB)
            is_overlap = Booking.objects.filter(
                facility=facility,
                booking_date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if is_overlap:
                messages.error(request, f'ห้อง {facility.facility_name} ไม่ว่างในช่วงเวลานี้ (Time slot overlapped)')
                return render(request, 'booking_form.html', {
                    'form': form, 
                    'facilities_json': facilities_json,
                    'upcoming_bookings': upcoming_bookings,
                    'booking_history': booking_history
                })

            # Generate Booking ID manually (BK-YYYYMMDD-HHMMSS) to prevent overwrites
            # Since model PK is CharField and not AutoField
            import datetime
            booking = form.save(commit=False)
            booking.booking_id = f"BK-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            booking.save()
            
            messages.success(request, 'บันทึกการจองสำเร็จ! (Booking successfully created)')
            return redirect('dashboard')
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {
        'form': form, 
        'facilities_json': facilities_json,
        'upcoming_bookings': upcoming_bookings,
        'booking_history': booking_history
    })

def student_list(request):
    query = request.GET.get('q')
    faculty_filter = request.GET.get('faculty')
    role_filter = request.GET.get('type') # 'Student', 'Lecturer', 'Researcher', 'Entrepreneur'
    
    students = Student.objects.all().order_by('student_id')
    faculties = Student.objects.values_list('faculty', flat=True).distinct().order_by('faculty')

    # Default to showing all if no role selected, OR you could default to 'Student'
    # For this request, having "All" as an option is good.
    if role_filter and role_filter != 'All':
        students = students.filter(type_student=role_filter)

    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(major__icontains=query)
        )
    
    if faculty_filter:
        students = students.filter(faculty=faculty_filter)

    return render(request, 'student_list.html', {
        'students': students, 
        'query': query,
        'faculties': faculties,
        'selected_faculty': faculty_filter,
        'selected_role': role_filter or 'All'
    })

def student_detail(request, student_id):
    # 1. Get Student Profile
    student = get_object_or_404(Student, student_id=student_id)
    
    # 2. Find Teams the student belongs to
    student_teams_rel = TeamStudent.objects.filter(student=student.student_id)
    team_names = student_teams_rel.values_list('team_name', flat=True)
    
    # 3. Find Projects associated with those teams
    # Note: Team model has project_name, so we can filter Teams by name to get project names,
    # or just filter Projects if project_name on Team matches project_name on Project.
    teams = Team.objects.filter(team_name__in=team_names)
    project_names = teams.values_list('project_name', flat=True)
    projects = Project.objects.filter(project_name__in=project_names)
    
    # 4. Find Awards associated with those teams
    awards = ProjectAward.objects.filter(team_name__in=team_names)
    
    context = {
        'student': student,
        'projects': projects,
        'awards': awards,
        'team_count': len(team_names)
    }
    context = {
        'student': student,
        'projects': projects,
        'awards': awards,
        'team_count': len(team_names)
    }
    return render(request, 'student_detail.html', context)

from .forms import ProjectForm, MemberAddForm
from django.utils import timezone

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            # Generate dummy ID (In real app, use AutoField or UUID)
            count = Project.objects.count() + 1
            project.project_id = f"PROJ-{timezone.now().year}-{count:04d}"
            project.create_by = "User" # Default user
            project.date_time = timezone.now()
            project.save()
            
            # Auto-create Team
            team_count = Team.objects.count() + 1
            Team.objects.create(
                team_id=f"TEAM-{team_count:04d}",
                team_name=f"{project.project_name} Team",
                project_name=project.project_name,
                date_time=timezone.now()
            )
            
            messages.success(request, f'สร้างโครงการ {project.project_name} เรียบร้อยแล้ว!')
            return redirect('project_detail', project_id=project.project_id)
    else:
        form = ProjectForm()
    
    return render(request, 'project_create.html', {'form': form})

from .forms import ProjectForm, MemberAddForm, StudentForm, ProjectTimelineForm # Import Forms

def project_add_member(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)
    # Find the team for this project
    team = Team.objects.filter(project_name=project.project_name).first()
    
    if not team:
        messages.error(request, 'ไม่พบทีมสำหรับโครงการนี้ กรุณาติดต่อผู้ดูแลระบบ')
        return redirect('project_detail', project_id=project_id)

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        if action_type == 'existing':
            member_form = MemberAddForm(request.POST)
            if member_form.is_valid():
                student = member_form.cleaned_data['student']
                
                if TeamStudent.objects.filter(team_name=team.team_name, student=student.student_id).exists():
                    messages.warning(request, f'{student.full_name} เป็นสมาชิกในทีมนี้อยู่แล้ว')
                else:
                    count = TeamStudent.objects.count() + 1
                    TeamStudent.objects.create(
                        tsid=f"TS-{timezone.now().year}-{count:05d}",
                        team_name=team.team_name,
                        student=student.student_id
                    )
                    messages.success(request, f'เพิ่ม {student.full_name} เข้าทีมเรียบร้อยแล้ว')
                return redirect('project_detail', project_id=project_id)

        elif action_type == 'new':
            student_form = StudentForm(request.POST)
            if student_form.is_valid():
                student_id = student_form.cleaned_data['student_id']
                if Student.objects.filter(pk=student_id).exists():
                     messages.error(request, f'รหัสนักศึกษา {student_id} มีอยู่ในระบบแล้ว กรุณาใช้ "เลือกจากรายชื่อ"')
                else:
                    student = student_form.save()
                    
                    count = TeamStudent.objects.count() + 1
                    TeamStudent.objects.create(
                        tsid=f"TS-{timezone.now().year}-{count:05d}",
                        team_name=team.team_name,
                        student=student.student_id
                    )
                    messages.success(request, f'ลงทะเบียนและเพิ่ม {student.full_name} เข้าทีมเรียบร้อยแล้ว')
                    return redirect('project_detail', project_id=project_id)
            else:
                 for field, errors in student_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    
    return redirect('project_detail', project_id=project_id)

from .models import ProjectTimeline

def project_add_timeline(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)
    if request.method == 'POST':
        form = ProjectTimelineForm(request.POST, request.FILES)
        if form.is_valid():
            timeline = form.save(commit=False)
            timeline.project = project
            timeline.save()
            messages.success(request, 'เพิ่มไทม์ไลน์เรียบร้อยแล้ว')
        else:
             messages.error(request, 'เกิดข้อผิดพลาดในการเพิ่มข้อมูล')
    return redirect('project_detail', project_id=project_id)

def project_edit_timeline(request, timeline_id):
    timeline = get_object_or_404(ProjectTimeline, pk=timeline_id)
    if request.method == 'POST':
        form = ProjectTimelineForm(request.POST, request.FILES, instance=timeline)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขข้อมูลเรียบร้อยแล้ว')
        else:
            messages.error(request, 'เกิดข้อผิดพลาดในการแก้ไขข้อมูล')
    return redirect('project_detail', project_id=timeline.project.project_id)

def project_delete_timeline(request, timeline_id):
    timeline = get_object_or_404(ProjectTimeline, pk=timeline_id)
    project_id = timeline.project.project_id
    timeline.delete()
    messages.success(request, 'ลบข้อมูลเรียบร้อยแล้ว')
    return redirect('project_detail', project_id=project_id)