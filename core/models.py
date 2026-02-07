from django.db import models
from django.utils import timezone

# ==========================================
# 1. กลุ่มคนและผู้ใช้งาน (People & Users)
# ==========================================

class Login(models.Model):
    user_id = models.CharField(db_column='UserID', primary_key=True, max_length=50)
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)
    full_name = models.CharField(db_column='FullName', max_length=255, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)
    permission = models.CharField(db_column='Permission', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Login'  # ชื่อตารางจริงใน Database

class Faculty(models.Model):
    faculty_name = models.CharField(db_column='FacultyName', primary_key=True, max_length=100)
    number_code = models.CharField(db_column='NumberCode', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Faculty'

class Student(models.Model):
    student_id = models.CharField(db_column='StudentID', primary_key=True, max_length=50)
    type_student = models.CharField(db_column='Type_Student', max_length=50, blank=True, null=True)
    full_name = models.CharField(db_column='FullName', max_length=255, blank=True, null=True)
    type_student_english = models.CharField(db_column='Type_Student_English', max_length=50, blank=True, null=True)
    full_name_english = models.CharField(db_column='FullName_English', max_length=255, blank=True, null=True)
    nickname = models.CharField(db_column='Nickname', max_length=100, blank=True, null=True)
    major = models.CharField(db_column='Major', max_length=100, blank=True, null=True)
    faculty = models.CharField(db_column='Faculty', max_length=50, blank=True, null=True) # เก็บชื่อคณะ
    year_of_study = models.CharField(db_column='Year_of_Study', max_length=50, blank=True, null=True)
    tel = models.CharField(db_column='Tel', max_length=50, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)
    date_time = models.DateTimeField(db_column='Date_Time', blank=True, null=True)
    create_by = models.CharField(db_column='Create_By', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Students'

class Advisor(models.Model):
    advisor_id = models.CharField(db_column='AdvisorID', primary_key=True, max_length=50)
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)
    full_name = models.CharField(db_column='FullName', max_length=255, blank=True, null=True)
    type_english = models.CharField(db_column='Type_English', max_length=50, blank=True, null=True)
    full_name_english = models.CharField(db_column='FullName_English', max_length=255, blank=True, null=True)
    position_advisor = models.CharField(db_column='Position_Advisor', max_length=100, blank=True, null=True)
    nickname = models.CharField(db_column='Nickname', max_length=100, blank=True, null=True)
    research_title = models.TextField(db_column='ResearchTitle', blank=True, null=True)
    major = models.CharField(db_column='Major', max_length=100, blank=True, null=True)
    faculty = models.CharField(db_column='Faculty', max_length=50, blank=True, null=True)
    tel = models.CharField(db_column='Tel', max_length=50, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)
    expertise = models.TextField(db_column='Expertise', blank=True, null=True)
    # ตัดฟิลด์ย่อยๆ บางตัวออกเพื่อความกระชับ แต่โครงสร้างหลักครบ
    date_time = models.DateTimeField(db_column='Date_Time', blank=True, null=True)

    class Meta:
        db_table = 'Advisors'

class Employee(models.Model):
    employee_id = models.CharField(db_column='EmployeeID', primary_key=True, max_length=50)
    full_name = models.CharField(db_column='FullName', max_length=255, blank=True, null=True)
    position = models.CharField(db_column='Position', max_length=100, blank=True, null=True)
    department = models.CharField(db_column='Department', max_length=100, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)
    tel = models.CharField(db_column='Tel', max_length=50, blank=True, null=True)
    permission = models.CharField(db_column='Permission', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Employee'

# ==========================================
# 2. กลุ่มนวัตกรรมและธุรกิจ (Innovation)
# ==========================================

class Project(models.Model):
    project_id = models.CharField(db_column='ProjectID', primary_key=True, max_length=50)
    project_name = models.CharField(db_column='ProjectName', max_length=255, blank=True, null=True)
    project_fullname = models.TextField(db_column='ProjectFullname', blank=True, null=True)
    project_detail = models.TextField(db_column='ProjectDetail', blank=True, null=True)
    objective = models.TextField(db_column='Objective', blank=True, null=True) # New
    budget_year = models.CharField(db_column='BudgetYear', max_length=20, blank=True, null=True) # New
    date_time = models.DateTimeField(db_column='Date_Time', blank=True, null=True)
    create_by = models.CharField(db_column='Create_By', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Projects'

    def __str__(self):
        return f"{self.project_name} ({self.project_id})"

class Team(models.Model):
    team_id = models.CharField(db_column='TeamID', primary_key=True, max_length=50)
    team_name = models.CharField(db_column='TeamName', max_length=255, blank=True, null=True)
    project_name = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)
    concept = models.TextField(db_column='Concept', blank=True, null=True) # New
    development_needs = models.TextField(db_column='DevelopmentNeeds', blank=True, null=True) # New
    date_time = models.DateTimeField(db_column='Date_Time', blank=True, null=True)

    class Meta:
        db_table = 'Teams'

class Company(models.Model):
    company_id = models.CharField(db_column='CompanyID', primary_key=True, max_length=50)
    product = models.TextField(db_column='Product', blank=True, null=True)
    company_detail = models.TextField(db_column='Company_Detail', blank=True, null=True)
    tel = models.CharField(db_column='Tel', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Company'

class Entrepreneur(models.Model):
    entrepreneur_id = models.AutoField(db_column='EntrepreneurID', primary_key=True)
    business_name = models.CharField(db_column='Business_Name', max_length=255, blank=True, null=True)
    fullname = models.CharField(db_column='Fullname', max_length=255, blank=True, null=True)
    tel = models.CharField(db_column='Tel', max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = 'Entrepreneur'

class EntrepreneurIncome(models.Model):
    ei_id = models.AutoField(primary_key=True)
    entrepreneur_id = models.CharField(db_column='EntrepreneurID', max_length=50, blank=True, null=True) # Linked to Entrepreneur
    year = models.CharField(db_column='Year', max_length=20, blank=True, null=True)
    income = models.DecimalField(db_column='Income', max_digits=12, decimal_places=2, blank=True, null=True)
    details = models.TextField(db_column='Details', blank=True, null=True)

    class Meta:
        db_table = 'EntrepreneurIncome'

# ==========================================
# 3. กลุ่มกิจกรรม (Activities)
# ==========================================

class Training(models.Model):
    training_id = models.CharField(db_column='TrainingID', primary_key=True, max_length=50)
    training_name = models.CharField(db_column='TrainingName', max_length=255, blank=True, null=True)
    training_date = models.DateField(db_column='TrainingDate', blank=True, null=True) # Start Date
    training_end_date = models.DateField(db_column='TrainingEndDate', blank=True, null=True) # New: End Date
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, db_column='ProjectID', blank=True, null=True, related_name='trainings') # New: FK
    lecturer_name = models.CharField(db_column='LecturerName', max_length=255, blank=True, null=True) # New: Who trained
    description = models.TextField(db_column='Description', blank=True, null=True)

    class Meta:
        db_table = 'Training'

class StudentTraining(models.Model):
    stid = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='StudentID', related_name='trainings')
    training = models.ForeignKey('Training', on_delete=models.CASCADE, db_column='TrainingID', related_name='participants')
    status = models.CharField(db_column='Status', max_length=50, default='Registered') # Registered, Attended

    class Meta:
        db_table = 'Student_Training'
        unique_together = ('student', 'training')

class SpeakerTraining(models.Model):
    spt_id = models.AutoField(primary_key=True)
    speaker_id = models.CharField(db_column='SpeakerID', max_length=50, blank=True, null=True)
    training_id = models.CharField(db_column='TrainingID', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Speaker_Training'

class ProjectAward(models.Model):
    paid = models.CharField(db_column='PAID', primary_key=True, max_length=50)
    team_name = models.CharField(db_column='TeamName', max_length=50, blank=True, null=True)
    project_name = models.CharField(db_column='ProjectName', max_length=50, blank=True, null=True)
    award_name = models.CharField(db_column='AwardName', max_length=255, blank=True, null=True) # New
    rank = models.CharField(db_column='Rank', max_length=50, blank=True, null=True) # New: Winner, Runner-up, etc.
    around = models.CharField(db_column='Around', max_length=50, blank=True, null=True)
    year = models.CharField(db_column='Year', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Project_Award'

class StudentAward(models.Model):
    said = models.AutoField(primary_key=True)
    student = models.CharField(db_column='StudentID', max_length=50, blank=True, null=True)
    award_name = models.CharField(db_column='AwardName', max_length=255, blank=True, null=True)
    around = models.CharField(db_column='Around', max_length=50, blank=True, null=True)
    year = models.CharField(db_column='Year', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Student_Award'

# ==========================================
# 4. ระบบบริการและปฏิบัติการ (Services - NEW)
# ==========================================

class Facility(models.Model):
    facility_id = models.CharField(db_column='FacilityID', primary_key=True, max_length=50)
    facility_name = models.CharField(db_column='FacilityName', max_length=255)
    facility_type = models.CharField(db_column='FacilityType', max_length=50, blank=True, null=True)
    capacity = models.IntegerField(db_column='Capacity', blank=True, null=True)
    location = models.TextField(db_column='Location', blank=True, null=True)
    zone = models.CharField(db_column='Zone', max_length=10, blank=True, null=True)
    floor = models.IntegerField(db_column='Floor', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=20, default='Available')
    description = models.TextField(db_column='Description', blank=True, null=True)
    photo = models.TextField(db_column='Photo', blank=True, null=True) # เก็บ URL
    created_at = models.DateTimeField(db_column='Created_At', auto_now_add=True)

    class Meta:
        db_table = 'Facilities'

class Booking(models.Model):
    booking_id = models.CharField(db_column='BookingID', primary_key=True, max_length=50)
    facility = models.ForeignKey(Facility, models.DO_NOTHING, db_column='FacilityID', blank=True, null=True)
    booked_by_user = models.ForeignKey(Login, models.DO_NOTHING, db_column='BookedBy_UserID', blank=True, null=True)
    registrant_name = models.CharField(db_column='RegistrantName', max_length=255, blank=True, null=True)
    booking_date = models.DateField(db_column='BookingDate', blank=True, null=True)
    start_time = models.TimeField(db_column='StartTime', blank=True, null=True)
    end_time = models.TimeField(db_column='EndTime', blank=True, null=True)
    topic = models.CharField(db_column='Topic', max_length=255, blank=True, null=True)
    phone_number = models.CharField(db_column='PhoneNumber', max_length=20, blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=20, default='Pending')

    @property
    def is_active(self):
        now = timezone.localtime(timezone.now())
        current_date = now.date()
        current_time = now.time()
        
        if self.booking_date == current_date and self.start_time and self.end_time:
            if self.start_time <= current_time <= self.end_time:
                return True
        return False
    
    @property
    def display_status(self):
        # Cancelled or Rejected override time-based status
        if self.status in ['Cancelled', 'Rejected']:
            return self.status
            
        now = timezone.localtime(timezone.now())
        current_date = now.date()
        current_time = now.time()
        
        # Check if Completed (Past)
        if self.booking_date and self.booking_date < current_date:
            return 'Completed'
        if self.booking_date and self.booking_date == current_date and self.end_time and self.end_time < current_time:
            return 'Completed'
            
        # Check if In Progress (Reuse is_active)
        if self.is_active:
            return 'In Progress'
            
        return self.status
    
    class Meta:
        db_table = 'Bookings'

class MaintenanceRequest(models.Model):
    request_id = models.CharField(db_column='RequestID', primary_key=True, max_length=50)
    requester = models.ForeignKey(Login, models.DO_NOTHING, db_column='RequesterID', blank=True, null=True)
    facility = models.ForeignKey(Facility, models.DO_NOTHING, db_column='FacilityID', blank=True, null=True)
    issue_title = models.CharField(db_column='Issue_Title', max_length=255, blank=True, null=True)
    description = models.TextField(db_column='Description', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=20, default='New')

    class Meta:
        db_table = 'Maintenance_Requests'

class DocumentRepository(models.Model):
    doc_id = models.CharField(db_column='DocID', primary_key=True, max_length=50)
    doc_name = models.CharField(db_column='DocName', max_length=255)
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)
    file_link = models.TextField(db_column='File_Link')
    
    class Meta:
        db_table = 'Document_Repository'

# ==========================================
# 5. ตารางเชื่อมโยง (Junction Tables)
# ==========================================

class StudentAdvisor(models.Model):
    stad_id = models.CharField(db_column='STADID', primary_key=True, max_length=50)
    student = models.CharField(db_column='StudentID', max_length=50, blank=True, null=True)
    advisor = models.CharField(db_column='AdvisorID', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Student_Advisors'

class TeamStudent(models.Model):
    tsid = models.CharField(db_column='TSID', primary_key=True, max_length=50)
    team_name = models.CharField(db_column='TeamName', max_length=255, blank=True, null=True)
    student = models.CharField(db_column='StudentID', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Team_Student'

class ProjectTimeline(models.Model):
    timeline_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='timelines')
    milestone_title = models.CharField(max_length=255)
    milestone_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, default='Pending') # Pending, In Progress, Completed
    description = models.TextField(blank=True, null=True)
    evidence_file = models.FileField(upload_to='timeline_evidence/', blank=True, null=True)

    class Meta:
        db_table = 'ProjectTimeline'
        ordering = ['milestone_date']

class TeamAdvisor(models.Model):
    taid = models.CharField(db_column='TAID', primary_key=True, max_length=50)
    team_name = models.CharField(db_column='TeamName', max_length=255, blank=True, null=True)
    advisor = models.CharField(db_column='AdvisorID', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Team_Advisors'

class TeamProject(models.Model):
    tpid = models.CharField(db_column='TPID', primary_key=True, max_length=50)
    team_name = models.CharField(db_column='TeamName', max_length=255, blank=True, null=True)
    project_name = models.CharField(db_column='ProjectName', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Team_Projects'

class StudentProject(models.Model):
    spid = models.CharField(db_column='SPID', primary_key=True, max_length=50)
    student = models.CharField(db_column='StudentID', max_length=50, blank=True, null=True)
    project_name = models.CharField(db_column='ProjectName', max_length=255, blank=True, null=True)
    year = models.CharField(db_column='Year', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Student_Project'

class ResearcherProject(models.Model):
    res_proj_id = models.AutoField(db_column='ResProjID', primary_key=True)
    researcher_id = models.CharField(db_column='ResearcherID', max_length=50, blank=True, null=True)
    project_name = models.CharField(db_column='ProjectName', max_length=255, blank=True, null=True)
    year = models.CharField(db_column='Year', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Researcher_Project'

# ==========================================
# 6. ตารางข้อมูลย่อย (Master Data)
# ==========================================

class Researcher(models.Model):
    researcher_id = models.CharField(db_column='ResearcherID', primary_key=True, max_length=50)
    full_name = models.CharField(db_column='FullName', max_length=255, blank=True, null=True)
    expertise = models.TextField(db_column='Expertise_Researcher', blank=True, null=True)
    
    class Meta:
        db_table = 'Researcher'

class Speaker(models.Model):
    speaker_id = models.CharField(db_column='SpeakerID', primary_key=True, max_length=50)
    full_name = models.CharField(db_column='FullName', max_length=255, blank=True, null=True)
    expertise = models.TextField(db_column='Expertise', blank=True, null=True)
    
    class Meta:
        db_table = 'Speaker'

class Bank(models.Model):
    bank_name = models.CharField(db_column='BankName', primary_key=True, max_length=100)
    class Meta:
        db_table = 'Bank'

class Contest(models.Model):
    contest_id = models.AutoField(db_column='ContestID', primary_key=True)
    contest_name = models.CharField(db_column='ContestName', max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'Contest'

class Stock(models.Model):
    barcode = models.CharField(db_column='Barcode', primary_key=True, max_length=50)
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)
    total_stock = models.IntegerField(db_column='Total_Stock', blank=True, null=True)
    class Meta:
        db_table = 'Stock'

class StockMovement(models.Model):
    sm_id = models.AutoField(primary_key=True)
    stock_item = models.ForeignKey(Stock, on_delete=models.CASCADE, db_column='StockID')
    qty = models.IntegerField(db_column='Qty')
    action_type = models.CharField(db_column='ActionType', max_length=20) # In, Out
    date_time = models.DateTimeField(auto_now_add=True, db_column='Date_Time')
    user = models.CharField(db_column='UserID', max_length=50, blank=True, null=True) # Who did it

    class Meta:
        db_table = 'Stock_Movement'

# ==========================================
# 7. ระบบความปลอดภัยและตรวจสอบ (Security & Audit)
# ==========================================

class AuditLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.CharField(db_column='UserID', max_length=50, blank=True, null=True) # User Email or ID
    action = models.CharField(db_column='Action', max_length=50) # Create, Update, Delete
    model_name = models.CharField(db_column='ModelName', max_length=50) # Which table
    object_id = models.CharField(db_column='ObjectID', max_length=50, blank=True, null=True) # Record ID
    timestamp = models.DateTimeField(auto_now_add=True, db_column='Timestamp')
    details = models.TextField(db_column='Details', blank=True, null=True) # Changed fields JSON

    class Meta:
        db_table = 'Audit_Log'
        ordering = ['-timestamp']
