from django.db import models, connection
from django.apps import AppConfig
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.utils import ProgrammingError
from authentication.models import User
from comments.models import Comment
# from supervisor.models import Supervisor
# from trainee.models import Trainee

from supervisor.models import Supervisor
from trainee.models import Trainee
from academy.validators import Marksheet as ms

from rest_framework import status
from rest_framework.response import Response

# Models (unchanged from your original code)
#####################################################################
class Designation(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

#####################################################################
class Institute(models.Model):
    name = models.CharField(max_length=124)
    acronym = models.CharField(max_length=16, unique=True)
    code = models.IntegerField(blank=True, unique=True)
    about = models.TextField(blank=True)
    history = models.TextField(blank=True)
    def __str__(self):
        return self.name

#####################################################################
class Department(models.Model):
    name = models.CharField(max_length=124)
    acronym = models.CharField(max_length=16, unique=True)
    code = models.IntegerField(unique=True)
    about = models.TextField(blank=True)
    history = models.TextField(blank=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    def __str__(self):
        return self.acronym

#####################################################################
class DegreeType(models.Model):
    name = models.CharField(max_length=124)
    acronym = models.CharField(max_length=16, unique=True)
    code = models.IntegerField(unique=True)
    def __str__(self):
        return self.acronym




#####################################################################
class Program(models.Model):
    name = models.CharField(max_length=124)
    acronym = models.CharField(max_length=16, unique=True)
    code = models.IntegerField(unique=True)
    duration = models.CharField(max_length=24, blank=True)
    required_credits = models.IntegerField(null=True)
    availability = models.CharField(max_length=32, blank=True)
    entry_period = models.CharField(max_length=64, blank=True)
    details = models.TextField(blank=True)
    degree_type = models.ForeignKey(DegreeType, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.acronym

#####################################################################
class TermChoices(models.Model):
    name = models.CharField(max_length=100)
    start = models.CharField(max_length=24, blank=True)
    end = models.CharField(max_length=24, blank=True)
    def __str__(self):
        return self.name

#####################################################################
class Semester(models.Model):
    term = models.ForeignKey(TermChoices, on_delete=models.CASCADE)
    year = models.IntegerField()
    code = models.IntegerField(unique=True)
    is_open = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    programs = models.ManyToManyField(Program, blank=True)
    def __str__(self):
        return f'{self.term.name} {self.year}'
    class Meta:
        unique_together = ['term', 'year']

#####################################################################
class Course(models.Model):
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=16)
    code = models.IntegerField()
    credit = models.FloatField()
    programs = models.ManyToManyField(Program, blank=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='+')
    def __str__(self):
        return f'{self.acronym} {self.code}'
    class Meta:
        unique_together = ['acronym', 'code', 'credit']

#####################################################################
class SupervisorEnrollment(models.Model):
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    designations = models.ManyToManyField(Designation)
    departments = models.ManyToManyField(Department)
    enrolled_by = models.ForeignKey(User, related_name='supervisor_enrolled_by', on_delete=models.SET_NULL, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='supervisor_enrollment_updated_by', on_delete=models.SET_NULL, blank=True, null=True)
    on_duty = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.supervisor.acronym} - {self.designations} - {self.departments}'

#####################################################################
class Batch(models.Model):
    number = models.PositiveIntegerField()
    program = models.ForeignKey(Program, related_name='batch', on_delete=models.SET_NULL, blank=True, null=True)
    session = models.CharField(max_length=9, blank=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.program}: Batch {self.number}'
    class Meta:
        unique_together = ['number', 'program']

class Section(models.Model):
    name = models.CharField(max_length=50)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='sections')
    max_seats = models.PositiveIntegerField(default=10)
    def __str__(self):
        return f'{self.batch}: Section {self.name}'
    class Meta:
        unique_together = ['name', 'batch']
    def get_available_seats(self):
        enrolled_count = TraineeEnrollment.objects.filter(batch_section=self).count()
        return self.max_seats - enrolled_count

#####################################################################
class TraineeEnrollment(models.Model):
    YEAR_CHOICES = [
        ("FR", "Freshman"), ("SO", "Sophomore"), ("JR", "Junior"),
        ("SR", "Senior"), ("GR", "Graduate"),
    ]
    year = models.CharField(max_length=2, choices=YEAR_CHOICES, default='FR')
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    batch_section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)
    enrolled_by = models.ForeignKey(User, related_name='trainee_enrolled_by', on_delete=models.SET_NULL, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='trainee_enrollment_updated_by', on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Trainee Enrollment: {self.trainee} - {self.batch_section}'

#####################################################################
class CourseOffer(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True)
    capacity = models.PositiveIntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    comments = GenericRelation(Comment)
    class Meta:
        unique_together = ['semester', 'course', 'supervisor']
    def __str__(self):
        return f'{self.course} - {self.semester} - {self.supervisor}'

#####################################################################
class CourseEnrollment(models.Model):
    course_offer = models.ForeignKey(CourseOffer, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    non_credit = models.BooleanField(default=False)
    regular = models.BooleanField(default=True)
    class Meta:
        unique_together = ['course_offer', 'trainee']
    def __str__(self):
        return f'Course Enrollment: {self.course_offer} - {self.trainee}'

#####################################################################
class CGPATable(models.Model):
    lower_mark = models.DecimalField(max_digits=5, decimal_places=2)
    higher_mark = models.DecimalField(max_digits=5, decimal_places=2)
    letter_grade = models.CharField(max_length=5)
    grade_point = models.DecimalField(max_digits=3, decimal_places=2)
    def __str__(self):
        return f"{self.letter_grade}: {self.grade_point}"

#####################################################################
class Marksheet(models.Model):
    course_enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE)
    attendance = models.FloatField(null=True, blank=True, validators=[ms.validate_attendance])
    assignment = models.FloatField(null=True, blank=True, validators=[ms.validate_assignment])
    mid_term = models.FloatField(null=True, blank=True, validators=[ms.validate_mid_term])
    final = models.FloatField(null=True, blank=True, validators=[ms.validate_final])
    is_published = models.BooleanField(default=False)
    def __str__(self):
        return f'Marksheet for {self.course_enrollment}'



    
class AcademicCalendarWeekend(models.Model):
    day = models.CharField(max_length=20, unique=True)
    is_weekend = models.BooleanField(default=True)

    def __str__(self):
        return self.day






class LessonPlan(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    creator = models.ForeignKey(User, related_name='created_plans', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assigned_plans', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Report(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    creator = models.ForeignKey(User, related_name='created_reports', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Assessment(models.Model):
    trainee = models.ForeignKey(User, related_name='assessments', on_delete=models.CASCADE)
    supervisor = models.ForeignKey(User, related_name='given_assessments', on_delete=models.CASCADE)
    score = models.IntegerField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment for {self.trainee.email} by {self.supervisor.email}"
    
# # Signal Handlers
# #####################################################################
# @receiver(post_migrate)
# def create_term_choices(sender, **kwargs):
#     app_config = kwargs.get('app_config')
#     if app_config and app_config.name == 'academy':
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT to_regclass('academy_termchoices')")
#             table_exists = cursor.fetchone()[0] is not None
        
#         if not table_exists:
#             print("Table 'academy_termchoices' does not exist yet; skipping term choices creation.")
#             return

#         term_choices_data = [
#             {'name': 'Fall', 'start': 'August', 'end': 'December'},
#             {'name': 'Autumn', 'start': 'September', 'end': 'December'},
#             {'name': 'Spring', 'start': 'January', 'end': 'May'},
#             {'name': 'Winter', 'start': 'January', 'end': 'April'},
#             {'name': 'Summer', 'start': 'May', 'end': 'August'},
#         ]
#         try:
#             for term_data in term_choices_data:
#                 TermChoices.objects.get_or_create(name=term_data['name'], defaults=term_data)
#             print("Default term choices added successfully.")
#         except ProgrammingError as e:
#             if 'academy_termchoices' in str(e):
#                 print("Table 'academy_termchoices' does not exist (caught exception); skipping term choices creation.")
#             else:
#                 raise

# #####################################################################
# @receiver(post_migrate)
# def create_designations(sender, **kwargs):
#     app_config = kwargs.get('app_config')
#     if app_config and app_config.name == 'academy':
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT to_regclass('academy_designation')")
#             table_exists = cursor.fetchone()[0] is not None
        
#         if not table_exists:
#             print("Table 'academy_designation' does not exist yet; skipping designation creation.")
#             return

#         designations_data = [
#             'New Recruit', 'Teaching Assistant', 'Instructor', 'Lecturer', 'Senior Lecturer',
#             'Principal Lecturer', 'Assistant Professor', 'Associate Professor', 'Professor',
#             'Distinguished Professor', 'Honorary Professor', 'Research Associate',
#             'Postdoctoral Fellow', 'Chair/Chairperson', 'Head of Department', 'Dean',
#             'Emeritus Professor', 'Visiting Professor', 'Adjunct Professor', 'Research Professor',
#         ]
#         try:
#             for designation_name in designations_data:
#                 Designation.objects.get_or_create(name=designation_name)
#             print("Default designations added successfully.")
#         except ProgrammingError as e:
#             if 'academy_designation' in str(e):
#                 print("Table 'academy_designation' does not exist (caught exception); skipping designation creation.")
#             else:
#                 raise

# #####################################################################
# # @receiver(post_migrate)
# # def create_degree_types(sender, **kwargs):
# #     app_config = kwargs.get('app_config')
# #     if app_config and app_config.name == 'academy':
# #         with connection.cursor() as cursor:
# #             cursor.execute("SELECT to_regclass('academy_degretype')")
# #             table_exists = cursor.fetchone()[0] is not None
        
# #         if not table_exists:
# #             print("Table 'academy_degretype' does not exist yet; skipping degree types creation.")
# #             return

# #         degree_types_data = [
# #             {'name': 'Bachelor of Arts', 'acronym': 'BA', 'code': '101'},
# #             {'name': 'Bachelor of Architecture', 'acronym': 'BArch', 'code': '102'},
# #             {'name': 'Bachelor of Business Administration', 'acronym': 'BBA', 'code': '103'},
# #             {'name': 'Bachelor of Education', 'acronym': 'BEd', 'code': '104'},
# #             {'name': 'Bachelor of Engineering', 'acronym': 'BEng', 'code': '105'},
# #             {'name': 'Bachelor of Fine Arts', 'acronym': 'BFA', 'code': '106'},
# #             {'name': 'Bachelor of Pharmacy', 'acronym': 'BPharm', 'code': '107'},
# #             {'name': 'Bachelor of Science', 'acronym': 'BSc', 'code': '108'},
# #             {'name': 'Bachelor of Social Science', 'acronym': 'BSS', 'code': '109'},
# #             {'name': 'Doctor of Business Administration', 'acronym': 'DBA', 'code': '201'},
# #             {'name': 'Doctor of Social Work', 'acronym': 'DSW', 'code': '202'},
# #             {'name': 'Doctor of Education', 'acronym': 'EdD', 'code': '203'},
# #             {'name': 'Bachelor of Laws', 'acronym': 'LLB', 'code': '204'},
# #             {'name': 'Master of Laws', 'acronym': 'LLM', 'code': '205'},
# #             {'name': 'Master of Arts', 'acronym': 'MA', 'code': '301'},
# #             {'name': 'Master of Architecture', 'acronym': 'MArch', 'code': '302'},
# #             {'name': 'Master of Business Administration', 'acronym': 'MBA', 'code': '303'},
# #             {'name': 'Master of Education', 'acronym': 'MEd', 'code': '304'},
# #             {'name': 'Master of Engineering', 'acronym': 'MEng', 'code': '305'},
# #             {'name': 'Master of Fine Arts', 'acronym': 'MFA', 'code': '306'},
# #             {'name': 'Master of Philosophy', 'acronym': 'MPhil', 'code': '307'},
# #             {'name': 'Master of Science', 'acronym': 'MSc', 'code': '308'},
# #             {'name': 'Master of Social Work', 'acronym': 'MSW', 'code': '309'},
# #             {'name': 'Doctor of Pharmacy', 'acronym': 'PharmD', 'code': '401'},
# #             {'name': 'Doctor of Philosophy', 'acronym': 'PhD', 'code': '402'},
# #             {'name': 'Doctor of Psychology', 'acronym': 'PsyD', 'code': '403'},
# #         ]
# #         try:
# #             for degree_data in degree_types_data:
# #                 DegreeType.objects.get_or_create(**degree_data)
# #             print("Default degree types added successfully.")
# #         except ProgrammingError as e:
# #             if 'academy_degretype' in str(e):
# #                 print("Table 'academy_degretype' does not exist (caught exception); skipping degree types creation.")
# #             else:
# #                 raise



# @receiver(post_migrate)
# def create_degree_types(sender, **kwargs):
#     """
#     Populate default degree types after all migrations have been applied.
#     This signal runs only when app_config is None (global post_migrate).
#     """
#     if kwargs.get('app_config') is not None:
#         return

#     # Check if the 'academy_degretype' table exists.
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT to_regclass('academy_degretype')")
#         table_exists = cursor.fetchone()[0] is not None

#     if not table_exists:
#         print("Table 'academy_degretype' does not exist yet; skipping degree types creation.")
#         return

#     degree_types_data = [
#         {'name': 'Bachelor of Arts', 'acronym': 'BA', 'code': 101},
#         {'name': 'Bachelor of Architecture', 'acronym': 'BArch', 'code': 102},
#         {'name': 'Bachelor of Business Administration', 'acronym': 'BBA', 'code': 103},
#         {'name': 'Bachelor of Education', 'acronym': 'BEd', 'code': 104},
#         {'name': 'Bachelor of Engineering', 'acronym': 'BEng', 'code': 105},
#         {'name': 'Bachelor of Fine Arts', 'acronym': 'BFA', 'code': 106},
#         {'name': 'Bachelor of Pharmacy', 'acronym': 'BPharm', 'code': 107},
#         {'name': 'Bachelor of Science', 'acronym': 'BSc', 'code': 108},
#         {'name': 'Bachelor of Social Science', 'acronym': 'BSS', 'code': 109},
#         {'name': 'Doctor of Business Administration', 'acronym': 'DBA', 'code': 201},
#         {'name': 'Doctor of Social Work', 'acronym': 'DSW', 'code': 202},
#         {'name': 'Doctor of Education', 'acronym': 'EdD', 'code': 203},
#         {'name': 'Bachelor of Laws', 'acronym': 'LLB', 'code': 204},
#         {'name': 'Master of Laws', 'acronym': 'LLM', 'code': 205},
#         {'name': 'Master of Arts', 'acronym': 'MA', 'code': 301},
#         {'name': 'Master of Architecture', 'acronym': 'MArch', 'code': 302},
#         {'name': 'Master of Business Administration', 'acronym': 'MBA', 'code': 303},
#         {'name': 'Master of Education', 'acronym': 'MEd', 'code': 304},
#         {'name': 'Master of Engineering', 'acronym': 'MEng', 'code': 305},
#         {'name': 'Master of Fine Arts', 'acronym': 'MFA', 'code': 306},
#         {'name': 'Master of Philosophy', 'acronym': 'MPhil', 'code': 307},
#         {'name': 'Master of Science', 'acronym': 'MSc', 'code': 308},
#         {'name': 'Master of Social Work', 'acronym': 'MSW', 'code': 309},
#         {'name': 'Doctor of Pharmacy', 'acronym': 'PharmD', 'code': 401},
#         {'name': 'Doctor of Philosophy', 'acronym': 'PhD', 'code': 402},
#         {'name': 'Doctor of Psychology', 'acronym': 'PsyD', 'code': 403},
#     ]
#     try:
#         for degree_data in degree_types_data:
#             DegreeType.objects.get_or_create(**degree_data)
#         print("Default degree types added successfully.")
#     except ProgrammingError as e:
#         if 'academy_degretype' in str(e):
#             print("Table 'academy_degretype' does not exist (caught exception); skipping degree types creation.")
#         else:
#             raise
# #####################################################################
# @receiver(post_migrate)
# def create_institutes(sender, **kwargs):
#     app_config = kwargs.get('app_config')
#     if app_config and app_config.name == 'academy':
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT to_regclass('academy_institute')")
#             table_exists = cursor.fetchone()[0] is not None
        
#         if not table_exists:
#             print("Table 'academy_institute' does not exist yet; skipping institutes creation.")
#             return

#         institutes = [
#             {'name': 'Institute of Science, Technology, Engineering, and Mathematics', 'acronym': 'STEM', 'code': '1001', 'about': 'The Institute of Science, Technology, Engineering, and Mathematics (STEM) offers a comprehensive education and research environment in the fields of science, technology, engineering, and mathematics, fostering innovation, problem-solving, and interdisciplinary collaboration.', 'history': ''},
#             {'name': 'Institute of Social Sciences', 'acronym': 'ISS', 'code': '1002', 'about': 'The Institute of Social Sciences conducts research and offers academic programs focused on the study of societies, cultures, and human behavior.', 'history': ''},
#             {'name': 'Institute of Business and Economics', 'acronym': 'IBE', 'code': '1003', 'about': 'The Institute of Business and Economics is dedicated to providing comprehensive education and research opportunities in the fields of business management, economics, and entrepreneurship.', 'history': ''},
#             {'name': 'Institute of Health Sciences', 'acronym': 'IHS', 'code': '1004', 'about': 'The Institute of Health Sciences is committed to advancing healthcare through cutting-edge research, interdisciplinary collaboration, and the education of future healthcare professionals.', 'history': ''},
#             {'name': 'Institute of Humanities', 'acronym': 'IH', 'code': '1005', 'about': 'The Institute of Humanities explores the diverse aspects of human thought, creativity, and expression, fostering critical thinking, cultural understanding, and artistic exploration.', 'history': ''},
#             {'name': 'Institute of Environmental Studies', 'acronym': 'IES', 'code': '1006', 'about': 'The Institute of Environmental Studies focuses on understanding and addressing environmental challenges through interdisciplinary research, education, and sustainable practices.', 'history': ''},
#             {'name': 'Institute of Computing and Information Technology', 'acronym': 'ICIT', 'code': '1007', 'about': 'The Institute of Computing and Information Technology is dedicated to advancing computer science, information technology, and related fields through research, innovation, and industry collaboration.', 'history': ''},
#             {'name': 'Institute of Arts and Design', 'acronym': 'IAD', 'code': '1008', 'about': 'The Institute of Arts and Design offers a creative and intellectually stimulating environment for the exploration and development of artistic expression, design, and visual communication.', 'history': ''},
#             {'name': 'Institute of Communication and Media Studies', 'acronym': 'ICMS', 'code': '1009', 'about': 'The Institute of Communication and Media Studies examines the dynamic and evolving nature of communication and media, exploring their social, cultural, and technological impact.', 'history': ''},
#             {'name': 'Institute of Law and Legal Studies', 'acronym': 'ILLS', 'code': '1010', 'about': 'The Institute of Law and Legal Studies provides a comprehensive understanding of legal principles, ethics, and governance, preparing students for careers in law, advocacy, and policy-making.', 'history': ''},
#             {'name': 'Institute of Education and Pedagogy', 'acronym': 'IEP', 'code': '1011', 'about': 'The Institute of Education and Pedagogy focuses on the theory and practice of education, preparing educators and researchers to make a positive impact on learning and instructional methodologies.', 'history': ''},
#             {'name': 'Institute of Agriculture and Rural Development', 'acronym': 'IARD', 'code': '1012', 'about': 'The Institute of Agriculture and Rural Development is dedicated to advancing sustainable agricultural practices, rural development strategies, and food security through research, education, and community engagement.', 'history': ''},
#             {'name': 'Institute of Psychology and Behavioral Sciences', 'acronym': 'IPBS', 'code': '1013', 'about': 'The Institute of Psychology and Behavioral Sciences investigates the complexities of human behavior, cognition, and mental processes, providing insights into individual and societal well-being.', 'history': ''},
#             {'name': 'Institute of Architecture and Urban Planning', 'acronym': 'IAUP', 'code': '1014', 'about': 'The Institute of Architecture and Urban Planning explores the art and science of designing sustainable and livable built environments, addressing the challenges of urban development and architectural design.', 'history': ''},
#             {'name': 'Institute of Energy and Sustainable Resources', 'acronym': 'IESR', 'code': '1015', 'about': 'The Institute of Energy and Sustainable Resources conducts research and offers educational programs focused on renewable energy, energy efficiency, and sustainable resource management, addressing global energy challenges and environmental sustainability.', 'history': ''},
#             {'name': 'Institute of Culture, Language and Literature', 'acronym': 'ICLL', 'code': '1016', 'about': 'The Institute of Culture, Language, and Literature (ICLL) is a prestigious academic institution dedicated to the study and exploration of various aspects of culture, language, and literature. The ICLL offers a wide range of programs and courses that delve into the rich tapestry of human culture, linguistic diversity, and literary traditions.', 'history': ''},
#         ]
#         try:
#             for institute in institutes:
#                 Institute.objects.get_or_create(**institute)
#             print("Default institutes added successfully.")
#         except ProgrammingError as e:
#             if 'academy_institute' in str(e):
#                 print("Table 'academy_institute' does not exist (caught exception); skipping institutes creation.")
#             else:
#                 raise

# #####################################################################
# @receiver(post_migrate)
# def populate_cgpa_table(sender, **kwargs):
#     app_config = kwargs.get('app_config')
#     if app_config and app_config.name == 'academy':
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT to_regclass('academy_cgpatable')")
#             table_exists = cursor.fetchone()[0] is not None
        
#         if not table_exists:
#             print("Table 'academy_cgpatable' does not exist yet; skipping CGPA table creation.")
#             return

#         cgpa_data = [
#             (80.00, 100.00, 'A+', 4.00), (75.00, 79.99, 'A', 3.75), (70.00, 74.99, 'A-', 3.50),
#             (65.00, 69.99, 'B+', 3.25), (60.00, 64.99, 'B', 3.00), (55.00, 59.99, 'B-', 2.75),
#             (50.00, 54.99, 'C+', 2.50), (45.00, 49.99, 'C', 2.25), (40.00, 44.99, 'D', 2.00),
#             (0.00, 39.99, 'F', 0.00),
#         ]
#         try:
#             for cgpa_entry in cgpa_data:
#                 CGPATable.objects.get_or_create(
#                     lower_mark=cgpa_entry[0], higher_mark=cgpa_entry[1],
#                     letter_grade=cgpa_entry[2], grade_point=cgpa_entry[3]
#                 )
#             print("Default CGPA table entries added successfully.")
#         except ProgrammingError as e:
#             if 'academy_cgpatable' in str(e):
#                 print("Table 'academy_cgpatable' does not exist (caught exception); skipping CGPA table creation.")
#             else:
#                 raise
            


# @receiver(post_migrate)
# def create_weekend_data(sender, **kwargs):
#     """
#     Populate default weekend data after all migrations have been applied.
#     This signal runs only when app_config is None.
#     """
#     if kwargs.get('app_config') is not None:
#         return

#     # Note: Django's default table name for AcademicCalendarWeekend is 'academy_academiccalendarweekend'
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT to_regclass('academy_academiccalendarweekend')")
#         table_exists = cursor.fetchone()[0] is not None

#     if not table_exists:
#         print("Table 'academy_academiccalendarweekend' does not exist yet; skipping weekend creation.")
#         return

#     weekend_data = [
#         {'day': 'Saturday', 'is_weekend': True},
#         {'day': 'Sunday', 'is_weekend': True},
#     ]
#     try:
#         for data in weekend_data:
#             AcademicCalendarWeekend.objects.get_or_create(**data)
#         print("Default weekend data created successfully.")
#     except ProgrammingError as e:
#         if 'academy_academiccalendarweekend' in str(e):
#             print("Table 'academy_academiccalendarweekend' does not exist (caught exception); skipping weekend creation.")
#         else:
#             raise