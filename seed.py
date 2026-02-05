import os
import django
import random
from datetime import datetime, timedelta

# 1. ตั้งค่า Django Environment (เพื่อให้เรียกใช้ Model ได้จากภายนอก)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scipark_system.settings')
django.setup()

from core.models import *
from django.utils import timezone

def run_seed():
    print("🌱 กำลังเริ่มสร้างข้อมูลตัวอย่าง (Seeding Data)...")

    # --- เคลียร์ข้อมูลเก่าก่อน (ถ้าต้องการลบให้ Uncomment) ---
    # Booking.objects.all().delete()
    # Project.objects.all().delete()
    # Team.objects.all().delete()
    # Student.objects.all().delete()
    # Facility.objects.all().delete()

    # --- 0. สร้างผู้ใช้งาน (Login) ---
    users = ["Admin User", "Teacher One", "Staff Member"]
    for i, u_name in enumerate(users):
        u_id = f"USER-{i+1:03d}"
        Login.objects.get_or_create(
            user_id=u_id,
            defaults={
                'full_name': u_name,
                'email': f"user{i+1}@scipark.com",
                'type': 'Staff',
                'permission': 'Admin' if i == 0 else 'User'
            }
        )
    print(f"สร้างผู้ใช้งานเรียบร้อย ({len(users)} คน)")

    # --- 1. สร้างคณะ (Faculty) ---
    faculties = ["วิทยาศาสตร์", "วิศวกรรมศาสตร์", "เทคโนโลยีสารสนเทศ", "เกษตรศาสตร์", "บริหารธุรกิจ"]
    for i, fac_name in enumerate(faculties):
        Faculty.objects.get_or_create(
            faculty_name=fac_name,
            defaults={'number_code': f'FAC-{i+1:02d}'}
        )
    print(f"สร้างคณะเรียบร้อย ({len(faculties)} คณะ)")

    # --- 2. สร้างบุคลากร (Student, Lecturer, Researcher, Entrepreneur) ---
    first_names = ["สมชาย", "วิภา", "ก้องภพ", "อารียา", "ณัฐวุฒิ", "พิมพ์ใจ", "ธีระ", "สุดา", "เอกชัย", "มาริสา"]
    last_names = ["ใจดี", "รักเรียน", "มีสุข", "ขยันยิ่ง", "เก่งกาจ", "มั่นคง", "สุขสันต์", "ยอดเยี่ยม"]
    
    # 2.1 นักศึกษา (Student)
    for i in range(1, 16): # 15 คน
        s_id = f"STD{datetime.now().year}-{i:03d}"
        fname = f"{random.choice(first_names)} {random.choice(last_names)}"
        Student.objects.update_or_create(
            student_id=s_id,
            defaults={
                'type_student': 'Student',
                'full_name': fname,
                'nickname': fname.split()[0],
                'major': "Computer Science",
                'faculty': random.choice(faculties),
                'email': f"student{i}@university.ac.th",
                'year_of_study': str(random.randint(1, 4)),
                'tel': f"08{random.randint(1, 9)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            }
        )

    # 2.2 อาจารย์ (Lecturer)
    for i in range(1, 6): # 5 คน
        l_id = f"LEC{datetime.now().year}-{i:03d}"
        fname = f"Dr. {random.choice(first_names)} {random.choice(last_names)}"
        Student.objects.update_or_create(
            student_id=l_id,
            defaults={
                'type_student': 'Lecturer',
                'full_name': fname,
                'nickname': fname.split()[1],
                'major': "Software Engineering",
                'faculty': random.choice(faculties),
                'email': f"lecturer{i}@university.ac.th",
                'tel': f"08{random.randint(1, 9)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            }
        )

    # 2.3 นักวิจัย (Researcher)
    for i in range(1, 6): # 5 คน
        r_id = f"RES{datetime.now().year}-{i:03d}"
        fname = f"{random.choice(first_names)} {random.choice(last_names)}"
        Student.objects.update_or_create(
            student_id=r_id,
            defaults={
                'type_student': 'Researcher',
                'full_name': fname,
                'nickname': fname.split()[0],
                'major': "AI Research",
                'faculty': "Science Park",
                'email': f"researcher{i}@scipark.ac.th",
                'tel': f"08{random.randint(1, 9)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            }
        )

    # 2.4 ผู้ประกอบการ (Entrepreneur)
    for i in range(1, 6): # 5 คน
        e_id = f"ENT{datetime.now().year}-{i:03d}"
        fname = f"คุณ{random.choice(first_names)} {random.choice(last_names)}"
        Student.objects.update_or_create(
            student_id=e_id,
            defaults={
                'type_student': 'Entrepreneur',
                'full_name': fname,
                'nickname': fname.split()[0],
                'major': "Business Owner",
                'faculty': "External",
                'email': f"ceo{i}@startup.com",
                'tel': f"08{random.randint(1, 9)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            }
        )
    print(f"สร้างบุคลากรเรียบร้อย (Student, Lecturer, Researcher, Entrepreneur)")

    # --- 3. สร้างโปรเจกต์ (Project) ---
    project_data = [
        ("Smart Farm IoT", "ระบบรดน้ำต้นไม้อัจฉริยะผ่านมือถือ", "ใช้เซ็นเซอร์วัดความชื้นและสั่งงานผ่าน IoT"),
        ("Elderly Care App", "แอปพลิเคชันดูแลผู้สูงอายุ", "แจ้งเตือนการกินยาและตรวจจับการหกล้ม"),
        ("AI Waste Sorter", "ถังขยะแยกประเภทด้วย AI", "ใช้กล้องตรวจจับขยะและแยกช่องให้อัตโนมัติ"),
        ("Dormitory System", "ระบบจัดการหอพักนักศึกษา", "จองห้อง แจ้งซ่อม และชำระเงินออนไลน์"),
        ("Queue Master", "ระบบจองคิวร้านอาหาร", "ลดเวลารอคอยหน้าร้านด้วยการจองผ่านเว็บ"),
        ("Crypto Wallet", "กระเป๋าเงินดิจิทัล", "รองรับการโอนเหรียญหลักๆ และมีความปลอดภัยสูง"),
        ("VR Campus Tour", "ทัวร์มหาวิทยาลัยเสมือนจริง", "สำหรับให้นักเรียนมัธยมเข้ามาดูสถานที่จริง"),
        ("Traffic Cam AI", "ตรวจจับป้ายทะเบียนรถ", "ระบบรักษาความปลอดภัยเข้าออกอาคาร"),
        ("Health Tracker", "บันทึกสุขภาพรายวัน", "เชื่อมต่อกับ Smart Watch เพื่อดึงข้อมูลชีพจร"),
        ("E-Library", "ห้องสมุดออนไลน์", "ยืมคืนหนังสือ E-Book ผ่านแท็บเล็ต")
    ]

    for i, (name, fullname, detail) in enumerate(project_data):
        p_id = f"PROJ-{i+1:03d}"
        Project.objects.get_or_create(
            project_id=p_id,
            defaults={
                'project_name': name,
                'project_fullname': fullname,
                'project_detail': detail,
                'date_time': timezone.now(),
                'create_by': "Admin Seed"
            }
        )
    print(f"สร้างโปรเจกต์เรียบร้อย (10 โครงการ)")

    # --- เคลียร์ข้อมูลเก่าก่อน (เฉพาะ Team และ TeamStudent เพื่อรีเซ็ตโครงสร้างทีม) ---
    TeamStudent.objects.all().delete()
    Team.objects.all().delete()
    # Booking.objects.all().delete()
    # Project.objects.all().delete()
    # Student.objects.all().delete()
    # Facility.objects.all().delete()

    # --- 0. สร้างผู้ใช้งาน (Login) ---
    # ... (Login creation remains same - omitting for brevity in diff, wait, replace_file_content expects exact context match)
    # Actually I should just target the Team generation section specifically if possible, 
    # but I want to uncomment the delete lines at the top too.
    # Let's do it in two chunks or one large chunk if contiguous? They are far apart.
    # I'll use multi_replace for safety or just replace the chunks relevant.
    
    # Let's stick to modifying the "Create Team" section first, and I will manually add the delete calls there.
    
    # ... (skipping to Team section) ...
    
    # --- 4. สร้างทีม (Team) ---
    print(f"กำลังรีเซ็ตข้อมูลทีม...")
    TeamStudent.objects.all().delete()
    Team.objects.all().delete()

    projects = Project.objects.all()
    
    count = 0
    for proj in projects:
        t_id = f"TEAM-{count+1:03d}"
        t_name = f"{proj.project_name} Team" # ตั้งชื่อทีมตามโปรเจกต์
        
        Team.objects.get_or_create(
            team_id=t_id,
            defaults={
                'team_name': t_name,
                'project_name': proj.project_name,
                'date_time': timezone.now()
            }
        )
        count += 1
    print(f"สร้างทีมเรียบร้อย ({count} ทีม - ตามจํานวนโปรเจกต์)")

    # --- 4.5. เชื่อมโยงนักศึกษาเข้าทีม (TeamStudent) ---
    all_teams = Team.objects.all()
    all_students = Student.objects.all()
    
    if len(all_teams) > 0 and len(all_students) > 0:
        count = 0
        for student in all_students:
            # สุ่มให้ 1 คนอยู่ 1-2 ทีม
            chosen_teams = random.sample(list(all_teams), k=random.randint(1, 2))
            for team in chosen_teams:
                ts_id = f"TS-{datetime.now().year}-{count+1:04d}"
                TeamStudent.objects.get_or_create(
                    tsid=ts_id,
                    defaults={
                        'team_name': team.team_name,
                        'student': student.student_id  # เก็บเป็น ID ตามโมเดล
                    }
                )
                count += 1
        print(f"เชื่อมโยงนักศึกษาเข้าทีมเรียบร้อย ({count} ความสัมพันธ์)")

    # --- 5. สร้างห้อง (Facility) ---
    print("Creating Facilities (Zones A-D, Floors 1-4)...")
    Booking.objects.all().delete()
    Facility.objects.all().delete()

    zones = ['A', 'B', 'C', 'D']
    floors = [1, 2, 3, 4]

    count = 0
    for zone in zones:
        for floor in floors:
            # Generate rooms 00 to 05 for demo (User mentioned up to 30)
            for i in range(0, 6): 
                # Code logic: TA100, TA101... TA200...
                room_code = (floor * 100) + i
                f_id = f"T{zone}{room_code}"
                
                # Determine type
                if i < 2:
                    ftype = "Meeting Room"
                    cap = 10
                elif i < 4:
                    ftype = "Lecture Room"
                    cap = 30
                else:
                    ftype = "Lab"
                    cap = 20

                Facility.objects.create(
                    facility_id=f_id,
                    facility_name=f_id,
                    facility_type=ftype,
                    capacity=cap,
                    location=f"Zone {zone}, Floor {floor}",
                    zone=zone,
                    floor=floor,
                    status='Available'
                )
                count += 1
    print(f"สร้างห้อง/อุปกรณ์เรียบร้อย ({count} รายการ)")

    # --- 6. สร้างไทม์ไลน์โครงการ (Project Timeline) ---
    print("Creating Project Timelines...")
    ProjectTimeline.objects.all().delete()
    
    milestones = [
        ("ยื่นข้อเสนอโครงการ", "ยื่นเอกสารและรอการอนุมัติเบื้องต้น"),
        ("อนุมัติโครงการ", "ผ่านการพิจารณาจากคณะกรรมการ"),
        ("เริ่มดำเนินงาน", "ทีมงานเริ่มพัฒนาผลิตภัณฑ์ต้นแบบ"),
        ("ทดสอบการใช้งาน", "นำไปทดสอบจริงกับกลุ่มเป้าหมาย"),
        ("ปิดโครงการ", "ส่งมอบงานและสรุปผลสำเร็จ")
    ]
    
    for proj in Project.objects.all():
        # Randomly choose current progress stage (1 to 5)
        current_stage = random.randint(1, 5)
        
        base_date = proj.date_time.date()
        
        for i, (title, desc) in enumerate(milestones):
            m_date = base_date + timedelta(days=i*15)
            
            if i + 1 < current_stage:
                status = "Completed"
            elif i + 1 == current_stage:
                status = "In Progress"
            else:
                status = "Pending"
                
            ProjectTimeline.objects.create(
                project=proj,
                milestone_title=title,
                milestone_date=m_date,
                status=status,
                description=desc
            )
            
    print("สร้างไทม์ไลน์เรียบร้อย")

    print("-" * 50)
    print("SEED DATA SUCCESS!")
    print("ไปที่: http://127.0.0.1:8000/projects/ เพื่อลองค้นหาได้เลย")

if __name__ == '__main__':
    run_seed()